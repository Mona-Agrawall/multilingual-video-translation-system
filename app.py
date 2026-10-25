"""Streamlit app that walks the user through translating a video, one step at a time."""

import uuid
from dataclasses import dataclass
from pathlib import Path

import streamlit as st

from pipeline import (
    extract_audio,
    merge_audio_into_video,
    synthesize_speech,
    transcribe_audio,
    translate_text,
)
from ui.components import (
    load_styles,
    render_footer,
    render_hero,
    render_info_panel,
    render_navbar,
    render_progress_tracker,
    render_step_card,
    render_success_badge,
)

# Every upload gets its own folder here, so runs never overwrite each other.
WORKSPACE_DIR = Path(__file__).parent / "workspace"

# Display name -> language code used by Google Translate and gTTS
LANGUAGES = {
    "🇮🇳 Hindi": "hi",
    "🇫🇷 French": "fr",
    "🇪🇸 Spanish": "es",
    "🇩🇪 German": "de",
    "🇮🇳 Tamil": "ta",
}


@dataclass(frozen=True)
class Step:
    done_flag: str  # session state key that becomes True when the step finishes
    icon: str
    label: str      # short name shown in the progress tracker
    title: str
    subtitle: str


STEPS = [
    Step("uploaded", "📤", "Upload", "Upload Video", "MP4 · up to 200 MB"),
    Step("audio_extracted", "🎧", "Extract", "Extract Audio", "FFmpeg · WAV · 16 kHz mono"),
    Step("transcribed", "📝", "Transcribe", "Speech to Text", "OpenAI Whisper · base model"),
    Step("translated", "🌍", "Translate", "Translate Text", f"Google Translate API · {len(LANGUAGES)} languages"),
    Step("speech_generated", "🔊", "Synthesize", "Generate Speech", "gTTS · duration-matched to original"),
    Step("merged", "🎬", "Merge", "Merge &amp; Export", "FFmpeg · AAC audio · MP4 output"),
]


def init_session_state():
    for step in STEPS:
        st.session_state.setdefault(step.done_flag, False)
    for key in ["run_dir", "transcript", "translation", "language"]:
        st.session_state.setdefault(key, None)


def run_file(filename):
    """Path of a file inside the current upload's workspace folder."""
    return st.session_state.run_dir / filename


def show_step_card(step_number):
    step = STEPS[step_number - 1]
    render_step_card(step, step_number, len(STEPS), done=st.session_state[step.done_flag])


# -------------------------------------------------
# Page setup
# -------------------------------------------------

st.set_page_config(
    page_title="Multilingual Video Translation | AI Video Translation",
    page_icon="🎬",
    layout="wide",
)
load_styles()
init_session_state()
state = st.session_state

render_navbar()
render_hero()
render_progress_tracker(STEPS, completed_count=sum(state[step.done_flag] for step in STEPS))

main_column, side_column = st.columns([2, 1], gap="large")

with main_column:

    # Step 1: upload
    show_step_card(1)
    uploaded_file = st.file_uploader(
        "Drop your video file here", type=["mp4"], label_visibility="collapsed"
    )
    if uploaded_file and not state.uploaded:
        state.run_dir = WORKSPACE_DIR / str(uuid.uuid4())
        state.run_dir.mkdir(parents=True)
        run_file("input.mp4").write_bytes(uploaded_file.getvalue())
        state.uploaded = True
        st.rerun()

    if state.uploaded:
        render_success_badge("Video uploaded successfully")
        st.video(run_file("input.mp4"))

    # Step 2: extract audio
    if state.uploaded:
        show_step_card(2)
        if not state.audio_extracted and st.button("Extract Audio Track"):
            with st.spinner("Extracting audio with FFmpeg…"):
                extract_audio(run_file("input.mp4"), run_file("audio.wav"))
            state.audio_extracted = True
            st.rerun()

        if state.audio_extracted:
            render_success_badge("Audio extracted successfully")
            st.audio(run_file("audio.wav"))

    # Step 3: speech to text
    if state.audio_extracted:
        show_step_card(3)
        if not state.transcribed and st.button("Generate Transcript"):
            with st.spinner("Transcribing with Whisper — this may take a moment…"):
                state.transcript = transcribe_audio(run_file("audio.wav"))
            state.transcribed = True
            st.rerun()

        if state.transcribed:
            render_success_badge("Transcript generated")
            st.text_area("Original Transcript", state.transcript, height=160)

    # Step 4: translate
    if state.transcribed:
        show_step_card(4)
        selected_language = st.selectbox("Target Language", list(LANGUAGES))
        if not state.translated and st.button("Translate Text"):
            with st.spinner("Translating…"):
                state.language = LANGUAGES[selected_language]
                state.translation = translate_text(state.transcript, state.language)
            state.translated = True
            st.rerun()

        if state.translated:
            render_success_badge("Translation complete")
            st.text_area("Translated Text", state.translation, height=160)

    # Step 5: text to speech
    if state.translated:
        show_step_card(5)
        if not state.speech_generated and st.button("Generate Audio"):
            with st.spinner("Synthesizing speech and syncing duration…"):
                synthesize_speech(
                    state.translation,
                    state.language,
                    reference_audio_path=run_file("audio.wav"),
                    output_path=run_file("speech.wav"),
                )
            state.speech_generated = True
            st.rerun()

        if state.speech_generated:
            render_success_badge("Audio generated &amp; synced")
            st.audio(run_file("speech.wav"))

    # Step 6: merge and export
    if state.speech_generated:
        show_step_card(6)
        if not state.merged and st.button("Merge Audio into Video"):
            with st.spinner("Merging translated audio with video…"):
                merge_audio_into_video(
                    run_file("input.mp4"), run_file("speech.wav"), run_file("translated_video.mp4")
                )
            state.merged = True
            st.rerun()

        if state.merged:
            render_success_badge("Final video ready — pipeline complete!")
            st.video(run_file("translated_video.mp4"))
            st.download_button(
                "⬇  Download Translated Video",
                run_file("translated_video.mp4").read_bytes(),
                file_name="translated_video.mp4",
            )

with side_column:
    render_info_panel(LANGUAGES)

render_footer()
