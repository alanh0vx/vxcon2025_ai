# Simple Chat - LLM Chef Assistant

A console-based chatbot that role-plays as "Chef Marco," an enthusiastic chef assistant powered by Ollama and gemma3:270m model.

## Features

- 👨‍🍳 **Chef Marco Role-Play**: Interactive chef character with cooking expertise
- 🍳 **Recipe Assistant**: Get recipes, cooking tips, and culinary advice
- 💬 **Console Interface**: Simple terminal-based chat experience
- 🐳 **Docker Support**: Easy containerized deployment
- 🤖 **Ollama Integration**: Uses local Ollama with gemma3:270m model
- ⌨️ **Graceful Exit**: Press Ctrl+C to exit cleanly

## Prerequisites

- **Ollama**: Must be installed and running on the host machine
- **Docker & Docker Compose**: For containerized deployment
- **gemma3:270m model**: Will be auto-pulled if not available

### Install Ollama

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull the required model
ollama pull gemma3:270m
```

## Quick Start

1. **Clone and navigate to the directory:**
   ```bash
   cd simple_chat
   ```

2. **Start the chatbot:**
   ```bash
   docker compose run --rm chatbot
   ```

3. **Interact with Chef Marco:**
   - Enter your name when prompted
   - Ask for recipes, cooking tips, or culinary advice
   - Press Ctrl+C to exit

## Usage Examples

Once started, you can ask Chef Marco questions like:

- "Can you give me a recipe for pasta carbonara?"
- "How do I properly season a steak?"
- "What's a good vegetarian dinner for tonight?"
- "How do I make homemade bread?"
- "What spices go well with chicken?"

## Configuration

The application uses environment variables that can be configured in `docker-compose.yml`:

- `OLLAMA_ENDPOINT`: Ollama API endpoint (default: `http://host.docker.internal:11434`)
- `MODEL_NAME`: LLM model to use (default: `gemma3:270m`)

## Architecture

```
simple_chat/
├── chat.py              # Main chatbot application
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Docker Compose setup
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Development

### Running Locally (without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Ollama is running:**
   ```bash
   ollama serve
   ```

3. **Run the chatbot:**
   ```bash
   python chat.py
   ```

### Customizing the Chef Character

Edit the `system_prompt` in `chat.py` to modify Chef Marco's personality or expertise areas.

## Troubleshooting

**Problem: Cannot connect to Ollama**
- Ensure Ollama is running: `ollama serve`
- Ensure model is available: `ollama pull gemma3:270m`
- Verify port 11434 is accessible

**Problem: Model not found**
- Pull the model manually: `ollama pull gemma3:270m`
- Verify it's installed: `ollama list`

**Problem: Docker connection issues**
- On Windows: Ensure Docker Desktop is running
- Check that `host.docker.internal` resolves correctly

**Problem: Slow responses**
- The gemma3:270m model is lightweight but may be slow on older hardware
- Consider using a larger model like `gemma3:2b` for better performance
- Ensure sufficient RAM is available

## Features Detail

### Chef Marco Character
- **Personality**: Enthusiastic, experienced chef with 20+ years of expertise
- **Specialties**: International cuisine, cooking techniques, recipe adaptation
- **Interaction Style**: Patient, encouraging, educational
- **Scope**: Focuses on cooking-related topics, gently redirects off-topic questions

### Technical Features
- **Model Auto-pulling**: Automatically downloads required model if missing
- **Error Handling**: Graceful handling of connection issues and interruptions
- **Interactive Console**: Real-time chat with typing indicators
- **Signal Handling**: Clean exit with Ctrl+C
- **Docker Integration**: Seamless containerized deployment

## Contributing

This is a simple demonstration application. Feel free to extend it with:
- Additional chef personalities
- Recipe database integration
- Conversation history
- Multi-language support
- Voice integration

## License

MIT License - feel free to use and modify as needed.