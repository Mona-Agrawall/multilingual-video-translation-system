"""Step 3: turn the spoken audio into text with OpenAI Whisper."""

WHISPER_MODEL = "base"


def transcribe_audio(audio_path):
    """Return the text spoken in the audio file."""
    # Whisper loads PyTorch, which takes seconds to import, so it is imported
    # here rather than at the top to keep the page itself loading quickly.
    import whisper

    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(str(audio_path))
    return result["text"].strip()
