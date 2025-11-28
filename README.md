# VideoGen AI - AI-Powered Video Generation with Voice Over

VideoGen AI is a web application that generates animated videos from text descriptions using AI. It combines Google's Gemini AI for creating Manim animations with ElevenLabs text-to-speech for voice over narration, creating fully automated video content.

## ✨ Features

- **AI-Powered Video Generation**: Describe your video in plain English and let AI create it
- **Voice Over Integration**: Automatic text-to-speech narration using ElevenLabs
- **Manim Animations**: Professional mathematical animations powered by Manim
- **Web Interface**: Clean, YouTube-style interface for creating and viewing videos
- **Video Gallery**: Browse and play all generated videos
- **REST API**: Programmatic access to video generation capabilities

## 🚀 Demo

![VideoGen AI Interface](https://via.placeholder.com/800x400/FF0000/FFFFFF?text=VideoGen+AI+Demo)

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.8+**
- **FFmpeg** (for audio/video processing)
- **Google Gemini API Key**
- **ElevenLabs API Key**

### Installing FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd videogen-ai
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API Keys:**

Edit `utils.py` and update the API keys:

```python
# Set up Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Set up ElevenLabs API
elevenlabs = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")
```

## ⚙️ Configuration

### API Keys Setup

1. **Google Gemini API:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Replace `YOUR_GEMINI_API_KEY` in `utils.py`

2. **ElevenLabs API:**
   - Visit [ElevenLabs](https://elevenlabs.io/app/profile)
   - Sign up and get your API key
   - Replace `YOUR_ELEVENLABS_API_KEY` in `utils.py`

### Voice Configuration

The app uses the following ElevenLabs voice settings:
- **Voice ID**: `JBFqnCBsd6RMkjVDRZzb` (English voice)
- **Model**: `eleven_multilingual_v2`
- **Format**: MP3 44.1kHz 128kbps

## 🚀 Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser:**
Navigate to `http://127.0.0.1:5000`

## 📖 Usage

### Web Interface

1. **Video Creator Tab:**
   - Enter a math topic to explain (e.g., "rotational motion", "quadratic equations", "Pythagorean theorem")
   - Select the explanation level: Basic, Intermediate, or Special Topic
   - Click "Generate Video"
   - Wait for AI to create educational animation, voice over, and subtitles
   - The video will automatically appear in the gallery

2. **Video Gallery Tab:**
   - Browse all generated math videos with level indicators
   - Click on any video to play it with synchronized subtitles
   - Use the download button to save videos locally
   - Videos include educational animations, voice over, and auto-generated subtitles

### API Usage

#### Generate Video
```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Your video description here"}'
```

**Response:**
```json
{
  "video_url": "/videos/GeneratedScene.mp4"
}
```

#### Get Video List
```bash
curl http://127.0.0.1:5000/videos
```

**Response:**
```json
[
  {
    "title": "Your video description...",
    "url": "/videos/GeneratedScene.mp4",
    "filename": "GeneratedScene.mp4"
  }
]
```

## 🏗️ Project Structure

```
videogen-ai/
├── app.py                 # Main Flask application
├── utils.py              # AI integration and video processing
├── requirements.txt      # Python dependencies
├── videos.json          # Video metadata storage
├── templates/
│   └── index.html       # Web interface
├── media/
│   ├── videos/          # Generated video files
│   └── images/          # Manim temporary files
└── README.md            # This file
```

## 🔧 How It Works

1. **Text Input**: User provides a video description
2. **AI Code Generation**: Gemini AI creates Manim Python code based on the description
3. **Video Rendering**: Manim renders the animation to MP4
4. **Voice Over**: ElevenLabs generates speech audio from the same text
5. **Audio-Video Sync**: FFmpeg combines video and audio into final output
6. **Storage**: Video is saved and metadata stored for gallery access

## 🎯 Example Videos

Try these prompts:

- "A blue circle that grows and shrinks with text 'Welcome' appearing"
- "Mathematical equation e=mc² with animated derivation"
- "Colorful geometric shapes dancing to music"
- "Step-by-step explanation of photosynthesis with diagrams"

## 🐛 Troubleshooting

### Common Issues

**"Failed to generate audio"**
- Check your ElevenLabs API key is valid
- Ensure you have credits in your ElevenLabs account

**"Failed to render video"**
- Verify Manim is installed correctly
- Check that FFmpeg is available in PATH

**"No text provided"**
- Ensure you're sending JSON with a "text" field in POST requests

### Logs

Check Flask console output for detailed error messages and processing status.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit: `git commit -am 'Add new feature'`
5. Push: `git push origin feature-name`
6. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Manim Community](https://www.manim.community/) - Mathematical animation engine
- [Google Gemini AI](https://ai.google.dev/) - Code generation
- [ElevenLabs](https://elevenlabs.io/) - Text-to-speech
- [Flask](https://flask.palletsprojects.com/) - Web framework

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Ensure all prerequisites are met
