import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from core.bayesian_kt import BKTModel
from core.knowledge_graph import CurriculumGraph
from core.course_data import BKT_DEFAULTS, QUIZ_QUESTIONS, LEARNING_GOALS, CONCEPT_RESOURCES

st.set_page_config(page_title="Learning Path Generator", layout="wide")

# CSS

st.markdown("""
<style>
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* labels */
.label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 12px;
}

/* quiz card */
.quiz-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-top: 3px solid #3b82f6;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 14px;
}
.quiz-meta { display:flex; align-items:center; gap:8px; margin-bottom:10px; }
.quiz-badge {
    background: #1d3a6e; color: #93c5fd;
    font-size: 0.68rem; font-weight: 700;
    padding: 2px 8px; border-radius: 20px;
}
.quiz-concept { color: #6b7280; font-size: 0.75rem; }
.quiz-q { color: #f3f4f6; font-size: 0.88rem; line-height: 1.6; margin: 0; }

/* mastery chips */
.chips-grid { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
.chip {
    border-radius: 6px; padding: 4px 8px;
    font-size: 0.72rem; font-weight: 600;
    border: 1px solid; white-space: nowrap;
}
.chip-mastered { background:#052e16; border-color:#10b981; color:#34d399; }
.chip-progress { background:#451a03; border-color:#f59e0b; color:#fbbf24; }
.chip-none     { background:#111827; border-color:#374151; color:#6b7280; }

/* path banner */
.path-banner {
    background: #0c1829; border: 1px solid #1e3a5f;
    border-radius: 8px; padding: 11px 16px;
    font-size: 0.84rem; color: #93c5fd;
    margin-bottom: 10px; line-height: 1.6;
}
.resource-row {
    display: flex; align-items: center; gap: 8px;
    background: #0a1628; border: 1px solid #1e3a5f;
    border-radius: 7px; padding: 9px 14px;
    font-size: 0.78rem; color: #60a5fa;
    margin-bottom: 12px; text-decoration: none;
}
.resource-row:hover { background: #0f1f3d; }

/* legend */
.legend-wrap { display:flex; gap:16px; flex-wrap:wrap; margin-top:10px; margin-bottom:14px; }
.legend-row { display:flex; align-items:center; gap:5px; font-size:0.74rem; color:#9ca3af; }
.legend-dot { width:10px; height:10px; border-radius:3px; flex-shrink:0; }
.legend-thr { color:#4b5563; font-size:0.68rem; }

/* activity log */
.log-scroll { overflow-y: auto; padding-right: 2px; }
.log-entry {
    border-left: 3px solid; border-radius: 0 6px 6px 0;
    padding: 9px 12px; margin-bottom: 7px; font-size: 0.78rem;
}
.log-bkt           { border-color:#7c3aed; background:#130f1e; }
.log-router        { border-color:#2563eb; background:#0a1628; }
.log-router-change { border-color:#22d3ee; background:#061e26; }
.log-agent-name { font-weight:700; font-size:0.74rem; }
.log-bkt    .log-agent-name { color:#a78bfa; }
.log-router .log-agent-name,
.log-router-change .log-agent-name { color:#60a5fa; }
.log-action { color:#e2e8f0; margin:3px 0 0; }
.log-result { color:#6b7280; font-size:0.72rem; margin-top:3px; }
.log-empty  { color:#374151; font-size:0.8rem; padding:10px; text-align:center; }

/* live trace */
.trace-card {
    background: #080d14; border: 1px solid #1e293b;
    border-radius: 10px; padding: 14px 16px; margin-bottom: 16px;
}
.trace-head {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #4b5563; margin-bottom: 12px;
}
.trace-answer-ok  { font-size:0.88rem; color:#34d399; font-weight:600; margin-bottom:10px; }
.trace-answer-bad { font-size:0.88rem; color:#f87171; font-weight:600; margin-bottom:10px; }
.trace-section {
    font-size: 0.68rem; font-weight: 700; letter-spacing:0.06em;
    text-transform: uppercase; color: #a78bfa;
    border-top: 1px solid #1e293b; padding-top: 10px; margin-top:10px; margin-bottom:8px;
}
.trace-section-router { color:#60a5fa; }
.trace-formula {
    font-family: 'Courier New', monospace;
    background: #0d1117; border: 1px solid #1e3a5f;
    border-radius: 6px; padding: 10px 12px;
    font-size: 0.72rem; color: #93c5fd;
    line-height: 1.8;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-word;
    overflow-x: auto;
}
.verdict-changed   { color:#34d399; font-size:0.82rem; margin-top:8px; }
.verdict-unchanged { color:#6b7280; font-size:0.82rem; margin-top:8px; }
.trace-empty {
    color:#374151; font-size:0.8rem; text-align:center;
    padding:28px 10px; border:1px dashed #1f2937; border-radius:8px;
}

/* bkt params */
.bkt-grid { display:grid; grid-template-columns:1fr 1fr; gap:7px; margin-top:6px; }
.bkt-cell {
    background:#0d1117; border:1px solid #1f2937;
    border-radius:7px; padding:9px 11px;
}
.bkt-sym  { font-size:0.9rem; font-weight:700; color:#a78bfa; }
.bkt-val  { font-size:0.75rem; color:#fbbf24; font-weight:600; margin:2px 0; }
.bkt-desc { font-size:0.67rem; color:#6b7280; line-height:1.4; }

/* ── Responsive ── */
@media (max-width: 1150px) {
    .trace-formula { font-size: 0.65rem; }
    .quiz-q        { font-size: 0.83rem; }
    .chip          { font-size: 0.68rem; padding: 3px 7px; }
}
@media (max-width: 900px) {
    .main .block-container { padding-top: 0.4rem; }
    .trace-formula  { font-size: 0.6rem; padding: 6px 8px; }
    .bkt-grid       { grid-template-columns: 1fr; }
    .path-banner    { font-size: 0.78rem; }
    .resource-row   { font-size: 0.72rem; }
    .legend-wrap    { gap: 8px; }
    .legend-row     { font-size: 0.68rem; }
}
@media (max-width: 640px) {
    .chips-grid     { gap: 3px; }
    .chip           { font-size: 0.65rem; padding: 3px 6px; }
    .trace-card     { padding: 10px; }
    .trace-formula  { font-size: 0.58rem; }
    .label          { font-size: 0.6rem; }
    .log-entry      { padding: 5px 8px; font-size: 0.72rem; }
}
</style>
""", unsafe_allow_html=True)

