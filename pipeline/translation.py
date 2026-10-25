"""Step 4: translate the transcript into the target language."""

import textwrap

from deep_translator import GoogleTranslator

# Google Translate rejects requests of 5000 characters or more,
# so long transcripts are sent in smaller pieces.
MAX_CHUNK_LENGTH = 4500


def translate_text(text, language):
    """Translate text into the given language code (for example "hi" or "fr")."""
    translator = GoogleTranslator(source="auto", target=language)
    chunks = textwrap.wrap(text, MAX_CHUNK_LENGTH)
    return " ".join(translator.translate(chunk) for chunk in chunks)
