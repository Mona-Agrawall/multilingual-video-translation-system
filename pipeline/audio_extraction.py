"""Step 2: pull the audio track out of the uploaded video."""

from .media import run_ffmpeg


def extract_audio(video_path, audio_path):
    """Save the video's sound as a 16 kHz mono WAV file, the format Whisper expects."""
    run_ffmpeg("-i", video_path, "-ac", "1", "-ar", "16000", audio_path)