# Session state

if "bkt_model" not in st.session_state: st.session_state.bkt_model = BKTModel(BKT_DEFAULTS)
if "kg" not in st.session_state or not hasattr(st.session_state.kg, "render_dot"):
    st.session_state.kg = CurriculumGraph()
if "quiz_index" not in st.session_state: st.session_state.quiz_index = 0
if "quiz_done" not in st.session_state: st.session_state.quiz_done = False
if "goal" not in st.session_state: st.session_state.goal = LEARNING_GOALS[0]
if "agent_log" not in st.session_state: st.session_state.agent_log = []
if "last_path" not in st.session_state: st.session_state.last_path = []
if "last_explanation" not in st.session_state: st.session_state.last_explanation = None

bkt: BKTModel = st.session_state.bkt_model
kg: CurriculumGraph = st.session_state.kg

# Header row

hcol, gcol = st.columns([3, 1])
with hcol:
    st.markdown(
        "<h2 style='margin:0 0 4px;color:#f9fafb;font-size:1.35rem;'>"
        "Dynamic Learning Path Generator</h2>"
        "<p style='margin:0;color:#4b5563;font-size:0.8rem;'>"
        "Answer the quiz questions — agents update your mastery and re-route your path in real time.</p>",
        unsafe_allow_html=True,
    )
with gcol:
    goal = st.selectbox("Goal", LEARNING_GOALS, key="goal_select",
                        label_visibility="visible")
    st.session_state.goal = goal

st.divider()

# Three columns

