import streamlit as st
import os
import subprocess
import uuid
import sys

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Multilingual Video Translator",
    page_icon="🎬",
    layout="centered"
)

# -------------------------------------------------
# CUSTOM STYLING
# -------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'SF Pro Display', sans-serif;
}

.stApp {
    background: #04080f;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(37, 99, 235, 0.12), transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(16, 185, 129, 0.06), transparent);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 760px; }

/* ── HEADER ── */
.app-header {
    text-align: center;
    padding: 48px 0 36px;
    position: relative;
}
.app-header .badge {
    display: inline-block;
    background: rgba(37,99,235,0.15);
    border: 1px solid rgba(37,99,235,0.4);
    color: #60a5fa;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.app-header h1 {
    font-size: clamp(28px, 5vw, 46px);
    font-weight: 800;
    line-height: 1.1;
    color: #f0f6ff;
    margin: 0 0 14px;
    letter-spacing: -0.02em;
}
.app-header h1 span {
    background: linear-gradient(135deg, #3b82f6, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.app-header .subtitle {
    color: #4b5e7a;
    font-size: 15px;
    letter-spacing: 0.04em;
}

/* ── PIPELINE BAR ── */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 0 0 44px;
    flex-wrap: nowrap;
    overflow-x: auto;
    padding: 4px 0;
}
.pip-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    min-width: 52px;
}
.pip-dot {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 2px solid #1e2d42;
    background: #0b1523;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
}
.pip-dot.active {
    border-color: #3b82f6;
    background: rgba(59,130,246,0.15);
    box-shadow: 0 0 14px rgba(59,130,246,0.4);
}
.pip-dot.done {
    border-color: #10b981;
    background: rgba(16,185,129,0.15);
    box-shadow: 0 0 14px rgba(16,185,129,0.35);
}
.pip-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #2d4056;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    text-align: center;
    white-space: nowrap;
}
.pip-label.active { color: #60a5fa; }
.pip-label.done   { color: #34d399; }
.pip-line {
    height: 2px;
    width: 28px;
    background: #0f1e2e;
    margin-bottom: 18px;
    flex-shrink: 0;
}
.pip-line.done { background: linear-gradient(to right, #10b981, #3b82f6); }

/* ── STEP CARDS ── */
.step-card {
    background: linear-gradient(145deg, #080f1a, #0c1525);
    border: 1px solid #0f1e33;
    border-radius: 18px;
    padding: 28px 30px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, #1e40af, transparent);
    opacity: 0.6;
}
.step-card.complete::before {
    background: linear-gradient(to right, transparent, #065f46, transparent);
}
.step-card .corner-num {
    position: absolute;
    top: 18px; right: 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #1a2d47;
    letter-spacing: 0.1em;
}
.step-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
}
.step-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: rgba(37,99,235,0.12);
    border: 1px solid rgba(37,99,235,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.step-icon.green {
    background: rgba(16,185,129,0.1);
    border-color: rgba(16,185,129,0.25);
}
.step-title-text {
    font-size: 18px;
    font-weight: 700;
    color: #d1e3f8;
    letter-spacing: -0.01em;
}
.step-desc {
    font-size: 12px;
    color: #2d4a66;
    margin-top: 2px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.03em;
}

/* ── SUCCESS STATE ── */
.success-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34d399;
    padding: 7px 16px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 16px;
}

/* ── DIVIDER ── */
.section-divider {
    border: none;
    border-top: 1px solid #0c1a2a;
    margin: 32px 0;
}

/* ── Streamlit element overrides ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.04em !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    color: #e0f0ff !important;
    border: 1px solid rgba(96,165,250,0.2) !important;
    box-shadow: 0 0 20px rgba(37,99,235,0.2), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    box-shadow: 0 0 30px rgba(59,130,246,0.35) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Download button */
.stDownloadButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    background: linear-gradient(135deg, #065f46, #047857) !important;
    color: #6ee7b7 !important;
    border: 1px solid rgba(52,211,153,0.2) !important;
    box-shadow: 0 0 20px rgba(16,185,129,0.2) !important;
    padding: 10px 28px !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 30px rgba(16,185,129,0.35) !important;
    transform: translateY(-1px) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(8,16,30,0.8) !important;
    border: 1px dashed #1a2d47 !important;
    border-radius: 14px !important;
    padding: 8px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #2563eb !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #2d4a66 !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #080f1a !important;
    border: 1px solid #0f1e33 !important;
    border-radius: 10px !important;
    color: #94b8d8 !important;
    font-family: 'Syne', sans-serif !important;
}

/* Text area */
.stTextArea > div > div > textarea {
    background: #060d18 !important;
    border: 1px solid #0f1e33 !important;
    border-radius: 10px !important;
    color: #7fb8d8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}

/* Success/info message boxes */
.stSuccess {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 10px !important;
    color: #34d399 !important;
}

/* Video player */
video {
    border-radius: 12px !important;
    border: 1px solid #0f1e33 !important;
}

/* Audio player */
audio {
    width: 100%;
    border-radius: 8px;
    filter: invert(0.85) hue-rotate(180deg);
    opacity: 0.85;
}

/* Label text */
.stTextArea label, .stSelectbox label, .stFileUploader label {
    color: #2d4a66 !important;
    font-size: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #040810; }
::-webkit-scrollbar-thumb { background: #1a2d47; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown("""
<div class="app-header">
    <div class="badge">✦ AI-Powered Pipeline</div>
    <h1>Multilingual Video<br><span>Translation System</span></h1>
    <p class="subtitle">Upload → Transcribe → Translate → Dub → Export</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CREATE FOLDERS
# -------------------------------------------------

folders = [
    "input_videos",
    "extracted_audio",
    "transcripts",
    "translated_text",
    "generated_audio",
    "output_videos"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------

states = [
    "uploaded",
    "audio_done",
    "transcript_done",
    "translated_done",
    "speech_done",
    "merged_done"
]

for s in states:
    if s not in st.session_state:
        st.session_state[s] = False

# -------------------------------------------------
# PIPELINE PROGRESS BAR
# -------------------------------------------------

steps_meta = [
    ("📤", "Upload"),
    ("🎧", "Extract"),
    ("📝", "Transcribe"),
    ("🌍", "Translate"),
    ("🔊", "Synthesize"),
    ("🎬", "Merge"),
]

completed = sum([
    st.session_state.uploaded,
    st.session_state.audio_done,
    st.session_state.transcript_done,
    st.session_state.translated_done,
    st.session_state.speech_done,
    st.session_state.merged_done,
])

pipeline_html = '<div class="pipeline">'
for i, (icon, label) in enumerate(steps_meta):
    if i < completed:
        dot_cls   = "pip-dot done"
        label_cls = "pip-label done"
        dot_inner = "✓"
    elif i == completed:
        dot_cls   = "pip-dot active"
        label_cls = "pip-label active"
        dot_inner = icon
    else:
        dot_cls   = "pip-dot"
        label_cls = "pip-label"
        dot_inner = icon

    pipeline_html += f"""
    <div class="pip-node">
        <div class="{dot_cls}">{dot_inner}</div>
        <span class="{label_cls}">{label}</span>
    </div>"""

    if i < len(steps_meta) - 1:
        line_cls = "pip-line done" if i < completed - 1 else "pip-line"
        pipeline_html += f'<div class="{line_cls}"></div>'

pipeline_html += '</div>'
st.markdown(pipeline_html, unsafe_allow_html=True)

# -------------------------------------------------
# STEP 1 — UPLOAD
# -------------------------------------------------

card_cls = "step-card complete" if st.session_state.uploaded else "step-card"
st.markdown(f"""
<div class="{card_cls}">
    <span class="corner-num">01 / 06</span>
    <div class="step-header">
        <div class="step-icon">📤</div>
        <div>
            <div class="step-title-text">Upload Video</div>
            <div class="step-desc">Accepts .mp4 format</div>
        </div>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Select your video file", type=["mp4"], label_visibility="collapsed")

if uploaded_file and not st.session_state.uploaded:
    unique_id = str(uuid.uuid4())
    input_path = os.path.join("input_videos", f"{unique_id}.mp4")

    for folder in folders[1:]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.session_state.video_path = input_path
    st.session_state.uploaded = True

if st.session_state.uploaded:
    st.markdown('<div class="success-pill">✓ &nbsp; Video uploaded successfully</div>', unsafe_allow_html=True)
    st.video(st.session_state.video_path, width=350)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 2 — EXTRACT AUDIO
# -------------------------------------------------

if st.session_state.uploaded:
    card_cls = "step-card complete" if st.session_state.audio_done else "step-card"
    st.markdown(f"""
    <div class="{card_cls}">
        <span class="corner-num">02 / 06</span>
        <div class="step-header">
            <div class="step-icon">🎧</div>
            <div>
                <div class="step-title-text">Extract Audio</div>
                <div class="step-desc">FFmpeg · WAV · 16kHz mono</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.audio_done:
        if st.button("Extract Audio Track"):
            with st.spinner("Extracting audio with FFmpeg..."):
                subprocess.run(
                    ["python3", "extract_audio.py", st.session_state.video_path],
                    check=True
                )
            st.session_state.audio_done = True
            st.rerun()

    if st.session_state.audio_done:
        st.markdown('<div class="success-pill">✓ &nbsp; Audio extracted successfully</div>', unsafe_allow_html=True)
        st.audio("extracted_audio/audio.wav")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 3 — SPEECH TO TEXT
# -------------------------------------------------

if st.session_state.audio_done:
    card_cls = "step-card complete" if st.session_state.transcript_done else "step-card"
    st.markdown(f"""
    <div class="{card_cls}">
        <span class="corner-num">03 / 06</span>
        <div class="step-header">
            <div class="step-icon">📝</div>
            <div>
                <div class="step-title-text">Speech to Text</div>
                <div class="step-desc">OpenAI Whisper · base model</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.transcript_done:
        if st.button("Generate Transcript"):
            with st.spinner("Transcribing with Whisper — this may take a moment..."):
                subprocess.run(["python3", "speech_to_text.py"], check=True)
            st.session_state.transcript_done = True
            st.rerun()

    if st.session_state.transcript_done:
        st.markdown('<div class="success-pill">✓ &nbsp; Transcript generated</div>', unsafe_allow_html=True)
        with open("transcripts/transcript.txt", "r", encoding="utf-8") as f:
            st.text_area("Original Transcript", f.read(), height=160)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 4 — TRANSLATE
# -------------------------------------------------

if st.session_state.transcript_done:
    card_cls = "step-card complete" if st.session_state.translated_done else "step-card"
    st.markdown(f"""
    <div class="{card_cls}">
        <span class="corner-num">04 / 06</span>
        <div class="step-header">
            <div class="step-icon">🌍</div>
            <div>
                <div class="step-title-text">Translate</div>
                <div class="step-desc">Google Translate API · 5 languages</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    language_dict = {
        "🇮🇳  Hindi":   "hi",
        "🇫🇷  French":  "fr",
        "🇪🇸  Spanish": "es",
        "🇩🇪  German":  "de",
        "🇮🇳  Tamil":   "ta"
    }

    selected_lang = st.selectbox("Target Language", list(language_dict.keys()))

    if not st.session_state.translated_done:
        if st.button("Translate Text"):
            with st.spinner("Translating..."):
                subprocess.run(
                    ["python3", "translate_text.py", language_dict[selected_lang]],
                    check=True
                )
            st.session_state.language = language_dict[selected_lang]
            st.session_state.translated_done = True
            st.rerun()

    if st.session_state.translated_done:
        st.markdown('<div class="success-pill">✓ &nbsp; Translation complete</div>', unsafe_allow_html=True)
        with open("translated_text/translated.txt", "r", encoding="utf-8") as f:
            st.text_area("Translated Text", f.read(), height=160)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 5 — TEXT TO SPEECH
# -------------------------------------------------

if st.session_state.translated_done:
    card_cls = "step-card complete" if st.session_state.speech_done else "step-card"
    st.markdown(f"""
    <div class="{card_cls}">
        <span class="corner-num">05 / 06</span>
        <div class="step-header">
            <div class="step-icon">🔊</div>
            <div>
                <div class="step-title-text">Generate Speech</div>
                <div class="step-desc">gTTS · duration-matched to original</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.speech_done:
        if st.button("Generate Audio"):
            with st.spinner("Synthesizing speech and syncing duration..."):
                subprocess.run(
                    ["python3", "text_to_speech.py", st.session_state.language],
                    check=True
                )
            st.session_state.speech_done = True
            st.rerun()

    if st.session_state.speech_done:
        st.markdown('<div class="success-pill">✓ &nbsp; Audio generated &amp; synced</div>', unsafe_allow_html=True)
        st.audio("generated_audio/translated.wav")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 6 — MERGE
# -------------------------------------------------

if st.session_state.speech_done:
    card_cls = "step-card complete" if st.session_state.merged_done else "step-card"
    st.markdown(f"""
    <div class="{card_cls}">
        <span class="corner-num">06 / 06</span>
        <div class="step-header">
            <div class="step-icon green">🎬</div>
            <div>
                <div class="step-title-text">Merge &amp; Export</div>
                <div class="step-desc">FFmpeg · AAC audio · MP4 output</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.merged_done:
        if st.button("Merge Audio into Video"):
            with st.spinner("Merging translated audio with video..."):
                result = subprocess.run(
                    ["python3", "sync_audio_video.py", st.session_state.video_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
            output_path = result.stdout.strip()
            st.session_state.final_video = output_path
            st.session_state.merged_done = True
            st.rerun()

    if st.session_state.merged_done:
        st.markdown('<div class="success-pill">✓ &nbsp; Final video ready — pipeline complete!</div>', unsafe_allow_html=True)
        st.video(st.session_state.final_video, width=350)

        with open(st.session_state.final_video, "rb") as f:
            st.download_button(
                "⬇  Download Translated Video",
                f,
                file_name="translated_video.mp4"
            )

    st.markdown('</div>', unsafe_allow_html=True)