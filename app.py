"""
TokenLens — Streamlit Tokenizer Visualizer
Run with: pip install streamlit tiktoken && streamlit run app.py
"""

import streamlit as st
import tiktoken
import html

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TokenLens",
    page_icon="🔬",
    layout="wide",
)

# ─── Styling ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.main { background: #0a0a0f; }
.stApp { background: #0a0a0f; color: #e8e6f0; }

/* Token colors */
.tok { display: inline; border-radius: 3px; padding: 2px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 2.1; cursor: default; }
.tok-0 { background: rgba(124,106,255,0.25); color: #b8acff; }
.tok-1 { background: rgba(255,106,171,0.25); color: #ffaccc; }
.tok-2 { background: rgba(106,220,255,0.25); color: #acedff; }
.tok-3 { background: rgba(255,200,80,0.25);  color: #ffd980; }
.tok-4 { background: rgba(80,255,160,0.25);  color: #80ffb8; }
.tok-5 { background: rgba(255,140,80,0.25);  color: #ffb880; }
.tok-6 { background: rgba(200,80,255,0.25);  color: #d480ff; }
.tok-7 { background: rgba(80,200,255,0.25);  color: #80d4ff; }

.token-display {
    background: #111118;
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    min-height: 80px;
    font-family: 'JetBrains Mono', monospace;
    line-height: 2.2;
    word-break: break-word;
}

.stat-box {
    background: #111118;
    border: 1px solid #2a2a3a;
    border-top: 2px solid #7c6aff;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #e8e6f0;
    letter-spacing: -0.04em;
    line-height: 1;
}

.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b6880;
    margin-top: 0.3rem;
}

.token-table {
    background: #111118;
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    overflow: hidden;
    width: 100%;
}

.token-table-row {
    display: flex;
    align-items: center;
    padding: 0.4rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    gap: 0.75rem;
}

.token-table-row:last-child { border-bottom: none; }
.tok-idx { color: #6b6880; min-width: 2.5rem; text-align: right; }
.tok-text { flex: 1; }
.tok-id { color: #6b6880; min-width: 4rem; text-align: right; }

h1.title {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #7c6aff, #ff6aab);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}
</style>
""", unsafe_allow_html=True)

# ─── Model configs ────────────────────────────────────────────────────────────
from tokenlens.core import MODELS, PRICING, COLORS, tokenize, get_encoder as _get_encoder

# ─── Functions ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_encoder(encoding_name: str):
    return _get_encoder(encoding_name)

def render_token_display(tokens: list[dict]) -> str:
    if not tokens:
        return '<div class="token-display" style="color:#6b6880;font-style:italic;font-family:\'JetBrains Mono\',monospace">Your tokenized text will appear here…</div>'
    parts = []
    for i, t in enumerate(tokens):
        color_cls = f"tok-{i % COLORS}"
        safe = html.escape(t["text"]).replace(" ", "&nbsp;")
        tok_id = t["id"]
        tok_bytes = t["bytes"]
        parts.append(f'<span class="tok {color_cls}" title="#{i} · ID:{tok_id} · {tok_bytes}B">{safe}</span>')
    inner = "".join(parts)
    return f'<div class="token-display">{inner}</div>'

def render_token_table(tokens: list[dict], limit: int = 100) -> str:
    rows = []
    for i, t in enumerate(tokens[:limit]):
        color_cls = f"tok-{i % COLORS}"
        safe = html.escape(t["text"]).replace(" ", "·").replace("\n", "↵").replace("\t", "→")
        rows.append(
            f'<div class="token-table-row">'
            f'<span class="tok-idx">{i}</span>'
            f'<span class="tok-text tok {color_cls}" style="padding:2px 6px;border-radius:4px">{safe}</span>'
            f'<span class="tok-id">{t["id"]}</span>'
            f'</div>'
        )
    if len(tokens) > limit:
        rows.append(f'<div class="token-table-row" style="justify-content:center;color:#6b6880">+ {len(tokens)-limit} more tokens</div>')
    return f'<div class="token-table">{"".join(rows)}</div>'

# ─── UI ──────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="title">🔬 TokenLens</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#6b6880;font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;letter-spacing:0.1em;margin-bottom:1.5rem">TOKENIZER VISUALIZER · POWERED BY TIKTOKEN</p>', unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    model_label = st.selectbox("Model / Encoding", list(MODELS.keys()), index=0)
    encoding_name = MODELS[model_label]
    
    text_input = st.text_area(
        "Input text",
        value="The quick brown fox jumps over the lazy dog. Tokenization splits text into tokens — the atomic units that language models process.",
        height=200,
        placeholder="Type or paste text here…"
    )

    # Tokenize
    try:
        enc = get_encoder(encoding_name)
        tokens = tokenize(text_input, enc) if text_input else []
    except Exception as e:
        st.error(f"Encoding error: {e}")
        tokens = []

    st.markdown("**Token Visualization**")
    st.markdown(render_token_display(tokens), unsafe_allow_html=True)

with col_right:
    # Stats
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(tokens):,}</div>
            <div class="stat-label">Tokens</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(text_input):,}</div>
            <div class="stat-label">Characters</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")

    ratio = f"{len(text_input)/len(tokens):.1f}" if tokens else "—"
    st.markdown(f"""
    <div class="stat-box" style="text-align:left;margin-bottom:1rem">
        <div class="stat-label">Encoder</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:1rem;color:#e8e6f0;margin-top:0.3rem">{encoding_name}</div>
        <div class="stat-label" style="margin-top:0.5rem">Chars/token ratio: <span style="color:#7c6aff">{ratio}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # API cost estimates
    st.markdown("**Estimated API Cost**")
    if tokens:
        cost_data = []
        for model_name, price_per_m in PRICING.items():
            cost = len(tokens) / 1_000_000 * price_per_m
            cost_data.append({"Model": model_name, "Cost (input)": f"${cost:.6f}"})
        st.table(cost_data)
    else:
        st.caption("Enter text to see cost estimates.")

    # Token list
    st.markdown("**Token List**")
    if tokens:
        st.markdown(render_token_table(tokens, limit=80), unsafe_allow_html=True)
    else:
        st.caption("No tokens yet.")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    '<p style="font-family:\'JetBrains Mono\',monospace;font-size:0.7rem;color:#6b6880">'
    'Built with <a href="https://github.com/openai/tiktoken" style="color:#7c6aff">tiktoken</a> · '
    'All processing is local · No data sent anywhere'
    '</p>',
    unsafe_allow_html=True
)