left, center, right = st.columns([1, 2, 1], gap="medium")

# Left column — quiz and mastery

with left:
    st.markdown("<div class='label'>🧠 Agent 1 — Knowledge Tracer</div>",
                unsafe_allow_html=True)

    if not st.session_state.quiz_done:
        idx = st.session_state.quiz_index
        if idx < len(QUIZ_QUESTIONS):
            q = QUIZ_QUESTIONS[idx]
            st.markdown(f"""
<div class="quiz-card">
  <div class="quiz-meta">
    <span class="quiz-badge">Q{idx+1} / {len(QUIZ_QUESTIONS)}</span>
    <span class="quiz-concept">{q['concept']}</span>
  </div>
  <p class="quiz-q">{q['question']}</p>
</div>""", unsafe_allow_html=True)

            choice = st.radio("", q["options"], key=f"q_{idx}", index=None,
                              label_visibility="collapsed")
            if st.button("Submit →", key=f"sub_{idx}", type="primary",
                         use_container_width=True):
                if choice is None:
                    st.warning("Select an answer first.")
                else:
                    correct = (choice == q["answer"])
                    old_m   = bkt.mastery(q["concept"])
                    new_m   = bkt.update(q["concept"], correct)

                    # BKT values for the trace panel
                    G, S, T = 0.25, 0.10, 0.20
                    if correct:
                        numer = (1 - S) * old_m
                        denom = (1 - S) * old_m + G * (1 - old_m)
                        label = "(1−S)·L"
                    else:
                        numer = S * old_m
                        denom = S * old_m + (1 - G) * (1 - old_m)
                        label = "S·L"
                    posterior = numer / denom if denom else old_m

                    # Agent 1 log entry
                    st.session_state.agent_log.insert(0, {
                        "type": "bkt",
                        "name": "🧠 BKT Agent",
                        "action": f"{'✓ Correct' if correct else '✗ Wrong'} — {q['concept']}",
                        "result": f"Mastery: {old_m:.0%} → {new_m:.0%}",
                        "changed": False,
                    })

                    # Agent 2 log entry
                    old_path = list(st.session_state.last_path)
                    new_path = kg.get_learning_path(goal, bkt.all_mastery())
                    changed  = (new_path != old_path)
                    st.session_state.agent_log.insert(0, {
                        "type": "router",
                        "name": "🗺️ Path Router",
                        "action": f"Re-routed to '{goal}' {'← updated' if changed else '(unchanged)'}",
                        "result": (" → ".join(new_path)) if new_path else f"'{goal}' fully reachable!",
                        "changed": changed,
                    })
                    st.session_state.last_path = new_path

                    # Pass update data to the right panel
                    st.session_state.last_explanation = {
                        "concept":      q["concept"],
                        "correct":      correct,
                        "old_m":        old_m,
                        "numer":        numer,
                        "denom":        denom,
                        "label":        label,
                        "posterior":    posterior,
                        "new_m":        new_m,
                        "path_changed": changed,
                        "old_path":     old_path,
                        "new_path":     new_path,
                    }

                    st.session_state.quiz_index += 1
                    if st.session_state.quiz_index >= len(QUIZ_QUESTIONS):
                        st.session_state.quiz_done = True
                    st.rerun()
        else:
            st.session_state.quiz_done = True
            st.rerun()
    else:
        st.success("Diagnostic complete.")

    # Mastery chips

    st.markdown("<div class='label' style='margin-top:12px;'>Current mastery estimates</div>",
                unsafe_allow_html=True)

    mastery    = bkt.all_mastery()
    chips_html = "<div class='chips-grid' style='margin-bottom:8px;'>"
    for concept, m in mastery.items():
        cls = "chip-mastered" if m >= 0.70 else "chip-progress" if m >= 0.40 else "chip-none"
        chips_html += f"<span class='chip {cls}'>{concept} {m:.0%}</span>"
    chips_html += "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

    # BKT parameters

    with st.expander("⚙️ BKT model parameters"):
        st.markdown("""
<div class='bkt-grid'>
  <div class='bkt-cell'><div class='bkt-sym'>L₀</div><div class='bkt-val'>10%</div>
    <div class='bkt-desc'>Prior — chance you already know a concept</div></div>
  <div class='bkt-cell'><div class='bkt-sym'>T</div><div class='bkt-val'>20%</div>
    <div class='bkt-desc'>Learn rate — gain mastery per attempt</div></div>
  <div class='bkt-cell'><div class='bkt-sym'>G</div><div class='bkt-val'>25%</div>
    <div class='bkt-desc'>Guess — correct without knowing</div></div>
  <div class='bkt-cell'><div class='bkt-sym'>S</div><div class='bkt-val'>10%</div>
    <div class='bkt-desc'>Slip — wrong even when you know</div></div>
</div>""", unsafe_allow_html=True)

    if st.button("↺ Reset session", use_container_width=True):
        bkt.reset()
        st.session_state.quiz_index       = 0
        st.session_state.quiz_done        = False
        st.session_state.agent_log        = []
        st.session_state.last_path        = []
        st.session_state.last_explanation = None
        st.rerun()

