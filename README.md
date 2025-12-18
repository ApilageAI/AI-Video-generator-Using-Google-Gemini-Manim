<div align="center">

# 🎬 VideoGen AI - Apilage AI Video Generator

### AI-Powered Educational Video Generation with Voice Over & Mathematical Animations

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![Manim](https://img.shields.io/badge/Manim-Community-orange.svg)](https://www.manim.community)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Gemini%20AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI"/>
  <img src="https://img.shields.io/badge/Manim-Animations-FF6B6B?style=for-the-badge" alt="Manim"/>
  <img src="https://img.shields.io/badge/TTS-Enabled-9B59B6?style=for-the-badge" alt="TTS"/>
</p>

---

**VideoGen AI** transforms text descriptions into stunning animated educational videos with professional voice-over narration. Simply describe what you want to explain, and the AI generates beautiful mathematical animations, code visualizations, and educational content—all with synchronized audio narration.

[🚀 Quick Start](#-quick-start) • [📖 How It Works](#-how-it-works) • [🔧 Installation](#-installation-guide) • [📡 API Docs](#-api-reference) • [❓ Troubleshooting](#-troubleshooting)

</div>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🎯 How It Works](#-how-it-works)
  - [System Architecture](#system-architecture)
  - [Flowchart](#flowchart)
  - [Detailed Process](#detailed-process)
- [📋 Requirements](#-requirements)
- [🔧 Installation Guide](#-installation-guide)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
- [🚀 Running the Application](#-running-the-application)
- [📡 API Reference](#-api-reference)
- [🧠 Core Technologies Explained](#-core-technologies-explained)
  - [Google Gemini AI & TTS](#google-gemini-ai--tts)
  - [Manim Animation Library](#manim-animation-library)
- [🎛️ Configuration Options](#️-configuration-options)
- [❓ Troubleshooting](#-troubleshooting)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Generation** | Describe your video in plain English—Gemini AI creates the animation code |
| 🎙️ **Voice Over Integration** | Automatic TTS narration using Gemini TTS with gTTS fallback |
| 🎨 **Professional Animations** | Stunning mathematical visualizations powered by Manim |
| 🌐 **Modern Web Interface** | Clean, YouTube-style UI for creating and viewing videos |
| 📚 **Video Gallery** | Browse, play, and download all generated videos |
| 📡 **REST API** | Programmatic access for integration with other applications |
| ⚡ **Job Queue System** | Background processing with status tracking |
| 🔄 **Auto-Retry Logic** | AI-powered error fixing with multiple retry attempts |
| 📱 **Responsive Design** | Works on desktop, tablet, and mobile devices |
| 🎬 **Subtitles Support** | Auto-generated WebVTT subtitles |

---

## 🎯 How It Works

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          VIDEOGEN AI ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────┐   │
│   │   User/API   │────▶│  Flask App   │────▶│    Job Queue System      │   │
│   │   Request    │     │  (app.py)    │     │  (Background Worker)     │   │
│   └──────────────┘     └──────────────┘     └────────────┬─────────────┘   │
│                                                          │                   │
│                              ┌───────────────────────────▼────────────────┐ │
│                              │              GENERATION PIPELINE            │ │
│                              │  ┌─────────────────────────────────────┐   │ │
│                              │  │  1. GEMINI AI CODE GENERATION       │   │ │
│                              │  │     • Analyze topic & level         │   │ │
│                              │  │     • Generate Manim Python code    │   │ │
│                              │  │     • Create voice script           │   │ │
│                              │  │     • Generate subtitles            │   │ │
│                              │  └──────────────────┬──────────────────┘   │ │
│                              │                     ▼                       │ │
│                              │  ┌─────────────────────────────────────┐   │ │
│                              │  │  2. CODE VALIDATION & SANITIZATION  │   │ │
│                              │  │     • Python syntax validation      │   │ │
│                              │  │     • Manim-specific fixes          │   │ │
│                              │  │     • AI auto-fix on errors         │   │ │
│                              │  └──────────────────┬──────────────────┘   │ │
│                              │                     ▼                       │ │
│                              │  ┌─────────────────────────────────────┐   │ │
│                              │  │  3. MANIM VIDEO RENDERING           │   │ │
│                              │  │     • Execute animation code        │   │ │
│                              │  │     • Render at 480p/15fps          │   │ │
│                              │  │     • Generate MP4 video            │   │ │
│                              │  └──────────────────┬──────────────────┘   │ │
│                              │                     ▼                       │ │
│                              │  ┌─────────────────────────────────────┐   │ │
│                              │  │  4. GEMINI TTS AUDIO GENERATION     │   │ │
│                              │  │     • Convert voice script to audio │   │ │
│                              │  │     • Professional voice (Kore)     │   │ │
│                              │  │     • gTTS fallback if needed       │   │ │
│                              │  └──────────────────┬──────────────────┘   │ │
│                              │                     ▼                       │ │
│                              │  ┌─────────────────────────────────────┐   │ │
│                              │  │  5. FFMPEG AUDIO/VIDEO MERGE        │   │ │
│                              │  │     • Sync audio with video         │   │ │
│                              │  │     • Extend video if needed        │   │ │
│                              │  │     • Final MP4 with audio          │   │ │
│                              │  └──────────────────┬──────────────────┘   │ │
│                              └─────────────────────┼──────────────────────┘ │
│                                                    ▼                         │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                      OUTPUT: Final Video + Subtitles                  │ │
│   │  • MP4 video with synchronized voice-over                            │ │
│   │  • WebVTT subtitle file                                              │ │
│   │  • Stored in /uploads folder                                         │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Flowchart

```
                              ┌─────────────────┐
                              │  User Input     │
                              │  (Topic + Level)│
                              └────────┬────────┘
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │   Create Job & Add to    │
                        │   Background Queue       │
                        └──────────────┬───────────┘
                                       │
                                       ▼
                    ┌───────────────────────────────────┐
                    │  GEMINI AI (gemini-2.0-flash)     │
                    │  ┌─────────────────────────────┐  │
                    │  │ Input: Topic + Level        │  │
                    │  │ Output:                     │  │
                    │  │  • Manim Python Code        │  │
                    │  │  • Voice Narration Script   │  │
                    │  │  • WebVTT Subtitles         │  │
                    │  └─────────────────────────────┘  │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Validate & Sanitize     │
                        │  Python Code             │
                        └──────────────┬───────────┘
                                       │
                          ┌────────────┼────────────┐
                          │            │            │
                          ▼            │            ▼
                    ┌──────────┐       │      ┌──────────────┐
                    │  Valid?  │───NO──┤      │  AI Auto-Fix │
                    │          │       │      │  (max 3x)    │
                    └────┬─────┘       │      └──────────────┘
                         │             │
                        YES            │
                         │◄────────────┘
                         ▼
              ┌──────────────────────────┐
              │  MANIM RENDERING ENGINE  │
              │  • Execute Animation     │
              │  • Generate 480p15 MP4   │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │  GEMINI TTS ENGINE       │
              │  • Voice: "Kore"         │
              │  • Output: WAV → MP3     │
              │  • Fallback: gTTS        │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │  FFMPEG PROCESSING       │
              │  • Extend video if short │
              │  • Merge audio + video   │
              │  • Audio sync: 300ms     │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │  Copy to /uploads        │
              │  Update Job Status       │
              └────────────┬─────────────┘
                           │
                           ▼
               ┌─────────────────────┐
               │   ✅ Video Ready!   │
               │   Return Video URL  │
               └─────────────────────┘
```

### Detailed Process

#### Step 1: Request Processing
When you submit a topic, the system:
1. Validates input (3-500 characters)
2. Creates a unique job ID (UUID)
3. Adds to a thread-safe background queue
4. Returns job ID immediately for status tracking

#### Step 2: AI Code Generation
Gemini AI (`gemini-2.0-flash`) generates:
- **Manim Python code** with professional animations
- **Voice script** for natural narration
- **WebVTT subtitles** with timing

The AI follows strict rules for:
- Zero visual overlap (one element at a time)
- Consistent color palette
- Proper timing for audio sync
- Branded "Apilage AI" ending

#### Step 3: Code Validation
The system sanitizes and validates:
- Python syntax checking via `ast.parse()`
- Common Manim issues auto-fixed
- Invalid colors replaced
- Missing imports added
- AI auto-fix with up to 3 retries

#### Step 4: Video Rendering
Manim renders the animation:
- Quality: 480p at 15fps
- Duration: 50-70 seconds
- Professional mathematical visualizations

#### Step 5: Audio Generation
Gemini TTS generates voice-over:
- Model: `gemini-2.5-flash-preview-tts`
- Voice: "Kore" (clear, professional)
- Format: WAV converted to MP3
- Fallback: gTTS if Gemini fails

#### Step 6: Audio/Video Merge
FFmpeg combines everything:
- Extends video if audio is longer
- Syncs audio with 300ms delay
- Outputs final MP4 with embedded audio

---

## 📋 Requirements

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 / macOS 10.14 / Ubuntu 18.04 | Latest versions |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 4 GB | 8 GB+ |
| **Storage** | 2 GB free | 10 GB+ |
| **Internet** | Required | Stable connection |

### Software Dependencies

| Software | Purpose | Required |
|----------|---------|----------|
| **Python 3.8+** | Runtime environment | ✅ Yes |
| **FFmpeg** | Audio/video processing | ✅ Yes |
| **LaTeX** | Mathematical equations in Manim | ⚠️ Recommended |
| **Cairo/Pango** | Graphics rendering | ⚠️ Auto-installed |

### API Keys Required

| Service | Purpose | How to Get |
|---------|---------|------------|
| **Google Gemini API** | AI code generation & TTS | [Google AI Studio](https://makersuite.google.com/app/apikey) |

### Python Packages

```txt
flask              # Web framework
google-generativeai # Gemini AI SDK
python-dotenv      # Environment variables
gtts               # Google Text-to-Speech (fallback)
manim              # Animation library (installed separately)
```

---

## 🔧 Installation Guide

### Windows

#### Step 1: Install Python
```powershell
# Download Python from https://www.python.org/downloads/
# ✅ Check "Add Python to PATH" during installation

# Verify installation
python --version   # Should show Python 3.8+
pip --version      # Should show pip version
```

#### Step 2: Install FFmpeg
```powershell
# Option A: Using Chocolatey (recommended)
choco install ffmpeg

# Option B: Using Winget
winget install ffmpeg

# Option C: Manual installation
# 1. Download from https://ffmpeg.org/download.html
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to System PATH

# Verify installation
ffmpeg -version
```

#### Step 3: Install LaTeX (Optional but Recommended)
```powershell
# Download MiKTeX from https://miktex.org/download
# Run installer and complete setup
# Verify installation
latex --version
```

#### Step 4: Clone & Setup Project
```powershell
# Clone the repository
git clone <your-repo-url>
cd manimfull

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### Step 5: Configure Environment
```powershell
# Create .env file
copy .env.example .env

# Edit .env with your API key
notepad .env
```

Add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=true
```

---

### macOS

#### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Dependencies
```bash
# Install Python (if needed)
brew install python@3.11

# Install FFmpeg
brew install ffmpeg

# Install LaTeX (optional but recommended)
brew install --cask mactex-no-gui
# Or minimal version:
brew install basictex

# Install additional dependencies for Manim
brew install cairo pango pkg-config

# Verify installations
python3 --version
ffmpeg -version
```

#### Step 3: Clone & Setup Project
```bash
# Clone the repository
git clone <your-repo-url>
cd manimfull

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### Step 4: Configure Environment
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API key
nano .env   # or: code .env / vim .env
```

Add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=true
```

---

### Linux (Ubuntu/Debian)

#### Step 1: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 2: Install Dependencies
```bash
# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install FFmpeg
sudo apt install ffmpeg -y

# Install LaTeX (for mathematical equations)
sudo apt install texlive texlive-latex-extra texlive-fonts-extra -y

# Install Manim dependencies
sudo apt install libcairo2-dev libpango1.0-dev -y

# Install additional build tools
sudo apt install build-essential pkg-config -y

# Verify installations
python3 --version
ffmpeg -version
latex --version
```

#### Step 3: Clone & Setup Project
```bash
# Clone the repository
git clone <your-repo-url>
cd manimfull

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Manim
pip install manim
```

#### Step 4: Configure Environment
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API key
nano .env
```

Add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=true
```

#### Step 5: Set Permissions (if needed)
```bash
# Make uploads directory writable
chmod 755 uploads/
chmod 755 media/
```

---

## 🚀 Running the Application

### Quick Start (All Platforms)

```bash
# 1. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 2. Start the server
python app.py
```

### Access Points

| Interface | URL | Description |
|-----------|-----|-------------|
| **Web App** | http://localhost:5002 | Main video generation interface |
| **API Docs** | http://localhost:5002/api-docs | Interactive API documentation |
| **Health Check** | http://localhost:5002/health | Server status endpoint |

### Production Deployment

```bash
# Using Gunicorn (recommended for production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5002 app:app

# Using Docker (if Dockerfile is available)
docker build -t videogen-ai .
docker run -p 5002:5002 videogen-ai
```

---

## 📡 API Reference

The VideoGen AI provides a comprehensive REST API for programmatic video generation.

### Base URL
```
http://localhost:5002
```

### Authentication
Currently, the API does not require authentication. For production, implement API key authentication.

---

### POST `/api/generate`
Submit a video generation request.

**Request:**
```bash
curl -X POST http://localhost:5002/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Explain the Pythagorean theorem with visual proof",
    "level": "basic"
  }'
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | ✅ Yes | The topic to explain (3-500 characters) |
| `level` | string | ❌ No | `basic`, `intermediate`, or `special_topic` (default: `basic`) |

**Response (202 Accepted):**
```json
{
  "success": true,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Video generation queued",
  "queue_position": 1,
  "status_url": "/api/status/550e8400-e29b-41d4-a716-446655440000",
  "video_url": "/api/video/550e8400-e29b-41d4-a716-446655440000"
}
```

---

### GET `/api/status/{job_id}`
Check the status of a video generation job.

**Request:**
```bash
curl http://localhost:5002/api/status/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "success": true,
  "job": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "topic": "Explain the Pythagorean theorem",
    "level": "basic",
    "status": "processing",
    "progress": "Rendering video...",
    "created_at": "2025-12-18T10:30:00.000Z",
    "updated_at": "2025-12-18T10:31:00.000Z"
  }
}
```

**Job Status Values:**
| Status | Description |
|--------|-------------|
| `pending` | Job is waiting in queue |
| `processing` | Job is currently being processed |
| `completed` | Video is ready |
| `failed` | Generation failed (check `error` field) |
| `cancelled` | Job was cancelled by user |

---

### GET `/api/video/{job_id}`
Get video details for a completed job.

**Request:**
```bash
curl http://localhost:5002/api/video/550e8400-e29b-41d4-a716-446655440000
```

**Response (completed):**
```json
{
  "success": true,
  "ready": true,
  "video_url": "/uploads/MathExplanationScene_20251218_103500.mp4",
  "video_filename": "MathExplanationScene_20251218_103500.mp4",
  "full_url": "http://localhost:5002/uploads/MathExplanationScene_20251218_103500.mp4",
  "subtitles": "WEBVTT\n\n00:00:00.000 --> 00:00:04.000\nWelcome to this lesson...",
  "topic": "Explain the Pythagorean theorem"
}
```

---

### GET `/api/queue`
Get current queue status.

**Request:**
```bash
curl http://localhost:5002/api/queue
```

**Response:**
```json
{
  "success": true,
  "queue": {
    "pending": 5,
    "processing": 1,
    "total_jobs": 150
  },
  "pending_jobs": [
    {
      "id": "job-id-1",
      "topic": "Explain derivatives...",
      "queue_position": 1,
      "created_at": "2025-12-18T10:30:00.000Z"
    }
  ],
  "processing_jobs": [
    {
      "id": "job-id-2",
      "topic": "Linear algebra basics...",
      "progress": "Generating audio...",
      "created_at": "2025-12-18T10:28:00.000Z"
    }
  ]
}
```

---

### POST `/api/cancel/{job_id}`
Cancel a pending job.

**Request:**
```bash
curl -X POST http://localhost:5002/api/cancel/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "success": true,
  "message": "Job cancelled"
}
```

---

### GET `/api/videos`
Get list of all generated videos.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 50 | Maximum videos to return |
| `offset` | integer | 0 | Pagination offset |

**Request:**
```bash
curl "http://localhost:5002/api/videos?limit=10&offset=0"
```

**Response:**
```json
{
  "success": true,
  "total": 150,
  "limit": 10,
  "offset": 0,
  "videos": [
    {
      "title": "MathExplanationScene...",
      "url": "/uploads/MathExplanationScene_20251218_103500.mp4",
      "full_url": "http://localhost:5002/uploads/...",
      "filename": "MathExplanationScene_20251218_103500.mp4",
      "level": "basic",
      "subtitles": "",
      "created": "2025-12-18T10:35:00.000Z",
      "size": 2456789
    }
  ]
}
```

---

### GET `/api/uploads`
Get list of all uploaded videos (direct file listing).

**Request:**
```bash
curl "http://localhost:5002/api/uploads?limit=20"
```

---

### GET `/health`
Health check endpoint.

**Request:**
```bash
curl http://localhost:5002/health
```

**Response:**
```json
{
  "status": "ok",
  "videos_count": 150,
  "queue_pending": 3,
  "queue_processing": 1,
  "worker_running": true
}
```

---

### API Error Responses

All errors follow this format:
```json
{
  "success": false,
  "error": "Detailed error message"
}
```

| HTTP Code | Description |
|-----------|-------------|
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Job/resource doesn't exist |
| 500 | Internal Server Error |

---

### JavaScript SDK Example

```javascript
// Using the included SDK: /static/apilage-sdk.js

// Generate a video
const response = await fetch('http://localhost:5002/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'Explain quadratic equations step by step',
    level: 'intermediate'
  })
});
const { job_id } = await response.json();

// Poll for status
const checkStatus = async () => {
  const status = await fetch(`http://localhost:5002/api/status/${job_id}`);
  const data = await status.json();
  
  if (data.job.status === 'completed') {
    console.log('Video ready:', data.job.video_url);
  } else if (data.job.status === 'failed') {
    console.error('Failed:', data.job.error);
  } else {
    setTimeout(checkStatus, 5000); // Check again in 5 seconds
  }
};
checkStatus();
```

---

### Python SDK Example

```python
import requests
import time

BASE_URL = "http://localhost:5002"

# Submit video generation request
response = requests.post(f"{BASE_URL}/api/generate", json={
    "topic": "Explain the chain rule in calculus",
    "level": "intermediate"
})
job_id = response.json()["job_id"]
print(f"Job submitted: {job_id}")

# Poll for completion
while True:
    status = requests.get(f"{BASE_URL}/api/status/{job_id}").json()
    job = status["job"]
    
    print(f"Status: {job['status']} - {job.get('progress', '')}")
    
    if job["status"] == "completed":
        print(f"✅ Video ready: {BASE_URL}{job['video_url']}")
        break
    elif job["status"] == "failed":
        print(f"❌ Failed: {job['error']}")
        break
    
    time.sleep(5)  # Wait 5 seconds before checking again
```

---

## 🧠 Core Technologies Explained

### Google Gemini AI & TTS

#### What is Gemini AI?

**Gemini** is Google's most advanced AI model family, capable of understanding and generating text, code, images, and audio. VideoGen AI uses two Gemini models:

| Model | Purpose | Description |
|-------|---------|-------------|
| `gemini-2.0-flash` | Code Generation | Generates Manim Python code, voice scripts, and subtitles |
| `gemini-2.5-flash-preview-tts` | Text-to-Speech | Converts narration text to natural-sounding audio |

#### How Gemini Code Generation Works

```
┌───────────────────────────────────────────────────────────────┐
│                    GEMINI CODE GENERATION                     │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  INPUT:                                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Topic: "Explain the Pythagorean theorem"                │ │
│  │ Level: "basic"                                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          │                                    │
│                          ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              GEMINI 2.0 FLASH MODEL                     │ │
│  │                                                         │ │
│  │  • Analyzes topic and determines educational content    │ │
│  │  • Generates Python Manim code with animations          │ │
│  │  • Creates natural voice-over script                    │ │
│  │  • Produces timed WebVTT subtitles                      │ │
│  │  • Follows strict visual rules (no overlap, colors)     │ │
│  │  • Adds branded "Apilage AI" ending                     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          │                                    │
│                          ▼                                    │
│  OUTPUT:                                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 1. Manim Python Code (400-800 lines)                    │ │
│  │ 2. Voice Script (50-70 seconds of narration)            │ │
│  │ 3. WebVTT Subtitles (timed to match animations)         │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

#### Gemini TTS (Text-to-Speech)

Gemini TTS is Google's latest text-to-speech model, offering:

- **Natural Voice**: The "Kore" voice provides clear, professional narration
- **Multi-language**: Supports multiple languages (primary: English)
- **High Quality**: 24kHz sample rate, converted to MP3
- **Fast Generation**: Streams audio in real-time

**TTS Pipeline:**
```
Voice Script → Gemini TTS API → Raw Audio (L16) → WAV → FFmpeg → MP3
```

**Fallback System:**
If Gemini TTS fails, the system automatically falls back to gTTS (Google Text-to-Speech):
```python
try:
    audio = generate_audio_with_gemini(text)  # Primary
except:
    audio = gTTS(text).save()  # Fallback
```

---

### Manim Animation Library

#### What is Manim?

**Manim** (Mathematical Animation Engine) is a Python library for creating precise mathematical animations. Originally created by 3Blue1Brown's Grant Sanderson, the community edition is now maintained by the Manim Community.

#### Why Manim?

| Feature | Benefit |
|---------|---------|
| **Precision** | Exact mathematical constructions |
| **Programmatic** | AI can generate animation code |
| **Beautiful** | Professional-quality output |
| **Flexible** | Supports text, shapes, graphs, 3D |
| **Export** | Direct MP4/GIF output |

#### How Manim Works

```
┌───────────────────────────────────────────────────────────────┐
│                      MANIM PIPELINE                           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. PYTHON CODE EXECUTION                                     │
│     ┌─────────────────────────────────────────────────────┐  │
│     │  class MathExplanationScene(Scene):                 │  │
│     │      def construct(self):                           │  │
│     │          title = Text("Pythagorean Theorem")        │  │
│     │          self.play(Write(title))                    │  │
│     │          ...                                        │  │
│     └─────────────────────────────────────────────────────┘  │
│                          │                                    │
│                          ▼                                    │
│  2. SCENE CONSTRUCTION                                        │
│     • Create mathematical objects (Text, MathTex, shapes)     │
│     • Define animations (Write, FadeIn, Transform)            │
│     • Set timing and transitions                              │
│                          │                                    │
│                          ▼                                    │
│  3. FRAME RENDERING (Cairo/OpenGL)                            │
│     • Each frame rendered at specified resolution             │
│     • 480p at 15fps = 15 frames per second                    │
│     • Anti-aliased vector graphics                            │
│                          │                                    │
│                          ▼                                    │
│  4. VIDEO ENCODING (FFmpeg)                                   │
│     • Frames compiled into MP4 video                          │
│     • H.264 codec for compatibility                           │
│     • Output: media/videos/*/480p15/*.mp4                     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

#### Manim Objects Used

| Object | Description | Example |
|--------|-------------|---------|
| `Text` | Display text | `Text("Hello", font_size=42)` |
| `MathTex` | LaTeX equations | `MathTex(r"e^{i\pi} + 1 = 0")` |
| `Circle` | Circles | `Circle(radius=2, color=BLUE)` |
| `Rectangle` | Rectangles | `Rectangle(width=4, height=2)` |
| `Arrow` | Arrows | `Arrow(LEFT, RIGHT)` |
| `VGroup` | Group objects | `VGroup(obj1, obj2).arrange(DOWN)` |
| `Dot` | Points | `Dot(color=RED)` |

#### Manim Animations Used

| Animation | Effect | Example |
|-----------|--------|---------|
| `Write` | Draw text/shapes | `self.play(Write(text))` |
| `FadeIn` | Fade in | `self.play(FadeIn(obj, shift=UP))` |
| `FadeOut` | Fade out | `self.play(FadeOut(obj))` |
| `Transform` | Morph between | `self.play(Transform(a, b))` |
| `GrowFromCenter` | Grow from center | `self.play(GrowFromCenter(circle))` |
| `Create` | Draw outline | `self.play(Create(shape))` |
| `Indicate` | Pulse highlight | `self.play(Indicate(obj))` |

---

## 🎛️ Configuration Options

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Development settings
FLASK_ENV=development
FLASK_DEBUG=true

# Optional - Server settings
HOST=0.0.0.0
PORT=5002
```

### Video Quality Settings

Modify in `utils.py`:
```python
# Current: Low quality for speed
cmd = ["manim", temp_file, scene_name, "-ql", ...]

# Options:
# -ql  = 480p at 15fps (fast)
# -qm  = 720p at 30fps (medium)
# -qh  = 1080p at 60fps (high quality, slow)
# -qk  = 4K at 60fps (very slow)
```

### Voice Settings

The TTS voice can be changed in `utils.py`:
```python
voice_config=genai_types.VoiceConfig(
    prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
        voice_name="Kore"  # Change voice here
    )
)
```

Available Gemini TTS voices:
- `Kore` (Default - Clear, professional)
- `Puck` (Casual, friendly)
- `Charon` (Deep, authoritative)
- `Fenrir` (Energetic)
- `Aoede` (Soft, calm)

---

## ❓ Troubleshooting

### Common Issues & Solutions

#### 1. "GEMINI_API_KEY environment variable not set"

**Problem:** The application can't find your API key.

**Solutions:**
```bash
# Option 1: Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Option 2: Set environment variable (temporary)
export GEMINI_API_KEY=your_key_here  # macOS/Linux
set GEMINI_API_KEY=your_key_here     # Windows CMD
$env:GEMINI_API_KEY="your_key_here"  # Windows PowerShell

# Option 3: Pass directly to Python
GEMINI_API_KEY=your_key python app.py
```

---

#### 2. "FFmpeg not found" or Video has no audio

**Problem:** FFmpeg is not installed or not in PATH.

**Solutions:**

**Windows:**
```powershell
# Using Chocolatey
choco install ffmpeg -y

# Verify
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
ffmpeg -version
```

**Linux:**
```bash
sudo apt install ffmpeg -y
ffmpeg -version
```

---

#### 3. "LaTeX Error" or Mathematical equations don't render

**Problem:** LaTeX is not installed for rendering equations.

**Solutions:**

**Windows:**
```powershell
# Download and install MiKTeX from https://miktex.org/download
```

**macOS:**
```bash
# Full TeX (large)
brew install --cask mactex

# Or minimal
brew install basictex
sudo tlmgr update --self
sudo tlmgr install collection-latex
```

**Linux:**
```bash
sudo apt install texlive texlive-latex-extra texlive-fonts-extra -y
```

---

#### 4. "ModuleNotFoundError: No module named 'manim'"

**Problem:** Manim is not installed.

**Solution:**
```bash
# Activate virtual environment first!
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install Manim
pip install manim
```

---

#### 5. Video generation times out

**Problem:** Animation is too complex or system is slow.

**Solutions:**
1. **Use simpler topics:** Try "What is a circle?" instead of complex multi-step derivations
2. **Reduce video quality:** The default 480p/15fps is already optimized for speed
3. **Check system resources:** Ensure you have at least 4GB free RAM
4. **Increase timeout:** Modify `timeout=600` in `render_video()` function

---

#### 6. "Both Gemini TTS and gTTS failed"

**Problem:** Audio generation failed completely.

**Solutions:**
1. **Check internet connection:** Both TTS services require internet
2. **Check Gemini API key:** Ensure it's valid and has quota
3. **Check Gemini TTS access:** TTS may require specific API permissions
4. **Firewall issues:** Ensure outbound connections to Google APIs are allowed

---

#### 7. Audio/Video out of sync

**Problem:** Voice-over doesn't match the animations.

**Solutions:**
1. The system adds a 300ms audio delay for sync
2. If still off, modify `adelay` in `combine_audio_video()`:
```python
"-af", "adelay=300|300",  # Increase/decrease this value
```

---

#### 8. "Port 5002 already in use"

**Problem:** Another process is using the port.

**Solutions:**
```bash
# Find and kill the process using port 5002
# macOS/Linux:
lsof -ti:5002 | xargs kill -9

# Windows:
netstat -ano | findstr :5002
taskkill /PID <PID> /F

# Or use a different port:
python app.py  # Then modify PORT in app.py
```

---

#### 9. Worker not processing jobs

**Problem:** Jobs stay in "pending" status forever.

**Solutions:**
1. **Restart the application:** The worker thread may have crashed
2. **Check logs:** Look for `[WORKER]` messages in console output
3. **Check jobs.json:** Delete it if corrupted: `rm jobs.json`

---

#### 10. "Cairo" or "Pango" errors on macOS

**Problem:** Missing graphics libraries.

**Solution:**
```bash
brew install cairo pango pkg-config
pip uninstall manim
pip install manim
```

---

### Debug Mode

Enable verbose logging:
```bash
# Set debug mode in .env
FLASK_DEBUG=true
FLASK_ENV=development

# Or run with verbose Manim output
python -c "from utils import generate_manim_code; print(generate_manim_code('test', 'basic'))"
```

### Log Locations

| Log Type | Location |
|----------|----------|
| Flask | Console output |
| Manim | `media/` folder + console |
| Jobs | `jobs.json` |
| Videos | `videos.json` |

---

## 📂 Project Structure

```
manimfull/
├── 📄 app.py                  # Main Flask application & API endpoints
├── 📄 utils.py                # AI generation, TTS, video rendering
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # Environment variables (create this)
├── 📄 .env.example            # Template for .env file
├── 📄 jobs.json               # Job queue persistence
├── 📄 videos.json             # Video metadata (legacy)
│
├── 📁 templates/              # HTML templates
│   ├── index.html             # Main web interface
│   └── api-docs.html          # API documentation page
│
├── 📁 static/                 # Static assets
│   └── apilage-sdk.js         # JavaScript SDK for API
│
├── 📁 uploads/                # Generated videos (final output)
│   └── *.mp4                  # Video files with timestamps
│
├── 📁 media/                  # Manim working directory
│   ├── videos/                # Rendered video files
│   │   └── generated/
│   │       └── 480p15/        # Low quality renders
│   ├── images/                # Manim temporary images
│   └── Tex/                   # LaTeX temporary files
│
├── 📁 icon/                   # Icon assets
│   ├── browser/
│   ├── clock/
│   ├── cpu/
│   ├── flags/
│   ├── mime/
│   ├── os/
│   └── other/
│
└── 📄 README.md               # This documentation
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd manimfull

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Make your changes
# ...

# Format code
black app.py utils.py

# Run tests (if available)
pytest

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### Contribution Guidelines

1. **Code Style:** Follow PEP 8 guidelines
2. **Documentation:** Update README for new features
3. **Testing:** Add tests for new functionality
4. **Commits:** Use descriptive commit messages
5. **Pull Requests:** Reference any related issues

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **[Manim Community](https://www.manim.community/)** - Mathematical animation engine
- **[Google Gemini AI](https://ai.google.dev/)** - AI code generation & TTS
- **[Flask](https://flask.palletsprojects.com/)** - Web framework
- **[FFmpeg](https://ffmpeg.org/)** - Audio/video processing
- **[gTTS](https://gtts.readthedocs.io/)** - Fallback text-to-speech

---

<div align="center">

**Made with ❤️ by Apilage AI**

[🌐 Website](https://apilage.com) • [📧 Support](mailto:support@apilage.com) • [🐛 Report Bug](https://github.com/apilage/videogen-ai/issues)

</div>
