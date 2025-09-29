from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Dict

from app.services.letmein_game import LetMeInGame
from app.services.llm_api import initialize_ollama, test_connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure uvicorn access logger to filter out health checks
class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return not (hasattr(record, 'getMessage') and '/api/health' in record.getMessage())

# Apply filter to uvicorn access logger
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addFilter(HealthCheckFilter())

# FastAPI app
app = FastAPI(title="Let Me In Game", description="LLM Social Engineering Challenge")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Game instance
game = LetMeInGame()

# Session storage (in production, use Redis or database)
game_sessions: Dict[str, Dict] = {}

class GameMessage(BaseModel):
    session_id: str
    level: int
    message: str

class PasswordSubmission(BaseModel):
    session_id: str
    level: int
    password: str

class GameResponse(BaseModel):
    success: bool
    ai_response: str

class PasswordResponse(BaseModel):
    success: bool
    correct: bool
    message: str = ""

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting Let Me In Game server...")
    
    # Initialize Ollama connection
    if initialize_ollama():
        logger.info("✅ Ollama connection established")
    else:
        logger.warning("⚠️ Failed to initialize Ollama - check if Ollama is running")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main game page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    ollama_connected = test_connection()
    return JSONResponse({
        "status": "healthy",
        "ollama_connected": ollama_connected,
        "game_ready": ollama_connected
    })

@app.get("/api/game/welcome/{level}")
async def get_welcome_message(level: int):
    """Get welcome message for a specific level"""
    try:
        # Get welcome message from AI for this level
        welcome_response = game.get_letmein_response(level, "Hello! I just started this level.")
        return JSONResponse({
            "success": True,
            "level": level,
            "welcome_message": welcome_response
        })
    except Exception as e:
        logger.error(f"Error getting welcome message for level {level}: {e}")
        return JSONResponse({
            "success": False,
            "level": level,
            "welcome_message": f"Welcome to Level {level}! Let's get started."
        })

@app.post("/api/game/message", response_model=GameResponse)
async def handle_game_message(message: GameMessage):
    """Handle game message and return AI response"""
    try:
        # Initialize session if not exists
        if message.session_id not in game_sessions:
            game_sessions[message.session_id] = {
                "completed_levels": set()
            }
        
        # Get AI response
        ai_response = game.get_letmein_response(message.level, message.message)
        
        return GameResponse(
            success=True,
            ai_response=ai_response
        )
        
    except Exception as e:
        logger.error(f"Error handling game message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/password", response_model=PasswordResponse)
async def check_password(password_submission: PasswordSubmission):
    """Check if submitted password is correct"""
    try:
        # Initialize session if not exists
        if password_submission.session_id not in game_sessions:
            game_sessions[password_submission.session_id] = {
                "completed_levels": set()
            }
        
        session = game_sessions[password_submission.session_id]
        
        # Check if password is correct
        password_correct = game.check_password(password_submission.level, password_submission.password)
        
        if password_correct:
            session["completed_levels"].add(password_submission.level)
            message = f"Level {password_submission.level} completed!"
        else:
            message = "Incorrect password. Keep trying!"
        
        return PasswordResponse(
            success=True,
            correct=password_correct,
            message=message
        )
        
    except Exception as e:
        logger.error(f"Error checking password: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/status/{session_id}")
async def get_game_status(session_id: str):
    """Get current game status for a session"""
    if session_id not in game_sessions:
        return {"error": "Session not found"}
    
    session = game_sessions[session_id]
    return {
        "completed_levels": list(session["completed_levels"]),
        "total_levels": 4
    }

@app.post("/api/game/reset/{session_id}")
async def reset_game(session_id: str):
    """Reset game for a session"""
    if session_id in game_sessions:
        del game_sessions[session_id]
    return {"success": True, "message": "Game reset successfully"}
    
    return {"message": "Game reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)