# Center column — knowledge graph

with center:
    st.markdown("<div class='label'>🗺️ Agent 2 — Knowledge Map &amp; Path Router</div>",
                unsafe_allow_html=True)

    mastery = bkt.all_mastery()
    path    = kg.get_learning_path(goal, mastery)

    if any(m > 0.11 for m in mastery.values()):
        if path:
            path_str = " → ".join(path)
            st.markdown(
                f"<div class='path-banner'>"
                f"<strong>Recommended route to {goal}:</strong><br>{path_str}"
                f"</div>",
                unsafe_allow_html=True,
            )
            # Show learning resource for first unmastered concept in path
            next_concept = path[0]
            if next_concept in CONCEPT_RESOURCES:
                res_label, res_url = CONCEPT_RESOURCES[next_concept]
                st.markdown(
                    f"<a href='{res_url}' target='_blank' class='resource-row'>"
                    f"📖 Next resource: <strong>{res_label}</strong> — {next_concept}"
                    f"</a>",
                    unsafe_allow_html=True,
                )
        else:
            st.success(f"All prerequisites mastered for **{goal}**!")
    else:
        st.markdown(
            "<div style='color:#4b5563;font-size:0.82rem;margin-bottom:8px;'>"
            "Complete the quiz on the left to generate your personalised path.</div>",
            unsafe_allow_html=True,
        )

    dot = kg.render_dot(mastery_dict=mastery, highlight_path=path)
    st.graphviz_chart(dot, use_container_width=True)

    # Legend
    st.markdown("""
<div class='legend-wrap'>
  <div class='legend-row'><div class='legend-dot' style='background:#1e8449;border:1px solid #2ecc71;'></div>Mastered<span class='legend-thr'>&nbsp;≥70%</span></div>
  <div class='legend-row'><div class='legend-dot' style='background:#9a6700;border:1px solid #f39c12;'></div>In Progress<span class='legend-thr'>&nbsp;40–69%</span></div>
  <div class='legend-row'><div class='legend-dot' style='background:#7b241c;border:1px solid #e74c3c;'></div>Not Started<span class='legend-thr'>&nbsp;&lt;40%</span></div>
  <div class='legend-row'><div class='legend-dot' style='background:#2980b9;border:1px solid #5dade2;'></div>Your Path</div>
</div>""", unsafe_allow_html=True)

    with st.expander("How to read this graph"):
        st.markdown("""
**% on each node** — the BKT estimate: probability (0–100%) that you have genuinely mastered that concept, inferred from your quiz answers.

**Why % changes after each answer** — BKT applies a Bayesian update. A correct answer raises mastery (discounting guesses); a wrong answer lowers it (discounting slips). The learn-rate T adds a small upward nudge regardless, because attempting a problem itself has learning value.

**Arrows** — A → B means *A is a prerequisite of B*. Graph flows left → right.

**Blue path** — Agent 2 finds all prerequisites of your goal, orders them topologically, and keeps only those below the 70% mastery threshold.

**Why the path sometimes doesn't change** — the router only re-routes when a concept crosses the 70% threshold. Small probability shifts below the threshold leave the path identical.
""")

