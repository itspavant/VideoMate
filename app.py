"""
VideoMate — Streamlit UI
A "post-production suite" interface: a console sidebar for capture controls,
a clapperboard "slate" that reveals session metadata once a run completes,
and an interview-style transcript for the RAG chat.

Wraps the existing pipeline (utils.audio_processor, core.transcriber,
core.summarizer, core.extractor, core.rag_engine) with zero backend changes.

Run with:  streamlit run app.py
"""

import os
import tempfile
import datetime as dt

import streamlit as st
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

st.set_page_config(page_title="VideoMate", page_icon="", layout="wide")

# ──────────────────────────────────────────────────────────────────────────
# Design system — "post-production console"
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap');

:root{
  --stage:#101511; --panel:#171d19; --panel-2:#1d2420; --line:#2c352e;
  --paper:#f2ece0; --ink:#21201b; --ink-soft:#5c584c;
  --signal:#ff5a36; --brass:#c9a24b; --ok:#4caf6d; --muted:#7c8a80;
}

html, body, [class*="css"]{ font-family:'IBM Plex Mono', monospace; }
.stApp{ background: var(--stage) !important; }
[data-testid="stSidebar"]{ background: var(--panel) !important; border-right:1px solid var(--line) !important; }
[data-testid="stSidebar"] *{ color: var(--paper) !important; }
h1,h2,h3{ font-family:'Space Grotesk', sans-serif !important; }

/* wordmark */
.wordmark{ display:flex; align-items:baseline; gap:.6rem; margin-bottom:.1rem; }
.wordmark .mark{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:2.1rem; color:var(--paper); letter-spacing:.01em; }
.wordmark .tag{ font-size:.68rem; color:var(--muted); letter-spacing:.22em; text-transform:uppercase; }
.rule{ height:1px; background:var(--line); margin:.9rem 0 1.4rem 0; }

