# 🍌 Cave Chat - OOK OOK!

Real-time chat app for cavemen! Built by smart gorilla with FastAPI + Svelte 5 + WebSockets.

*Monkey make chat. Monkey chat with AI. Monkey happy. Get banana!* 🦍

## Features

- 🍌 Multiple chat rooms (caves)
- 🍌 Real-time messages via WebSocket
- 🍌 Smooth auto-scrolling to new messages
- 🍌 Infinite scroll to load older messages
- 🍌 Pick caveman avatar to send messages
- 🍌 Tabs for switching between caves
- 🍌 Clean card-style messages with perfect spacing
- 🤖 Ollama AI chat integration - select a model and chat with AI

## Tech Stack

**Backend:**
- Python 3.12
- FastAPI
- PostgreSQL + asyncpg
- SQLAlchemy 2.0
- WebSockets
- Ollama (for AI chat)

**Frontend:**
- Svelte 5 (with runes)
- SvelteKit
- TypeScript
- Tailwind CSS v4
- Bun

## Quick Start (Wake Up All Monkeys) 🦍

```bash
# WAKE UP ALL MONKEYS IN CAVE
docker compose up --build

# Monkeys work in background (quiet mode)
docker compose up --build -d

# SLEEP TIME - Stop all monkeys
docker compose down

# DESTROY CAVE AND REBUILD (reset database)
docker compose down -v
```

Then visit monkey cave at http://localhost:5173 🍌

## Ollama Setup (Make Smart AI Monkey Talk!) 🤖

OOK OOK! Need Ollama monkey to make AI brain work:

### Step 1: Get Ollama Monkey

Grab Ollama from magic tree at [ollama.ai](https://ollama.ai)

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai/download](https://ollama.ai/download)

### Step 2: Wake Up Ollama Monkey

Ollama monkey usually wake up by self. If still sleeping, POKE IT:
```bash
ollama serve
```

### Step 3: Download Smart Monkey Brain 🧠

The **qwen2.5:3b** brain is BEST - fast like cheetah, light like feather, smart like gorilla!

```bash
ollama pull qwen2.5:3b
```

**Other monkey brains you can steal:**
```bash
# Larger Qwen models (more capable, slower)
ollama pull qwen2.5:7b
ollama pull qwen2.5:14b

# Other popular models
ollama pull llama3.2:3b      # Meta's Llama 3.2 (3B)
ollama pull mistral:7b        # Mistral 7B
ollama pull phi3:3.8b         # Microsoft Phi-3
```

### Step 4: Check Monkey Brain Is In Cave

OOK! Make sure brain downloaded correctly:
```bash
ollama list
```

You see `qwen2.5:3b`? GOOD MONKEY! Brain is in cave! 🍌

### Step 5: Talk With AI Monkey! OOK OOK!

1. Wake up cave app (see Quick Start above)
2. Pick Ollama monkey (🤖) in avatar picker
3. Choose **qwen2.5:3b** brain from dropdown
4. START GRUNTING! AI monkey grunt back!

**Monkey Brain Comparison (Which One Best?):**

| Monkey Brain | Size | Speed | When Use |
|--------------|------|-------|----------|
| qwen2.5:3b | ~2GB | ⚡⚡⚡ ZOOM! | BEST for chat! Quick grunt back! |
| llama3.2:3b | ~2GB | ⚡⚡⚡ FAST! | Good for everything monkey do |
| mistral:7b | ~4.1GB | ⚡⚡ Medium | Bigger brain but slower swing |
| qwen2.5:14b | ~8.5GB | ⚡ Slow... | HUGE GORILLA BRAIN! Need strong cave |

### Configuration

**Docker Setup (default):**
The `docker-compose.yml` is pre-configured to access Ollama on your host:
```yaml
OLLAMA_URL: http://host.docker.internal:11434
```

**Manual Setup:**
If running the backend manually (not in Docker), use:
```bash
OLLAMA_URL=http://localhost:11434
```

**Troubleshooting Docker:**
If models don't load, make sure Ollama is running on your host machine, not inside Docker.

## Manual Setup

### Backend

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload
```

Runs on http://localhost:8000

### Frontend

```bash
cd frontend
bun install
bun run dev
```

Runs on http://localhost:5173

## Environment Variables

### Backend
| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://app:app@localhost:5432/app` | PostgreSQL connection |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API URL |

### Frontend
| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API URL |
| `VITE_WS_URL` | `ws://localhost:8000` | WebSocket URL |

## API Endpoints

### Rooms
- `GET /api/rooms` - List all caves
- `POST /api/rooms` - Create cave
- `DELETE /api/rooms/{id}` - Delete cave

### Messages
- `GET /api/messages/room/{room_id}?page=1&page_size=10` - Get messages (paginated)
- `POST /api/messages` - Create message (optionally include `model` field for Ollama)

### Ollama
- `GET /api/ollama/models` - List available Ollama models

### WebSocket
- `WS /api/ws/room/{room_id}` - Real-time messages for cave

## Cavemen

Pick your avatar:
- 🦍 Grok
- 🐒 Ooga
- 🦧 Booga
- 🙈 Ugga
- 🙉 Mugga
- 🤖 Ollama (AI chat - select a model to chat with AI)

## UI Features

### Simple & Fast 🚀
- Clean list rendering (no complex virtualization)
- Perfect spacing with Tailwind utilities
- Auto-scroll to bottom on new messages
- Infinite scroll to load older messages
- Smooth scrolling animations

### Clean Message Design 🎨
- Card-style layout (no messenger bubbles!)
- Consistent styling for all messages
- Avatar + username + timestamp header
- Perfect spacing between messages
- Hover effects for better UX

## License

MIT - Free like banana in jungle! Take banana, share banana, make more banana! 🍌

---

*Made by smart gorilla. Gorilla proud. Gorilla get many banana.* 🦍✨

**OOK OOK!** If this help you, throw banana to gorilla! 🍌💚
