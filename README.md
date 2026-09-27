Source-Available Archive — Not Open Source
This repository is publicly available for archival and educational purposes. Commercial use, redistribution, copying and rebranding, white-labeling, and publication of substantially copied versions are prohibited without written permission from ApilageAI PVT LTD.



# VideoGen AI

AI-powered video generation from natural-language prompts using **Google Gemini**, **Manim**, and text-to-speech narration.

VideoGen AI is a Flask web application that turns an educational topic or short description into an animated explainer video. Gemini generates the Manim animation code, narration is generated as audio, and the application renders synchronized video segments into a final MP4 with subtitles.

> **Project status:** This repository is archived. This README documents the implementation currently present in the `main` branch.

## Features

- Generate educational animation videos from text prompts.
- Use Google Gemini to create Manim animation code.
- Generate narration audio with gTTS and optional ElevenLabs integration.
- Audio-first production pipeline for improved narration/video synchronization.
- Render mathematical notation and formulas through Manim and LaTeX.
- Background job queue for asynchronous API-based generation.
- Track pending, processing, completed, failed, and cancelled jobs.
- Browse generated videos through the web interface or REST API.
- Retrieve subtitles and generated video metadata.
- API authentication using `X-Auth-Code` and `X-API-Key` headers.
- Health-check endpoint for deployment monitoring.

## How It Works

1. A user submits an educational topic or description.
2. The application generates a narration script and splits it into timed segments.
3. Text-to-speech audio is generated for each segment.
4. Gemini generates Manim code for the corresponding visual content.
5. Manim renders the animation segments.
6. Audio and video are muxed and concatenated into a final MP4.
7. The completed video and subtitles are returned to the user.

## Architecture

- **Flask** — web application and REST API.
- **Google Gemini** — AI-generated Manim animation code and educational content.
- **Manim** — mathematical and educational animation rendering.
- **gTTS / ElevenLabs** — narration generation.
- **FFmpeg / pydub** — audio/video processing and synchronization.
- **JSON files** — lightweight persistence for jobs and video metadata.
- **Gunicorn** — production WSGI server.

## Requirements

### Software

- Python 3.9 or newer
- FFmpeg
- LaTeX and `dvisvgm` for Manim mathematical rendering
- A Google Gemini API key
- Optional ElevenLabs API key

The included deployment documentation targets AlmaLinux/RHEL-based systems. Other operating systems may require different package-manager commands.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ApilageAI/AI-Video-generator-Using-Google-Gemini-Manim.git
cd AI-Video-generator-Using-Google-Gemini-Manim
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The main Python dependencies are:

- Flask 3.0.0
- `google-generativeai` 0.8.3
- gTTS 2.5.0
- `python-dotenv` 1.0.0
- Manim 0.18.0
- pydub 0.25.1

### 4. Install system dependencies

Install FFmpeg and the libraries required by Manim. On AlmaLinux:

```bash
sudo dnf install -y ffmpeg ffmpeg-devel
sudo dnf install -y cairo cairo-devel pango pango-devel
sudo dnf install -y python3-devel gcc gcc-c++
sudo dnf install -y libffi-devel openssl-devel
```

Install LaTeX support for `Tex` and `MathTex` scenes:

```bash
sudo dnf install -y texlive-scheme-medium dvisvgm
```

See [`INSTALL_LATEX.md`](INSTALL_LATEX.md) for detailed installation and troubleshooting instructions.

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Set your credentials in `.env`:

```dotenv
GEMINI_API_KEY=your_google_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Required for authenticated /api/* endpoints
AUTH_CODE=replace_with_a_strong_auth_code
API_KEY=replace_with_a_strong_api_key
```

Keep `.env` private and never commit real API keys or authentication credentials.

## Running Locally

Start the Flask application directly:

```bash
source venv/bin/activate
python app.py
```

The development server listens on:

```text
http://localhost:5002
```

Open the web interface at `http://localhost:5002/`.

Useful pages and endpoints:

- `/` — web application
- `/api-docs` — API documentation page
- `/health` — application and worker health status
- `/videos` — list generated videos

## API Usage

Authenticated API requests require both headers:

```http
X-Auth-Code: your_auth_code
X-API-Key: your_api_key
```

### Queue a video-generation job

```bash
curl -X POST http://localhost:5002/api/generate \
  -H "Content-Type: application/json" \
  -H "X-Auth-Code: your_auth_code" \
  -H "X-API-Key: your_api_key" \
  -d '{"topic":"Explain the Pythagorean theorem"}'
```

Example response:

```json
{
  "success": true,
  "job_id": "uuid-string",
  "message": "Video generation queued",
  "queue_position": 1,
  "status_url": "/api/status/uuid-string",
  "video_url": "/api/video/uuid-string"
}
```

