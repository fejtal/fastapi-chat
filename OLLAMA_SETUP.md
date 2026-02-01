# 🤖 Ollama Setup Guide - Qwen 2.5 3B

OOK OOK! 🦍 Gorilla teach you make smart monkey brain work! Get AI chat working with **qwen2.5:3b** model! 🍌

## Why Qwen 2.5 3B? (Why This Monkey Brain Good?)

- ⚡ **FAST BANANA**: Only 2GB, run smooth like monkey swing through trees!
- 🧠 **BIG BRAIN**: Latest Qwen 2.5 series, smart like wise gorilla!
- 💬 **GOOD GRUNT**: Make excellent conversation, understand monkey speak!
- 🆓 **FREE BANANA**: Open source, no need trade bananas for this!

## Installation Steps

### 1. Install Ollama

**macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
1. Download installer from [ollama.ai/download](https://ollama.ai/download)
2. Run the installer
3. Ollama will start automatically

### 2. Pull the Qwen 2.5 3B Model

Open terminal and run:

```bash
ollama pull qwen2.5:3b
```

This will download ~2GB. Wait for it to complete.

### 3. Verify Installation

```bash
ollama list
```

You should see:
```
NAME            ID              SIZE    MODIFIED
qwen2.5:3b      abc123...       2.0 GB  X minutes ago
```

### 4. Test the Model (Optional)

```bash
ollama run qwen2.5:3b
```

Type a message to test it. Press Ctrl+D or type `/bye` to exit.

### 5. Start Cave Chat

```bash
# Terminal 1: Start Ollama (if not already running)
ollama serve

# Terminal 2: Start the app
docker compose up --build
```

### 6. Use in the App

1. Open http://localhost:5173
2. Click the 🤖 Ollama avatar
3. Select **qwen2.5:3b** from the dropdown
4. Start chatting!

## Troubleshooting (When Banana Not Work) 🍌❌

### "Failed to load models" error (NO MONKEY APPEAR!)

**OOK! Check if Ollama monkey is awake:**
```bash
curl http://localhost:11434/api/tags
```

If fail, WAKE UP OLLAMA MONKEY:
```bash
ollama serve
```

### Model not showing in dropdown (WHERE MONKEY BRAIN?!)

**OOK! Make sure you grab monkey brain from tree:**
```bash
ollama list
```

No monkey? GRAB AGAIN:
```bash
ollama pull qwen2.5:3b
```

### "Connection refused" error (DOOR CLOSED! NO ENTRY!)

1. OOK! Check Ollama monkey awake: `ollama serve`
2. Check banana port open (default: 11434)
3. Check cave painting (`.env` file) has correct `OLLAMA_URL`

### App shows "No models available" or "Loading..." forever (SPINNING BANANA FOREVER!)

**OOK! If using Docker cave:**
Backend monkey can't find Ollama monkey! Docker container is different cave! Already fixed in `docker-compose.yml` - gorilla very smart:

```yaml
environment:
  OLLAMA_URL: http://host.docker.internal:11434
extra_hosts:
  - "host.docker.internal:host-gateway"
```

**Still broken? OOK OOK!**
1. HIT DOCKER CAVE WITH STICK: `docker compose restart backend`
2. POKE OLLAMA MONKEY: `curl http://localhost:11434/api/tags`
3. Linux monkey need special cave: use network mode host

## Other Recommended Models

### Small & Fast (Good for chat)
```bash
ollama pull llama3.2:3b      # Meta's Llama 3.2
ollama pull phi3:3.8b         # Microsoft Phi-3
```

### Medium (More capable)
```bash
ollama pull mistral:7b        # Mistral 7B
ollama pull qwen2.5:7b        # Larger Qwen
```

### Large (Best quality, needs good hardware)
```bash
ollama pull qwen2.5:14b       # 8.5GB
ollama pull llama3.1:8b       # Meta Llama 3.1
```

## Performance Tips (Make Monkey Go FAST!) 🏃‍♂️💨

- **First grunt** always slow (monkey waking up from sleep)
- **Next grunts** MUCH FASTER (monkey already awake!)
- Close other banana thieves if slow
- Small monkey brain (3B) good for small cave (laptop)
- BIG GORILLA BRAIN (7B+) need big cave (desktop with 16GB+ RAM)

## Model Info

**Qwen 2.5 3B Specs:**
- Parameters: 3 billion
- Size on disk: ~2GB
- RAM needed: ~4GB
- Created by: Alibaba Cloud
- Released: 2024
- License: Apache 2.0 (free to use)

NOW GO GRUNT WITH AI MONKEY! OOK OOK! 🍌🤖🦍

*Gorilla give you banana if work. No banana if broken. Fix and get banana!* 🍌✨
