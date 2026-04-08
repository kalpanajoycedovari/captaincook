import streamlit as st
from agent import build_graph

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CaptionCook",
    page_icon="🍳",
    layout="centered"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main {
        background-color: #fdf8f3;
    }

    .title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: #2c1a0e;
        text-align: center;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #7a5c44;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .result-box {
        background-color: #fff8f2;
        border-left: 4px solid #d4845a;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
        color: #2c1a0e;
    }

    .score-box {
        background-color: #fff3e0;
        border: 2px solid #d4845a;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }

    .stButton > button {
        background-color: #d4845a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1.1rem;
        font-family: 'DM Sans', sans-serif;
        width: 100%;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: #b8694a;
    }

    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1.5px solid #d4845a;
        padding: 0.6rem 1rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="title">🍳 CaptionCook</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI content chef — drop in a topic, get a full Instagram brief</div>', unsafe_allow_html=True)
st.divider()

# ── Workflow Visualiser ────────────────────────────────────────────────────────
with st.expander("🔍 See how CaptionCook works under the hood"):
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:center; gap:0; padding:20px; flex-wrap:nowrap; overflow-x:auto;">
        <div style="background:#fff8f2; border:2px solid #d4845a; border-radius:12px; padding:12px 16px; text-align:center; min-width:130px;">
            <div style="font-size:1.3rem">🔍</div>
            <div style="font-weight:600; color:#2c1a0e; font-size:0.85rem">Trend Researcher</div>
            <div style="color:#7a5c44; font-size:0.72rem; margin-top:4px">Finds trending angles</div>
        </div>
        <div style="color:#d4845a; font-size:1.8rem; padding:0 6px;">→</div>
        <div style="background:#fff8f2; border:2px solid #d4845a; border-radius:12px; padding:12px 16px; text-align:center; min-width:130px;">
            <div style="font-size:1.3rem">✍️</div>
            <div style="font-weight:600; color:#2c1a0e; font-size:0.85rem">Caption Writer</div>
            <div style="color:#7a5c44; font-size:0.72rem; margin-top:4px">Writes viral caption</div>
        </div>
        <div style="color:#d4845a; font-size:1.8rem; padding:0 6px;">→</div>
        <div style="background:#fff8f2; border:2px solid #d4845a; border-radius:12px; padding:12px 16px; text-align:center; min-width:130px;">
            <div style="font-size:1.3rem">📋</div>
            <div style="font-weight:600; color:#2c1a0e; font-size:0.85rem">Strategy Advisor</div>
            <div style="color:#7a5c44; font-size:0.72rem; margin-top:4px">Builds content plan</div>
        </div>
        <div style="color:#d4845a; font-size:1.8rem; padding:0 6px;">→</div>
        <div style="background:#fff8f2; border:2px solid #d4845a; border-radius:12px; padding:12px 16px; text-align:center; min-width:130px;">
            <div style="font-size:1.3rem">⚡</div>
            <div style="font-weight:600; color:#2c1a0e; font-size:0.85rem">Virality Scorer</div>
            <div style="color:#7a5c44; font-size:0.72rem; margin-top:4px">Rates viral potential</div>
        </div>
    </div>
    <p style="text-align:center; color:#7a5c44; font-size:0.78rem; margin-top:4px;">Each node passes its output as context to the next — that's LangGraph state flow!</p>
    """, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
topic = st.text_input(
    "",
    placeholder="e.g. aesthetic london cafes, morning routine, thrift haul...",
    label_visibility="collapsed"
)

cook_button = st.button("Cook it! 🍳")

# ── Run Agent ──────────────────────────────────────────────────────────────────
if cook_button and topic.strip():
    app = build_graph()

    with st.status("CaptionCook is cooking... 🍳", expanded=True) as status:
        st.write("🔍 Researching trends...")
        result = app.invoke({"topic": topic})
        st.write("✍️ Writing your caption...")
        st.write("📋 Building content strategy...")
        st.write("⚡ Scoring virality...")
        status.update(label="Your content brief is ready! 🍳", state="complete")

    st.divider()

    # ── Results ────────────────────────────────────────────────────────────────
    st.markdown("### 📈 Trending Angles")
    st.markdown(f'<div class="result-box">{result["trends"]}</div>', unsafe_allow_html=True)

    st.markdown("### ✍️ Your Caption")
    st.markdown(f'<div class="result-box">{result["caption"]}</div>', unsafe_allow_html=True)
    st.code(result["caption"], language=None)

    st.markdown("### 📋 Content Strategy")
    st.markdown(f'<div class="result-box">{result["strategy"]}</div>', unsafe_allow_html=True)

    st.markdown("### ⚡ Virality Score")
    st.markdown(f'<div class="score-box">{result["score"]}</div>', unsafe_allow_html=True)

    st.divider()
    st.caption("Made with 🍳 CaptionCook — LangGraph + Ollama + Streamlit")

elif cook_button and not topic.strip():
    st.warning("Please enter a topic first!")