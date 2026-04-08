# 🍳 CaptionCook

> *Your AI content chef — drop in a topic, get a full Instagram brief.*

CaptionCook is a **multi-agent AI system** built with LangGraph that researches trends, writes captions, builds a content strategy, and scores your idea for virality — all from a single topic input.

---

## 🎬 Demo

![CaptionCook Workflow](assets/demo.png)

---

## 🤖 How It Works

CaptionCook uses a **LangGraph state graph** — four specialised AI agents that fire sequentially, each passing its output as context to the next node.

```
__start__
    ↓
🔍 Trend Researcher    →  finds trending Instagram angles for your topic
    ↓
✍️  Caption Writer      →  writes a hook, body, CTA + 10 hashtags
    ↓
📋 Strategy Advisor    →  editing style, music vibe, best post time, reel length
    ↓
⚡ Virality Scorer     →  scores the idea /10 with strengths, weaknesses & verdict
    ↓
__end__
```

Each node updates a shared `CaptionCookState` TypedDict — that's LangGraph's state flow in action.

---

## 🧱 Tech Stack

| Layer | Tool |
|---|---|
| Agent framework | LangGraph + LangChain |
| LLM | Ollama (gemma3:4b) — runs locally |
| UI | Streamlit |
| Language | Python 3.11 |

---

## 🔑 Why Ollama? The API Key Journey

Building CaptionCook wasn't without its battles. Here's the honest story:

**Attempt 1 — Anthropic Claude API**
The original plan was to use Claude Haiku via the Anthropic API. The code worked perfectly — but the API requires credits and the free tier doesn't include API access. Without adding billing, every call returned:
```
anthropic.BadRequestError: Your credit balance is too low to access the Anthropic API.
```

**Attempt 2 — Google Gemini API (Free Tier)**
Switched to Gemini 2.0 Flash which advertises a free tier. Got the key, updated the code — but hit an immediate wall:
```
google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED
Quota exceeded — limit: 0
```
The free tier quota was at zero on the linked Google Cloud project. Tried `gemini-1.5-flash` as a fallback — that model returned a 404 as it's deprecated in the newer API version.

**The fix — Ollama**
Rather than keep chasing API keys, the smarter move was to run a model **locally for free**. Ollama lets you pull and run open-source models directly on your machine — no API key, no quota, no billing. We pulled `gemma3:4b` (3.3GB, Google's open-source model) and it works perfectly.

The tradeoff is speed — local inference is slower than a cloud API — but for a portfolio project and personal use, it's completely worth it. No cost, no limits, works offline.

> **Lesson learned:** Always have a local fallback. Cloud APIs are great for production, but Ollama is unbeatable for development and personal projects.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com) installed

### 1. Clone the repo
```bash
git clone https://github.com/kalpanajoycedovari/captaincook.git
cd captaincook
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install langgraph langchain langchain-anthropic langchain-community langchain-ollama streamlit python-dotenv grandalf
```

### 4. Pull the model
```bash
ollama pull gemma3:4b
```

### 5. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser and start cooking! 🍳

---

## 📁 Project Structure

```
captioncook/
├── agent.py       # LangGraph multi-agent brain (4 nodes)
├── app.py         # Streamlit UI
├── .env           # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 💡 Example Output

**Topic:** `aesthetic london cafes`

**Caption generated:**
> *"Okay, but seriously… this is the spot."* ☕️🍂
> Lost myself in the rain-soaked charm of a hidden gem in Walthamstow today — dark academia vibes, oat milk lattes, and a playlist that makes you want to read for hours...

**Virality Score:** 8.5/10

---

## 🔮 Future Plans

- [ ] Add Tavily web search for real-time trend data
- [ ] Export content brief as PDF
- [ ] Support for TikTok and Twitter/X briefs
- [ ] Add image prompt suggestions for the Reel cover

---

## 👩‍💻 Built By

**Joy (Kalpana Joyce Dovari)**
MSc Artificial Intelligence — Northumbria University London

[![GitHub](https://img.shields.io/badge/GitHub-kalpanajoycedovari-black?logo=github)](https://github.com/kalpanajoycedovari)

---

*Made with 🍳 LangGraph + Ollama + Streamlit*