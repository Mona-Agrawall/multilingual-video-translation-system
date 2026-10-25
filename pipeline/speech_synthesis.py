"""Step 5: speak the translated text and fit it to the original audio length."""

from gtts import gTTS

from .media import get_duration, run_ffmpeg

# FFmpeg's atempo filter only accepts speed factors between 0.5 and 2.0.
MIN_SPEED = 0.5
MAX_SPEED = 2.0


def build_atempo_filter(speed):
    """Chain atempo filters so speed factors outside 0.5-2.0 still work."""
    filters = []
    while speed > MAX_SPEED:
        filters.append(f"atempo={MAX_SPEED}")
        speed /= MAX_SPEED
    while speed < MIN_SPEED:
        filters.append(f"atempo={MIN_SPEED}")
        speed /= MIN_SPEED
    filters.append(f"atempo={speed}")
    return ",".join(filters)


def synthesize_speech(text, language, reference_audio_path, output_path):
    """Generate speech for the text, sped up or slowed down to match the reference audio."""
    raw_speech_path = output_path.with_suffix(".mp3")
    gTTS(text=text, lang=language).save(str(raw_speech_path))

    speed = get_duration(raw_speech_path) / get_duration(reference_audio_path)
    run_ffmpeg("-i", raw_speech_path, "-filter:a", build_atempo_filter(speed), output_path)
