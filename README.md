# Multilingual Video Translation System

AI-based system that translates spoken content in a video into another language while keeping audio-video synchronization intact.

## Workflow
1. Extract audio from video
2. Convert speech to text
3. Translate text
4. Convert translated text to speech
5. Merge translated audio with video

## Tech Stack
- Python
- Speech Recognition
- Translation APIs
- FFmpeg

## How to Run
1. Place the input video inside `input_videos/`
2. Run `main.py`
3. The translated video will be saved in `output_videos/`