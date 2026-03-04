<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:050d14,30:0d1a2e,70:0a1f3a,100:050d14&height=200&section=header&text=🎬%20Multilingual%20Video%20Translation&fontSize=32&fontColor=58a6ff&fontAlignY=40&desc=AI-Powered%20Video%20Translation%20with%20Audio-Video%20Sync&descAlignY=60&descColor=8b949e&animation=fadeIn" />

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Whisper](https://img.shields.io/badge/OpenAI%20Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-58a6ff?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-00e5ff?style=for-the-badge)

<br>

> An AI-powered pipeline that translates spoken content in any video into another language —  
> while keeping the audio and video in perfect sync.

<br>

**[🚀 Live Demo](#)** &nbsp;·&nbsp; **[🐛 Report a Bug](https://github.com/Mona-Agrawall/multilingual-video-translation-system/issues)** &nbsp;·&nbsp; **[✨ Request Feature](https://github.com/Mona-Agrawall/multilingual-video-translation-system/issues)**

</div>

---

## 📸 Screenshots

<div align="center">

  
<img width="1053" height="1191" alt="image" src="https://github.com/user-attachments/assets/d2489c2d-495a-4264-841f-2f00f0c2fe37" style="border-radius:10px; margin-bottom:12px;" />
<br>
<img width="898" height="1199" alt="image" src="https://github.com/user-attachments/assets/2bffc882-f426-4500-b3a5-4883666b054c"  style="border-radius:10px; margin-bottom:12px;"/>
<br>
<img width="939" height="1199" alt="image" src="https://github.com/user-attachments/assets/88921f2c-c725-4d47-a6f0-fdd7194a6501" style="border-radius:10px;"/>

</div>

---

## 🧠 How It Works

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  MP4 Video  │ →  │ Extract     │ →  │ Speech →    │ →  │  Translate  │ →  │ TTS + Sync  │ →  │   Output    │
│   Upload    │    │   Audio     │    │   Text      │    │    Text     │    │    Audio    │    │    Video    │
│             │    │  (FFmpeg)   │    │  (Whisper)  │    │  (Google)   │    │   (gTTS)    │    │  (FFmpeg)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

The pipeline works in 6 automated stages:

1. **Extract** — Pull raw audio from the uploaded video using FFmpeg
2. **Transcribe** — Convert speech to text using OpenAI Whisper
3. **Translate** — Translate the transcript using Google Translate API
4. **Synthesize** — Generate natural-sounding speech from translated text via gTTS
5. **Synchronize** — Time-stretch the generated audio to match original duration using FFmpeg
6. **Merge** — Combine the translated audio track back into the original video

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ **Speech-to-Text** | Accurate transcription using OpenAI Whisper across 99+ languages |
| 🌍 **Multi-language Translation** | Powered by Google Translate API for broad language support |
| 🔊 **Text-to-Speech** | Natural audio generation from translated text using gTTS |
| ⏱️ **Audio-Video Sync** | FFmpeg time-stretching ensures translated audio matches original timing |
| 🖥️ **Simple Web UI** | Clean Streamlit interface — upload, translate, download |
| 📁 **Auto Output** | Translated video saved automatically to `output_videos/` |

---

## 🛠️ Tech Stack

```yaml
Language    : Python 3.x
UI          : Streamlit
Transcription : OpenAI Whisper
Translation : Google Translate API
TTS         : gTTS (Google Text-to-Speech)
Audio/Video : FFmpeg, Pydub
Output      : MP4 (output_videos/)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- FFmpeg installed and added to system PATH

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mona-Agrawall/multilingual-video-translation-system.git
cd multilingual-video-translation-system

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install FFmpeg
# Windows  → https://ffmpeg.org/download.html  (add to PATH)
# macOS    → brew install ffmpeg
# Linux    → sudo apt install ffmpeg

# 4. Verify FFmpeg
ffmpeg -version
```

### Run

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
multilingual-video-translation-system/
│
├── app.py                  # Streamlit UI and main app logic
├── requirements.txt        # Python dependencies
├── output_videos/          # Translated video output (auto-created)
└── README.md               # Project documentation
```

---

## 🎯 Use Cases

- 🎓 **Education** — Translate lecture videos for international students
- 🌐 **Content Localization** — Dub YouTube or marketing videos into multiple languages
- 🗣️ **Speech Dubbing** — Prototype voice-over workflows for films or podcasts
- ♿ **Accessibility** — Make video content available in a viewer's native language

---

## 🔮 Future Enhancements

- [ ] **Speaker diarization** — Preserve individual speaker voices in translation
- [ ] **Subtitle generation** — Export `.srt` / `.vtt` subtitle files alongside video
- [ ] **Batch processing** — Translate multiple videos in one run
- [ ] **Voice cloning** — Match the original speaker's voice style in the output
- [ ] **Language auto-detection** — Automatically detect source language
- [ ] **Progress bar** — Real-time pipeline progress in the Streamlit UI

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: describe your change"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

---

## 👩‍💻 Author

<div align="center">

**Mona Agrawal**

[![GitHub](https://img.shields.io/badge/GitHub-Mona--Agrawall-181717?style=for-the-badge&logo=github)](https://github.com/Mona-Agrawall)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-mona--agrawal-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/mona-agrawal-/)

</div>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*If you found this project useful, consider giving it a ⭐ — it means a lot!*

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:050d14,30:0d1a2e,70:0a1f3a,100:050d14&height=100&section=footer&animation=fadeIn" />

</div>