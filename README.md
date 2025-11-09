# VXCON 2025 AI - LLM Programming Educational Projects

This repository contains educational projects for teaching Large Language Model (LLM) programming concepts using Ollama, Python, and modern web technologies.

## 🎯 Projects

### 1. **Simple Chat** - Console LLM Chatbot
A terminal-based chatbot featuring "Chef Marco," demonstrating basic LLM interaction patterns.

**Key Learning Topics:**
- LLM API integration with Ollama
- System prompt design
- Console application development
- Docker containerization

**Quick Start:**
```bash
cd simple_chat
docker compose run --rm chatbot
```

you can modify the model from `gemma:270m` to other models like `gemma:4b` from `docker-compose.yml`

📖 **[Detailed Documentation](simple_chat/README.md)**

### 2. **LetMeIn Game** - Social Engineering AI Challenge
A web-based game where players attempt to trick an AI into revealing passwords across 4 difficulty levels.

**Key Learning Topics:**
- AI security and prompt injection
- Web application development (FastAPI + JavaScript)
- Session management and persistence
- LLM prompt engineering

**Quick Start:**
```bash
cd letmein
docker compose up --build
# Visit: http://localhost:8000
```

you can modify the model from `gemma:270m` to other models like `gemma:4b` from `config.json`

📖 **[Detailed Documentation](letmein/README.md)**

## 📚 Learning Resources

### **[Complete Learning Guide](learning.md)**
Comprehensive educational material covering:
- **LLM Parameters** (temperature, top_p, max_tokens)
- **System Prompt Engineering**
- **API Integration Patterns**
- **Security Considerations**
- **Docker and Containerization**
- **Common Pitfalls and Solutions**

## 🛠️ Prerequisites

### Required Software
- **Docker & Docker Compose** - For containerized deployment
- **Ollama** - Local LLM server ([Installation Guide](https://ollama.ai/))
- **Git** - For cloning the repository

### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required model
ollama pull gemma3:270m
```

## 🎓 Educational Objectives

This repository is designed to teach students:

1. **Practical LLM Integration** - Real-world API usage patterns
2. **AI Security Awareness** - Prompt injection and safety concepts
3. **Modern Development Practices** - Containerization, REST APIs, frontend/backend separation
4. **System Design** - Session management, error handling, user experience
5. **Prompt Engineering** - Crafting effective prompts for different use cases

## 🏗️ Project Architecture

```
vxcon2025_ai/
├── simple_chat/             # Console chatbot
│   ├── chat.py              # Main chatbot application
│   ├── system_prompts.py    # AI personality definitions
│   ├── docker-compose.yml
│   └── README.md
├── letmein/                 # Web-based AI security game
│   ├── app/
│   │   ├── services/        # Game logic and LLM integration
│   │   ├── static/          # Frontend assets (CSS, JS)
│   │   ├── templates/       # HTML templates
│   │   └── main.py          # FastAPI server
│   ├── docker-compose.yml
│   └── README.md
├── learning.md              # Comprehensive learning guide
└── README.md                # This file
```

## 🎯 Teaching Applications

### **Beginner Level**
- Start with Simple Chat to understand basic LLM interactions
- Learn about system prompts and parameter tuning
- Practice Docker basics and containerization

### **Intermediate Level**
- Explore LetMeIn game to understand AI security concepts
- Learn about prompt injection and defense strategies
- Study web application architecture patterns

### **Advanced Level**
- Implement additional security measures
- Add new game levels or chatbot personalities
- Explore performance optimization techniques
- Integrate with other LLM providers

## 🔗 Quick Navigation

| Component | Description | Documentation |
|-----------|-------------|---------------|
| **Simple Chat** | Console LLM chatbot | [README](simple_chat/README.md) |
| **LetMeIn Game** | Web-based AI security challenge | [README](letmein/README.md) |
| **Learning Guide** | Technical concepts and tutorials | [learning.md](learning.md) |

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vxcon2025_ai
   ```

2. **Install Ollama and pull the model:**
   ```bash
   ollama serve
   ollama pull gemma3:270m
   ```

3. **Choose a project to explore:**
   - For beginners: `cd simple_chat`
   - For web development: `cd letmein`

4. **Follow the project-specific README for detailed setup**

## 🤝 Contributing

This is an educational repository. Students and instructors are encouraged to:
- Add new game levels or chatbot personalities
- Improve security measures
- Enhance documentation
- Share learning experiences

## 📄 License

MIT License - Feel free to use for educational purposes.

---

**Happy Learning!** 🎓 These projects provide hands-on experience with modern LLM programming while teaching important concepts about AI safety, security, and practical application development.