### Check job status

```bash
curl http://localhost:5002/api/status/JOB_ID \
  -H "X-Auth-Code: your_auth_code" \
  -H "X-API-Key: your_api_key"
```

Job statuses include:

- `pending`
- `processing`
- `completed`
- `failed`
- `cancelled`

### Retrieve a completed video

```bash
curl http://localhost:5002/api/video/JOB_ID \
  -H "X-Auth-Code: your_auth_code" \
  -H "X-API-Key: your_api_key"
```

### Inspect the queue

```bash
curl http://localhost:5002/api/queue \
  -H "X-Auth-Code: your_auth_code" \
  -H "X-API-Key: your_api_key"
```

### List generated videos

```bash
curl "http://localhost:5002/api/videos?limit=50&offset=0" \
  -H "X-Auth-Code: your_auth_code" \
  -H "X-API-Key: your_api_key"
```

### Cancel a pending job

```bash
curl -X POST http://localhost:5002/api/cancel/JOB_ID \
  -H "X-Auth-Code: your_auth_code" \
  -H "X-API-Key: your_api_key"
```

Only jobs with `pending` status can be cancelled.

## Project Structure

```text
.
├── app.py                    # Flask application, routes, and job queue
├── utils.py                  # AI, narration, Manim, and video-generation pipeline
├── wsgi.py                   # WSGI entry point for Gunicorn
├── requirements.txt          # Python dependencies
├── .env.example              # Environment-variable template
├── templates/                # Web UI and API documentation templates
├── static/                   # Frontend assets
├── media/                    # Manim-generated media files
├── uploads/                  # Final uploaded/generated MP4 files
├── videos/                   # Video output directory
├── texts/                    # Generated text assets
├── jobs.json                 # Persisted job state
├── videos.json               # Video metadata
├── test_*.py                 # Test and verification scripts
├── DEPLOYMENT_GUIDE.md       # AlmaLinux, Gunicorn, and Apache deployment guide
└── INSTALL_LATEX.md          # LaTeX setup for Manim math rendering
```

Generated media, job state, and uploaded videos may grow substantially over time. Add appropriate retention and cleanup policies for production deployments.

## Testing and Verification

The repository includes test and verification scripts such as:

```bash
python test_comprehensive.py
python test_e2e_generation.py
python test_fallback.py
python test_problematic_case.py
python test_syntax_fix.py
python test_text_layout.py
```

Shell-based checks are also available:

```bash
bash test-api.sh
bash test-server.sh
bash verify_all.sh
```

Some tests require configured API credentials, a working Manim installation, FFmpeg, LaTeX, and access to the local application server.

## Production Deployment

For a production deployment, use Gunicorn behind a reverse proxy such as Apache:

```bash
gunicorn --bind 127.0.0.1:5000 \
  --workers 2 \
  --timeout 300 \
  --worker-class sync \
  wsgi:application
```

Video generation is CPU- and disk-intensive. Configure increased proxy timeouts, monitor available disk space, and protect generated media and API credentials.

For the complete AlmaLinux and Virtualmin deployment procedure, see [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md).

## Troubleshooting

### Video generation fails

Verify the following:

```bash
ffmpeg -version
manim --version
python --version
```

Then check that `GEMINI_API_KEY` is valid and inspect the application logs.

### Mathematical text does not render

Install LaTeX and `dvisvgm`, then verify:

```bash
latex --version
pdflatex --version
xelatex --version
dvisvgm --version
```

See [`INSTALL_LATEX.md`](INSTALL_LATEX.md).

### API requests return 401 or 403

Confirm that both `X-Auth-Code` and `X-API-Key` are present and exactly match the values configured in `.env`.

### Jobs are not being processed

Check `/health` and confirm that `worker_running` is `true`. Also inspect `jobs.json` and the application logs for rendering or filesystem errors.

## Security Notes

- Do not commit `.env` or expose API keys in client-side code.
- Replace development authentication values with strong secrets.
- Restrict CORS to trusted origins in production instead of allowing `*`.
- Run behind HTTPS when exposing the application publicly.
- Use a production WSGI server rather than Flask's development server.
- Restrict access to generated media and API endpoints as appropriate.
- Review disk usage and remove old intermediate and final video files.

## License

No license file is currently included in this repository. Unless a license is added, the code should be treated as **all rights reserved** by default.

## Acknowledgements

This project builds on:

- [Google Gemini](https://ai.google.dev/)
- [Manim](https://www.manim.community/)
- [Flask](https://flask.palletsprojects.com/)
- [gTTS](https://gtts.readthedocs.io/)
- [ElevenLabs](https://elevenlabs.io/)
- [FFmpeg](https://ffmpeg.org/)