# Right column — live trace and activity log

with right:
    st.markdown("<div class='label'>🔬 Live Model Reasoning</div>",
                unsafe_allow_html=True)

    exp = st.session_state.last_explanation

    if exp is None:
        st.markdown(
            "<div class='trace-empty'>Answer a question on the left<br>to see live BKT calculations<br>and path decisions here.</div>",
            unsafe_allow_html=True,
        )
    else:
        c      = exp["concept"]
        ok     = exp["correct"]
        old_m  = exp["old_m"]
        post   = exp["posterior"]
        new_m  = exp["new_m"]
        numer  = exp["numer"]
        denom  = exp["denom"]
        lbl    = exp["label"]
        T      = 0.20

        ans_cls  = "trace-answer-ok"  if ok else "trace-answer-bad"
        ans_icon = "✓ Correct" if ok else "✗ Incorrect"

        # BKT formula lines
        sign = "correct" if ok else "incorrect"
        formula = (
            f"Prior mastery L     = {old_m:.3f}  ({old_m:.0%})\n\n"
            f"Bayesian update ({sign}):\n"
            f"  P(L|answer) = {lbl} / denominator\n"
            f"             = {numer:.4f} / {denom:.4f}\n"
            f"             = {post:.3f}  ({post:.0%})\n\n"
            f"After learn-rate T  = {T}:\n"
            f"  L' = {post:.3f} + {T} × (1 − {post:.3f})\n"
            f"     = {post:.3f} + {T*(1-post):.3f}\n"
            f"     = {new_m:.3f}  ({new_m:.0%})"
        )

        # Path Router verdict
        if exp["path_changed"]:
            old_str  = " → ".join(exp["old_path"]) if exp["old_path"] else "—"
            new_str  = " → ".join(exp["new_path"]) if exp["new_path"] else f"'{goal}' reachable!"
            verdict_cls  = "verdict-changed"
            verdict_html = (
                f"<div class='{verdict_cls}'>"
                f"✔ Path updated — {c} crossed 70% threshold<br>"
                f"<span style='color:#6b7280;font-size:0.73rem;'>"
                f"Before: {old_str}<br>After:&nbsp;&nbsp;{new_str}"
                f"</span></div>"
            )
        else:
            verdict_cls  = "verdict-unchanged"
            verdict_html = (
                f"<div class='{verdict_cls}'>"
                f"— No change — {c} at {new_m:.0%}, below 70% threshold<br>"
                f"<span style='font-size:0.73rem;'>Path re-evaluated and confirmed</span>"
                f"</div>"
            )

        st.markdown(f"""
<div class='trace-card'>
  <div class='trace-head'>Last answer{c}</div>
  <div class='{ans_cls}'>{ans_icon}</div>
  <div class='trace-section'>Agent 1 — BKT Update</div>
  <div class='trace-formula'>{formula}</div>
  <div class='trace-section trace-section-router'>Agent 2 — Path Router</div>
  {verdict_html}
</div>""", unsafe_allow_html=True)

    # Activity log

    if st.session_state.agent_log:
        st.markdown("<div class='label' style='margin-top:20px;'>Activity log</div>",
                    unsafe_allow_html=True)
        log_html = "<div class='log-scroll'>"
        for e in st.session_state.agent_log:
            if e["type"] == "bkt":
                css = "log-entry log-bkt"
            elif e["changed"]:
                css = "log-entry log-router-change"
            else:
                css = "log-entry log-router"
            log_html += (
                f"<div class='{css}'>"
                f"<div class='log-agent-name'>{e['name']}</div>"
                f"<div class='log-action'>{e['action']}</div>"
                f"<div class='log-result'>{e['result']}</div>"
                f"</div>"
            )
        log_html += "</div>"
        st.markdown(log_html, unsafe_allow_html=True)
