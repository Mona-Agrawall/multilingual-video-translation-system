"""The video translation pipeline. Each module handles one step."""

from .audio_extraction import extract_audio
from .speech_synthesis import synthesize_speech
from .transcription import transcribe_audio
from .translation import translate_text
from .video_merging import merge_audio_into_video

__all__ = [
    "extract_audio",
    "transcribe_audio",
    "translate_text",
    "synthesize_speech",
    "merge_audio_into_video",
]