/* sidebar console */
.panel-eyebrow{ font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; color:var(--brass) !important; margin: .2rem 0 .5rem 0; }
.led-row{ display:flex; align-items:center; gap:.55rem; padding:.4rem 0; border-bottom:1px solid var(--line); font-size:.72rem; }
.led{ width:8px; height:8px; border-radius:50%; flex-shrink:0; background:#3a453d; box-shadow:none; }
.led.on{ background:var(--ok); box-shadow:0 0 6px var(--ok); }
.led.active{ background:var(--signal); box-shadow:0 0 6px var(--signal); animation:blink 1s infinite; }
@keyframes blink{ 50%{opacity:.35;} }

.stTextInput>div>div>input, .stSelectbox>div>div{
  background: var(--panel-2) !important; border:1px solid var(--line) !important;
  border-radius:4px !important; color: var(--paper) !important; font-family:'IBM Plex Mono',monospace !important;
}
.stButton>button{
  background: var(--signal) !important; color:#171000 !important; border:none !important;
  border-radius:4px !important; font-family:'Space Grotesk',sans-serif !important; font-weight:700 !important;
  letter-spacing:.08em !important; text-transform:uppercase !important; padding:.6rem 1rem !important;
}
.stButton>button:hover{ filter:brightness(1.08); }
.stButton>button[kind="secondary"]{ background:var(--panel-2) !important; color:var(--paper) !important; border:1px solid var(--line) !important; }

/* segmented language toggle */
div[role="radiogroup"]{ display:flex; gap:0; border:1px solid var(--line); border-radius:4px; overflow:hidden; width:fit-content; }
div[role="radiogroup"] label{ margin:0 !important; padding:.35rem .9rem !important; background:var(--panel-2); }
div[role="radiogroup"] label[data-checked="true"]{ background:var(--signal) !important; }

/* the slate — signature element */
.slate{ background:var(--paper); border-radius:6px; overflow:hidden; margin:1.2rem 0 1.6rem 0;
  box-shadow:0 18px 40px -20px rgba(0,0,0,.6); }
.slate-stripes{ height:22px;
  background: repeating-linear-gradient(-45deg, #1a1a1a 0 18px, #f2ece0 18px 36px); }
.slate-body{ padding:1.3rem 1.6rem 1.5rem 1.6rem; }
.slate-row{ display:flex; flex-wrap:wrap; gap:2.2rem; margin-bottom:.7rem; }
.slate-field .k{ font-size:.6rem; letter-spacing:.18em; text-transform:uppercase; color:var(--ink-soft); }
.slate-field .v{ font-family:'Space Grotesk',sans-serif; font-weight:700; color:var(--ink); font-size:1rem; }
.slate-title{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.7rem; color:var(--ink); line-height:1.15; }

/* reading cards (paper) */
.paper-card{ background:var(--paper); color:var(--ink); border-radius:6px; padding:1.3rem 1.5rem; height:100%; }
.paper-card .eyebrow{ font-family:'IBM Plex Mono',monospace; font-size:.62rem; letter-spacing:.18em; text-transform:uppercase; color:var(--ink-soft); margin-bottom:.6rem; }
.paper-card .body{ font-family:'Source Serif 4',serif; font-size:.98rem; line-height:1.7; white-space:pre-wrap; }

/* cue cards row */
.cue{ background:var(--panel-2); border:1px solid var(--line); border-left:3px solid var(--brass);
  border-radius:4px; padding:1.1rem 1.2rem; height:100%; }
.cue .eyebrow{ font-size:.62rem; letter-spacing:.18em; text-transform:uppercase; color:var(--brass); margin-bottom:.55rem; }
.cue .body{ font-family:'Source Serif 4',serif; color:var(--paper); font-size:.92rem; line-height:1.65; white-space:pre-wrap; }

/* transcript reel */
.tape{ background:var(--panel-2); border:1px solid var(--line); border-radius:6px; padding:1.1rem 1.3rem;
  max-height:340px; overflow-y:auto; font-family:'Source Serif 4',serif; color:var(--paper); line-height:1.75; white-space:pre-wrap; }

/* interview-style chat */
.line{ display:flex; gap:.7rem; margin-bottom:.85rem; align-items:baseline; }
.line .tc{ font-size:.68rem; color:var(--muted); width:64px; flex-shrink:0; }
.line .who{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:.72rem; width:34px; flex-shrink:0; }
.line.you .who{ color:var(--brass); }
.line.ai .who{ color:var(--signal); }
.line .txt{ font-family:'Source Serif 4',serif; font-size:.95rem; color:var(--paper); line-height:1.6; }
.transcript-shell{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:1.2rem 1.4rem; }

.empty{ text-align:center; padding:4rem 1rem; color:var(--muted); }
.empty .big{ font-size:2.4rem; margin-bottom:.4rem; }
[data-testid="stMarkdownContainer"] p{ color:var(--paper); }
::-webkit-scrollbar{ width:6px; } ::-webkit-scrollbar-thumb{ background:var(--line); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────────────────────────────────
for key, default in {
    "result": None, "chat_history": [], "steps": {}, "run_meta": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

STEP_ORDER = [
    ("audio", "Ingest & chunk"),
    ("transcript", "Transcribe"),
    ("title", "Title"),
    ("summary", "Summarize"),
    ("extract", "Extract"),
    ("rag", "Build RAG index"),
]


def set_step(key, state):
    st.session_state.steps[key] = state


def save_uploaded_file(uploaded_file) -> str:
    tmp_path = os.path.join(tempfile.gettempdir(), f"ai_video_assistant_{uploaded_file.name}")
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return tmp_path


def fmt_time():
    return dt.datetime.now().strftime("%H:%M:%S")


# ──────────────────────────────────────────────────────────────────────────
# Sidebar — capture console
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="wordmark"><span class="mark">CONSOLE</span></div>'
                '<div class="tag">Session Intelligence Console</div>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-eyebrow">Source</div>', unsafe_allow_html=True)
    mode = st.radio("mode", ["Link / path", "Upload"], label_visibility="collapsed")
    source = None
    if mode == "Link / path":
        source = st.text_input("src", placeholder="youtube.com/watch?v=... or /path/file.mp4", label_visibility="collapsed")
    else:
        up = st.file_uploader("upload", type=["mp4", "mp3", "wav", "m4a", "mov", "mkv", "webm"], label_visibility="collapsed")
        if up is not None:
            source = save_uploaded_file(up)
            st.caption(f"◉ staged: {up.name}")

    st.markdown('<div class="panel-eyebrow" style="margin-top:1.1rem">Language</div>', unsafe_allow_html=True)
    language = st.radio("lang", ["english", "hinglish"], label_visibility="collapsed", horizontal=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    run_clicked = st.button("▶  Run session", use_container_width=True, disabled=not source)

    if st.session_state.result:
        if st.button("↺  Clear session", use_container_width=True, type="secondary"):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.session_state.steps = {}
            st.session_state.run_meta = None
            st.rerun()

    if st.session_state.steps:
        st.markdown('<div class="rule"></div><div class="panel-eyebrow">Signal chain</div>', unsafe_allow_html=True)
        rows = ""
        for key, label in STEP_ORDER:
            s = st.session_state.steps.get(key, "pending")
            css = "on" if s == "done" else ("active" if s == "active" else "")
            rows += f'<div class="led-row"><div class="led {css}"></div><span>{label}</span></div>'
        st.markdown(rows, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="wordmark"><span class="mark">VideoMate</span></div>'
            '<div class="tag">Transcribe · Summarize · Interrogate the recording</div>'
            '<div class="rule"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Run pipeline
# ──────────────────────────────────────────────────────────────────────────
if run_clicked and source:
    st.session_state.steps = {}
    st.session_state.chat_history = []
    status = st.empty()
    try:
        set_step("audio", "active")
        status.info("Ingesting source…")
        chunks = process_input(source)
        set_step("audio", "done")

        set_step("transcript", "active")
        status.info("Transcribing…")
        transcript = transcribe_all(chunks, language=language)
        set_step("transcript", "done")

        set_step("title", "active")
        title = generate_title(transcript=transcript)
        set_step("title", "done")

        set_step("summary", "active")
        status.info("Summarizing…")
        summary = summarize(transcript=transcript)
        set_step("summary", "done")

        set_step("extract", "active")
        status.info("Extracting action items, decisions, questions…")
        action_items = extract_action_items(transcript=transcript)
        decisions = extract_key_decisions(transcript=transcript)
        questions = extract_questions(transcript=transcript)
        set_step("extract", "done")

        set_step("rag", "active")
        status.info("Building RAG index…")
        rag_chain = build_rag_chain(transcript=transcript)
        set_step("rag", "done")

        st.session_state.result = {
            "title": title, "transcript": transcript, "summary": summary,
            "action_items": action_items, "key_decisions": decisions,
            "open_questions": questions, "rag_chain": rag_chain,
        }
        word_count = len(transcript.split())
        st.session_state.run_meta = {
            "logged_at": dt.datetime.now().strftime("%d %b %Y, %H:%M"),
            "language": language,
            "words": f"{word_count:,}",
            "est_read": f"{max(1, word_count // 200)} min",
        }
        status.empty()
        st.rerun()
    except Exception as e:
        for k, _ in STEP_ORDER:
            if st.session_state.steps.get(k) == "active":
                st.session_state.steps[k] = "pending"
        status.error(f"Session failed: {e}")

# ──────────────────────────────────────────────────────────────────────────
# Results
# ──────────────────────────────────────────────────────────────────────────
result = st.session_state.result

if not result:
    st.markdown("""
    <div class="empty">
        <div class="big">🎞️</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;color:#f2ece0;">No session logged yet</div>
        <div style="max-width:380px;margin:.4rem auto 0 auto;">Load a link, path, or file in the console on the left, then press
        <strong style="color:#ff5a36;">Run session</strong>.</div>
    </div>""", unsafe_allow_html=True)
else:
    meta = st.session_state.run_meta or {}
    st.markdown(f"""
    <div class="slate">
        <div class="slate-stripes"></div>
        <div class="slate-body">
            <div class="slate-title">{result['title']}</div>
            <div class="slate-row" style="margin-top:.9rem">
                <div class="slate-field"><div class="k">Logged</div><div class="v">{meta.get('logged_at','—')}</div></div>
                <div class="slate-field"><div class="k">Language</div><div class="v">{meta.get('language','—')}</div></div>
                <div class="slate-field"><div class="k">Word count</div><div class="v">{meta.get('words','—')}</div></div>
                <div class="slate-field"><div class="k">Read time</div><div class="v">{meta.get('est_read','—')}</div></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown(f'<div class="paper-card"><div class="eyebrow">Summary</div>'
                    f'<div class="body">{result["summary"]}</div></div>', unsafe_allow_html=True)
    with col2:
        with st.expander("Full transcript", expanded=False):
            st.markdown(f'<div class="tape">{result["transcript"]}</div>', unsafe_allow_html=True)
            st.download_button("Download .txt", data=result["transcript"],
                                file_name=f"{result['title']}_transcript.txt", mime="text/plain")

    st.write("")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(f'<div class="cue"><div class="eyebrow">✅ Action items</div>'
                    f'<div class="body">{result["action_items"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="cue"><div class="eyebrow">🔑 Key decisions</div>'
                    f'<div class="body">{result["key_decisions"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="cue"><div class="eyebrow">❓ Open questions</div>'
                    f'<div class="body">{result["open_questions"]}</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-eyebrow" style="color:#c9a24b !important;">Interview transcript — chat with the recording</div>',
                unsafe_allow_html=True)

    transcript_html = '<div class="transcript-shell">'
    if not st.session_state.chat_history:
        transcript_html += '<span style="color:#7c8a80;font-size:.85rem;">Ask a question below to begin the interview.</span>'
    for msg in st.session_state.chat_history:
        cls = "you" if msg["role"] == "user" else "ai"
        who = "YOU" if msg["role"] == "user" else "AI"
        transcript_html += (f'<div class="line {cls}"><span class="tc">[{msg["tc"]}]</span>'
                            f'<span class="who">{who}</span><span class="txt">{msg["content"]}</span></div>')
    transcript_html += '</div>'
    st.markdown(transcript_html, unsafe_allow_html=True)

    q_col, b_col = st.columns([5, 1], gap="small")
    with q_col:
        question = st.text_input("q", placeholder="What did we decide about the launch date?", label_visibility="collapsed")
    with b_col:
        ask_clicked = st.button("Ask →", use_container_width=True)

    if ask_clicked and question.strip():
        with st.spinner("Rewinding the tape…"):
            answer = ask_question(result["rag_chain"], question.strip())
        st.session_state.chat_history.append({"role": "user", "content": question.strip(), "tc": fmt_time()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "tc": fmt_time()})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear interview", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()