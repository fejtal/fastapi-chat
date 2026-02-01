# 🦍 GORILLA MADE THIS WITH CLAUDE AI! NEVER LOOK AT CODE! ALL WORK PERFECT!

**Made by Claude Sonnet 4.5 & Opus!** Gorilla just grunt instructions. Claude write ALL code. Gorilla never read one line! Everything work! Magic! 🪄✨

⚠️ **MONKEY RUN LOCAL ONLY! NO DEPLOY! SECURITY NOT GOOD!** ⚠️

This cave for learning and banana experiments! No production! No internet! Run on monkey computer only! 🍌🦍

---

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
- 🦍 **Special AI Cave** - Dedicated room for chatting with gemma3:4b ALPHA GORILLA!
- 🤖 **Smart AI Detection** - Any room with "AI Cave" or "🤖" in name becomes AI-enabled!

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

## Quick Start (ONE COMMAND!) 🦍

### Step 1: Install Ollama & Get ALPHA BRAIN 🧠

First, install Ollama from [ollama.ai](https://ollama.ai):

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:** Download from [ollama.ai/download](https://ollama.ai/download)

Then download **gemma3:4b** - THE ONLY BRAIN THAT SPEAKS MONKEY! 🦍
```bash
ollama pull gemma3:4b
```

### Step 2: Start Ollama Service 🤖

Ollama usually starts automatically after install. If not, run:
```bash
ollama serve
```

**Keep this running!** It's the AI brain server! 🧠

### Step 3: Run Everything!

```bash
docker compose up --build
```

**THAT'S IT!** Visit http://localhost:5173 🍌

1. Go to **🤖 AI Cave** room (created automatically!)
2. Pick any caveman avatar (🦍 Grok, 🐒 Ooga, etc.)
3. Choose **gemma3:4b** model from dropdown
4. Type "OOK OOK!" and watch ALPHA GORILLA respond! 💪

## Useful Commands 🦍

```bash
# Stop all monkeys (keep database)
docker compose down

# Stop + DELETE DATABASE (fresh start!)
docker compose down -v

# Restart if broken
docker compose down && docker compose up --build

# Check if Ollama awake
curl http://localhost:11434/api/tags

# Wake up Ollama if sleeping
ollama serve
```

## Why gemma3:4b? 🦍

**ONLY THIS BRAIN UNDERSTANDS MONKEY LANGUAGE!**

- Talks like ALPHA GORILLA: "OOK! Me know this. Do this. 🍌"
- Uses banana bullets 🍌
- Simple words. Big brain. 💪
- True sigma energy! 🔥

Other brains talk boring human language. gemma3:4b = REAL GORILLA! 🦍✨

## Configuration

Docker automatically connects to Ollama on your host machine using `host.docker.internal:11434`.

**Just run `docker compose up --build` and everything works!** 🍌

## API Endpoints

### Rooms
- `GET /api/rooms` - List all caves
- `POST /api/rooms` - Create cave
- `DELETE /api/rooms/{id}` - Delete cave

### Messages
- `GET /api/messages/room/{room_id}?page=1&page_size=10` - Get messages (paginated)
- `POST /api/messages` - Create message (include `model` field in AI rooms for AI response)

### Ollama
- `GET /api/ollama/models` - List available Ollama models

### WebSocket
- `WS /api/ws/room/{room_id}` - Real-time messages for cave

## How AI Rooms Work 🤖

### Default Rooms Created:
1. **🤖 AI Cave (Talk to Qwen)** - Chat with ALPHA GORILLA AI!
2. **Cave 🍌** - Regular monkey chat

### Making AI Rooms:
Create any room with "AI Cave" or "🤖" in the name, and it becomes AI-enabled! 
- ModelSelector appears automatically
- Pick gemma3:4b and start talking to ALPHA GORILLA! 💪

### Cavemen Avatars:
Pick your monkey:
- 🦍 Grok
- 🐒 Ooga
- 🦧 Booga
- 🙈 Ugga
- 🙉 Mugga

**All monkeys can talk in AI Cave!** Just pick a model and GRUNT! 🦍

## UI Features

- 🚀 TanStack Virtual for smooth scrolling (handle 10,000+ messages!)
- 🎨 Clean card-style messages (no messenger bubbles!)
- 🍌 Perfect spacing (no overlap, consistent gaps)
- 💪 Auto-scroll to new messages
- 🌴 Infinite scroll for old messages
- 🦍 Jungle-themed loading with random monkey phrases

## License

MIT - Free like banana in jungle! Take banana, share banana, make more banana! 🍌

---

*Made by smart gorilla. Gorilla proud. Gorilla get many banana.* 🦍✨

**OOK OOK!** If this help you, throw banana to gorilla! 🍌💚
