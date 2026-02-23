import streamlit as st
import os
import subprocess
import uuid

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
.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #4B8BBE;
    text-align: center;
}
.sub-text {
    text-align: center;
    color: #A0A0A0;
    margin-bottom: 30px;
}
.section-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 25px;
    border: 1px solid #1F2937;
}
.step-title {
    font-size: 20px;
    font-weight: 600;
    color: #60A5FA;
    margin-bottom: 10px;
}
.stButton>button {
    border-radius: 8px;
    background-color: #2563EB;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎬 AI Video Translation Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Upload → Extract → Transcribe → Translate → Generate → Merge</div>', unsafe_allow_html=True)

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
# STEP 1 — UPLOAD
# -------------------------------------------------

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="step-title">Step 1: Upload Video</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload MP4 Video", type=["mp4"])

if uploaded_file and not st.session_state.uploaded:

    unique_id = str(uuid.uuid4())
    input_path = os.path.join("input_videos", f"{unique_id}.mp4")

    # Clean pipeline artifacts
    for folder in folders[1:]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.session_state.video_path = input_path
    st.session_state.uploaded = True

if st.session_state.uploaded:
    st.success("Video uploaded successfully.")
    st.video(st.session_state.video_path, width=350)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 2 — EXTRACT AUDIO
# -------------------------------------------------

if st.session_state.uploaded:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 2: Extract Audio</div>', unsafe_allow_html=True)

    if not st.session_state.audio_done:
        if st.button("Extract Audio"):
            subprocess.run(
                ["python", "extract_audio.py", st.session_state.video_path],
                check=True
            )
            st.session_state.audio_done = True

    if st.session_state.audio_done:
        st.success("Audio extracted.")
        st.audio("extracted_audio/audio.wav")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 3 — SPEECH TO TEXT
# -------------------------------------------------

if st.session_state.audio_done:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 3: Speech to Text</div>', unsafe_allow_html=True)

    if not st.session_state.transcript_done:
        if st.button("Generate Transcript"):
            subprocess.run(["python", "speech_to_text.py"], check=True)
            st.session_state.transcript_done = True

    if st.session_state.transcript_done:
        with open("transcripts/transcript.txt", "r", encoding="utf-8") as f:
            st.text_area("Transcript", f.read(), height=180)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 4 — TRANSLATE
# -------------------------------------------------

if st.session_state.transcript_done:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 4: Translate</div>', unsafe_allow_html=True)

    language_dict = {
        "Hindi": "hi",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Tamil": "ta"
    }

    selected_lang = st.selectbox("Choose Target Language", list(language_dict.keys()))

    if not st.session_state.translated_done:
        if st.button("Translate Text"):
            subprocess.run(
                ["python", "translate_text.py", language_dict[selected_lang]],
                check=True
            )
            st.session_state.language = language_dict[selected_lang]
            st.session_state.translated_done = True

    if st.session_state.translated_done:
        with open("translated_text/translated.txt", "r", encoding="utf-8") as f:
            st.text_area("Translated Text", f.read(), height=180)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 5 — TEXT TO SPEECH
# -------------------------------------------------

if st.session_state.translated_done:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 5: Generate Speech</div>', unsafe_allow_html=True)

    if not st.session_state.speech_done:
        if st.button("Generate Audio"):
            subprocess.run(
                ["python", "text_to_speech.py", st.session_state.language],
                check=True
            )
            st.session_state.speech_done = True

    if st.session_state.speech_done:
        st.audio("generated_audio/translated.wav")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 6 — MERGE
# -------------------------------------------------

if st.session_state.speech_done:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 6: Merge Audio with Video</div>', unsafe_allow_html=True)

    if not st.session_state.merged_done:
        if st.button("Merge Now"):

            result = subprocess.run(
                ["python", "sync_audio_video.py", st.session_state.video_path],
                capture_output=True,
                text=True,
                check=True
            )

            output_path = result.stdout.strip()
            st.session_state.final_video = output_path
            st.session_state.merged_done = True

    if st.session_state.merged_done:
        st.success("Final video created successfully.")

        # Maintain proper size for 9:16 video
        st.video(st.session_state.final_video, width=350)

        with open(st.session_state.final_video, "rb") as f:
            st.download_button(
                "Download Final Video",
                f,
                file_name="translated_video.mp4"
            )

    st.markdown('</div>', unsafe_allow_html=True)