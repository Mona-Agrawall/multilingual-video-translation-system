# Multilingual Video Translation System

An AI-powered system that translates spoken content in a video into another language while maintaining accurate audio-video synchronization.

```Video → Audio → Text → Translate → Speech → Synced Video```

## Features
- Upload MP4 video via Streamlit UI
- Extract audio using FFmpeg
- Convert speech to text using Whisper
- Translate transcript into target language
- Generate translated speech using TTS
- Automatically match generated audio duration to original
- Merge translated audio back into video


## Workflow
1. Extract audio from video
2. Convert speech to text
3. Translate text
4. Convert translated text to speech
5. Match audio duration using FFmpeg time-stretching
6. Merge translated audio with video

Final output is saved inside:
```output_videos/```

## Tech Stack
- Python
- Streamlit
- OpenAI Whisper
- FFmpeg
- gTTS
- Pydub
- Google Translate API

## How to Run
1. Install Dependencies
```pip install -r requirements.txt```
2. Install FFmpeg
Download and add FFmpeg to system PATH.
   Verify:
  ```ffmpeg -version```

3. Run Application
```streamlit run app.py```

Open in browser:
http://localhost:8501

## Use Cases
- Video localization
- Multilingual content creation
- Educational translation
- Speech dubbing
## Screenshots Of The Project

<img width="1917" height="1197" alt="Screenshot 2026-03-03 145416" src="https://github.com/user-attachments/assets/17c3e83b-483e-4687-bce3-364ebb411eee" />
<img width="1919" height="1199" alt="Screenshot 2026-03-03 145425" src="https://github.com/user-attachments/assets/2fef2169-78ae-4553-a776-a3ce2c868793" />
<img width="1919" height="1199" alt="image" src="https://github.com/user-attachments/assets/55393dbd-0659-497c-b412-88fcc93fd63c" />


## Author
Mona Agrawal

## Thank you!
