# VideoGen AI - Setup & Debug Summary

## Issues Fixed

### 1. **CSS Compatibility Issues** ✅
- **Problem**: Missing standard `line-clamp` property in HTML template
- **Fix**: Added `line-clamp: 2;` alongside `-webkit-line-clamp: 2;` in `.video-title` and `.related-video-title` classes
- **Files**: `templates/index.html`

### 2. **Missing Dependencies** ✅
- **Problem**: `google-generativeai`, `elevenlabs`, and `python-dotenv` packages not installed
- **Fix**: Installed all required packages via pip
- **Status**: All packages now available in virtual environment

### 3. **API Key Security** ✅
- **Problem**: API keys were hardcoded in `utils.py`
- **Fix**: 
  - Migrated to environment variables using `.env` file
  - Added `python-dotenv` to manage environment variables
  - Created `.env.example` template
  - Added validation to ensure API keys are configured
- **Files**: `utils.py`, `.env.example`, `requirements.txt`

### 4. **Improved Error Handling** ✅
- **Problem**: Missing error handling for file cleanup and missing API keys
- **Fixes**:
  - Added try-catch-finally blocks in `render_video()` to ensure temp files are cleaned up
  - Added subdirectory handling for video files with audio suffix
  - Better error messages for missing API keys
  - Fixed subprocess error output handling with `capture_output=True`
- **Files**: `utils.py`, `app.py`

### 5. **Video File Path Issues** ✅
- **Problem**: Video filename handling didn't account for "_with_audio" suffix
- **Fix**: Updated `render_video()` to preserve actual filename and fixed video route in `app.py`
- **Files**: `utils.py`, `app.py`

### 6. **Requirements Updated** ✅
- Added `python-dotenv` to `requirements.txt`

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- FFmpeg (for audio/video processing)
- Google Gemini API Key
- ElevenLabs API Key

### Installation Steps

1. **Clone/Navigate to project:**
```bash
cd /Users/dinethgunawardana/Desktop/manim
```

2. **Create Python virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Add your API keys:
```
GEMINI_API_KEY=your_actual_gemini_api_key
ELEVENLABS_API_KEY=your_actual_elevenlabs_api_key
FLASK_ENV=development
FLASK_DEBUG=true
```

5. **Install FFmpeg (if not already installed):**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

6. **Run the application:**
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

---

## Project Structure

```
.
├── app.py                 # Flask application main file
├── utils.py              # Utility functions (Manim rendering, API calls)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # Project documentation
├── templates/
│   └── index.html       # Web interface
├── media/
│   ├── videos/          # Generated videos
│   ├── images/          # Temporary images
│   └── Tex/             # LaTeX files
└── videos.json          # Video metadata storage
```

---

## Features

✅ **AI-Powered Video Generation**: Generate animations from text descriptions using Google Gemini
✅ **Voice Over Integration**: Automatic text-to-speech narration using ElevenLabs
✅ **Manim Animations**: Professional mathematical animations
✅ **Web Interface**: Clean YouTube-style interface
✅ **Video Gallery**: Browse and play all generated videos
✅ **REST API**: Programmatic access to video generation

---

## Common Issues & Solutions

### Issue: "GEMINI_API_KEY environment variable not set"
**Solution**: Make sure your `.env` file exists and contains a valid `GEMINI_API_KEY`

### Issue: "ELEVENLABS_API_KEY environment variable not set"
**Solution**: Make sure your `.env` file exists and contains a valid `ELEVENLABS_API_KEY`

### Issue: "manim command not found"
**Solution**: Install Manim via pip: `pip install manim`

### Issue: "ffmpeg: command not found"
**Solution**: Install FFmpeg using your system package manager (see setup instructions)

### Issue: Video files not found after generation
**Solution**: Ensure the `media/videos/generated/480p15/` directory exists and has write permissions

---

## Testing the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open browser:**
Navigate to `http://localhost:5000`

3. **Generate a test video:**
- Go to "Create" tab
- Enter: "A simple circle with animated text saying hello world"
- Click "Generate Video"
- Wait for processing and view the result in "Gallery" tab

---

## Troubleshooting

### Debug Mode
The application runs in debug mode by default. Check terminal output for detailed error messages.

### Check Logs
Monitor the terminal where you ran `python app.py` for any errors during generation.

### Validate Environment
```bash
# Check if all packages are installed
pip list | grep -E "flask|google-generativeai|manim|elevenlabs|python-dotenv"

# Test imports
python -c "import flask, google.generativeai, manim, elevenlabs, dotenv; print('All imports successful')"
```

---

## Next Steps

1. Set up your API keys in `.env`
2. Ensure FFmpeg is installed
3. Run `python app.py`
4. Visit `http://localhost:5000`
5. Start generating videos!

---

**All errors have been fixed and the application is ready to use!** ✅
