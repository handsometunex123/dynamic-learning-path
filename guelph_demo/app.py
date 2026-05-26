import streamlit as st

st.set_page_config(
    page_title="Dynamic Learning Path Generator",
    page_icon="🗺️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body {
    overflow: hidden !important;
    height: 100vh !important;
}
.stApp {
    overflow: hidden !important;
    height: 100vh !important;
}
.main {
    overflow: hidden !important;
    height: 100%;
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 700px;
    height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    scrollbar-width: thin;
    scrollbar-color: #374151 transparent;
}
.main .block-container::-webkit-scrollbar       { width: 4px; }
.main .block-container::-webkit-scrollbar-track  { background: transparent; }
.main .block-container::-webkit-scrollbar-thumb  { background: #374151; border-radius: 4px; }

/* agent cards */
.agent-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 20px;
    height: 100%;
}
.agent-bkt   { border-top: 3px solid #8b5cf6; }
.agent-route { border-top: 3px solid #3b82f6; }
.tag {
    display: inline-block;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 3px 9px; border-radius: 20px; margin-bottom: 10px;
}
.tag-bkt   { background:#2e1065; color:#a78bfa; }
.tag-route { background:#0c1e3a; color:#60a5fa; }
.agent-card h3 { font-size:1rem; color:#f9fafb; margin:0 0 7px; }
.agent-card p  { font-size:0.84rem; color:#9ca3af; line-height:1.6; margin:0; }

/* steps */
.step-row {
    display:flex; gap:12px; align-items:flex-start; margin-bottom:10px;
}
.step-num {
    min-width:26px; height:26px;
    background:#1d4ed8; color:white; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:0.74rem; font-weight:700; flex-shrink:0;
}
.step-text { color:#d1d5db; font-size:0.9rem; padding-top:3px; line-height:1.5; }

.section-label {
    font-size:0.68rem; font-weight:700; letter-spacing:0.1em;
    text-transform:uppercase; color:#4b5563; margin-bottom:14px;
}
.cta-hint {
    text-align:center; color:#4b5563;
    font-size:0.78rem; margin-top:8px;
}

@media (max-width: 640px) {
    .main .block-container { padding-top: 1rem; }
    h1 { font-size: 1.6rem !important; }
}
</style>
""", unsafe_allow_html=True)

# Hero

st.markdown("""
<div style="text-align:center; padding-bottom:6px;">
  <div style="font-size:2.8rem; margin-bottom:10px;">🗺️</div>
  <h1 style="font-size:2rem; font-weight:800; margin:0 0 8px; color:#f9fafb; line-height:1.25;">
    Dynamic Learning Path Generator
  </h1>
  <p style="color:#6b7280; font-size:0.98rem; margin:0; line-height:1.6;">
    "Google Maps for learning" — two AI agents diagnose what you know<br>
    and build a personalised route to your goal.
  </p>
</div>
""", unsafe_allow_html=True)

# CTA button

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

col_l, col_btn, col_r = st.columns([1, 2, 1])
with col_btn:
    if st.button("▶  Start Demo", type="primary", use_container_width=True):
        st.switch_page("pages/1_Learning_Path.py")

st.markdown(
    "<div class='cta-hint'>No setup required · opens instantly</div>",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# Agent cards

st.markdown("<div class='section-label'>How it works — 2 agents</div>",
            unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="medium")

with c1:
    st.markdown("""
<div class="agent-card agent-bkt">
  <span class="tag tag-bkt">Agent 1</span>
  <h3>🧠 Knowledge Tracer</h3>
  <p>Uses <strong style="color:#c4b5fd">Bayesian Knowledge Tracing</strong> to
  estimate how well you know each concept.<br><br>
  After every quiz answer it updates the mastery probability —
  accounting for guessing and slipping.</p>
</div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="agent-card agent-route">
  <span class="tag tag-route">Agent 2</span>
  <h3>🗺️ Path Router</h3>
  <p>Reads mastery estimates from Agent 1 and traverses a
  <strong style="color:#93c5fd">prerequisite Knowledge Graph</strong>.<br><br>
  Finds the shortest path through unmastered topics and
  re-routes automatically as your knowledge changes.</p>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# Steps

st.markdown("<div class='section-label'>What to expect</div>",
            unsafe_allow_html=True)

for num, text in [
    ("1", "Pick a <strong>learning goal</strong> from the dropdown — e.g. <em>OOP</em> or <em>Algorithms</em>"),
    ("2", "Answer the <strong>short diagnostic quiz</strong> — each answer updates your mastery in real time"),
    ("3", "Watch the <strong>knowledge map</strong> highlight your path and see the model calculations on the right"),
]:
    st.markdown(f"""
<div class="step-row">
  <div class="step-num">{num}</div>
  <div class="step-text">{text}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

col_l2, col_btn2, col_r2 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("▶  Start Demo ", key="btn2", type="primary", use_container_width=True):
        st.switch_page("pages/1_Learning_Path.py")
