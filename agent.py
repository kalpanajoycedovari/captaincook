import os
from dotenv import load_dotenv
from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

load_dotenv()

# ── Model ──────────────────────────────────────────────────────────────────────
llm = ChatOllama(model="gemma3:4b")

# ── Shared State ───────────────────────────────────────────────────────────────
class CaptionCookState(TypedDict):
    topic: str
    trends: str
    caption: str
    strategy: str
    score: str

# ── Node 1: Trend Researcher ───────────────────────────────────────────────────
def trend_researcher(state: CaptionCookState) -> CaptionCookState:
    topic = state["topic"]
    print(f"🔍 Researching trends for: {topic}")

    summary = llm.invoke(f"""
You are a social media trend analyst who knows Instagram inside out.

Topic: '{topic}'

Based on your knowledge of Instagram trends in 2024-2025, summarise:
1. The top 3 trending content angles for this topic
2. The most popular content styles (aesthetic, POV, tutorial, etc.)
3. The kind of hooks that stop the scroll for this niche

Be specific and concise. Format as a numbered list.
""")
    return {**state, "trends": summary.content}


# ── Node 2: Caption Writer ─────────────────────────────────────────────────────
def caption_writer(state: CaptionCookState) -> CaptionCookState:
    print("✍️  Writing caption...")

    caption = llm.invoke(f"""
You are an Instagram caption expert who writes viral content.

Topic: {state["topic"]}
Trending angles: {state["trends"]}

Write an engaging Instagram caption with:
- A strong hook (first line that stops the scroll)
- 3-4 lines of engaging body text
- A call to action
- 10 relevant hashtags

Make it feel natural, not corporate. Match the energy of current Instagram trends.
""")
    return {**state, "caption": caption.content}


# ── Node 3: Strategy Advisor ───────────────────────────────────────────────────
def strategy_advisor(state: CaptionCookState) -> CaptionCookState:
    print("📋 Building content strategy...")

    strategy = llm.invoke(f"""
You are an Instagram growth strategist.

Topic: {state["topic"]}
Caption written: {state["caption"]}

Give a short content strategy brief covering:
1. Editing style (cuts, transitions, pacing)
2. Music vibe (genre, energy, examples)
3. Best time to post
4. Reel length recommendation
5. One pro tip to maximise reach

Keep it practical and actionable.
""")
    return {**state, "strategy": strategy.content}


# ── Node 4: Virality Scorer ────────────────────────────────────────────────────
def virality_scorer(state: CaptionCookState) -> CaptionCookState:
    print("⚡ Scoring virality...")

    score = llm.invoke(f"""
You are a viral content expert.

Topic: {state["topic"]}
Caption: {state["caption"]}
Strategy: {state["strategy"]}
Trends: {state["trends"]}

Score this content idea out of 10 for virality potential.
Format your response exactly like this:

SCORE: X/10
STRENGTHS: (2-3 bullet points)
WEAKNESSES: (1-2 bullet points)
VERDICT: (one punchy sentence)
""")
    return {**state, "score": score.content}


# ── Build the Graph ────────────────────────────────────────────────────────────
def build_graph():
    graph = StateGraph(CaptionCookState)

    graph.add_node("trend_researcher", trend_researcher)
    graph.add_node("caption_writer", caption_writer)
    graph.add_node("strategy_advisor", strategy_advisor)
    graph.add_node("virality_scorer", virality_scorer)

    graph.set_entry_point("trend_researcher")
    graph.add_edge("trend_researcher", "caption_writer")
    graph.add_edge("caption_writer", "strategy_advisor")
    graph.add_edge("strategy_advisor", "virality_scorer")
    graph.add_edge("virality_scorer", END)

    return graph.compile()


# ── Run directly for testing ───────────────────────────────────────────────────
if __name__ == "__main__":
    app = build_graph()
    topic = input("Enter a topic for your Instagram content: ")
    result = app.invoke({"topic": topic})

    print("\n" + "="*60)
    print("🍳 CAPTIONCOOK RESULTS")
    print("="*60)
    print("\n📈 TRENDS\n", result["trends"])
    print("\n✍️  CAPTION\n", result["caption"])
    print("\n📋 STRATEGY\n", result["strategy"])
    print("\n⚡ VIRALITY SCORE\n", result["score"])