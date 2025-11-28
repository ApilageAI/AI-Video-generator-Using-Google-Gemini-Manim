# VideoGen AI | AI Powered Video Generation with Voice Over  
AI Video Generator using Google Gemini and Manim

VideoGen AI is a web app that turns text prompts into fully generated educational videos.  
It uses Google Gemini to create Manim animation code and ElevenLabs to generate natural voice over, then combines everything into a single ready to watch video.

Perfect for math explainers, concept breakdowns, and auto generated learning content.

---

## ✨ Features

* **AI video from plain text**  
  Type what you want explained and let the system design the animation and script.

* **Automatic voice over**  
  ElevenLabs text to speech is used to create clear and natural narration.

* **Manim powered animations**  
  High quality math and concept visualizations rendered with Manim.

* **Simple web interface**  
  YouTube style layout for creating, browsing, and watching generated videos.

* **Video gallery**  
  All generated videos are listed with easy playback and download.

* **REST API**  
  Trigger video generation and retrieve videos from your own apps.

---

## 🚀 Demo
## 🖼️ Screenshots

![UI 1](https://firebasestorage.googleapis.com/v0/b/apilage-ai.firebasestorage.app/o/Screenshot%202025-11-28%20at%209.54.50%E2%80%AFPM.png?alt=media&token=8f4f3537-83f3-45f3-bb34-8db217e0a193)

![UI 2](https://firebasestorage.googleapis.com/v0/b/apilage-ai.firebasestorage.app/o/Screenshot%202025-11-28%20at%209.54.55%E2%80%AFPM.png?alt=media&token=1f405581-f806-4a3f-9c98-0e70d4e74ecc)

![UI 3](https://firebasestorage.googleapis.com/v0/b/apilage-ai.firebasestorage.app/o/Screenshot%202025-11-28%20at%209.54.58%E2%80%AFPM.png?alt=media&token=4ed487bf-6649-4a14-8c05-cf826eb1da31)
---

## 🎞️ Demo Video

<video width="800" controls>
  <source src="https://firebasestorage.googleapis.com/v0/b/apilage-ai.firebasestorage.app/o/IntroShapes.mp4?alt=media&token=a6f6ec53-3cf9-48c4-8676-38986092289d" type="video/mp4">
  Your browser does not support the video tag.
</video>

---
## 📋 Prerequisites

Make sure you have:

* Python 3.8 or newer  
* FFmpeg installed and in your PATH  
* Google Gemini API key  
* ElevenLabs API key  

### Install FFmpeg

**macOS with Homebrew**
```bash
brew install ffmpeg

Ubuntu or Debian

sudo apt update
sudo apt install ffmpeg

Windows

Download FFmpeg from the official site and add it to your PATH:
https://ffmpeg.org/download.html

⸻

🛠️ Installation
	1.	Clone the repository

git clone <your repo url>
cd videogen_ai


	2.	Create and activate a virtual environment

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate


	3.	Install dependencies

pip install -r requirements.txt


	4.	Configure API keys
Edit utils.py and set your keys:

# Gemini setup
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# ElevenLabs setup
elevenlabs = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")



⸻

⚙️ Configuration

Google Gemini API
	1.	Go to Google AI Studio
https://makersuite.google.com/app/apikey
	2.	Create an API key
	3.	Paste it into utils.py in place of YOUR_GEMINI_API_KEY

ElevenLabs API
	1.	Go to ElevenLabs profile page
https://elevenlabs.io/app/profile
	2.	Create or copy your API key
	3.	Paste it into utils.py in place of YOUR_ELEVENLABS_API_KEY

Voice settings in ElevenLabs
	•	Voice ID: JBFqnCBsd6RMkjVDRZzb
	•	Model: eleven_multilingual_v2
	•	Output: MP3, 44.1 kHz, 128 kbps

You can customize these in the code if you prefer other voices.

⸻

🚀 Running the app
	1.	Start the Flask server:

python app.py


	2.	Open your browser and visit:

http://127.0.0.1:5000



⸻

📖 Usage

Web interface

Video Creator tab
	1.	Enter a topic you want explained
Examples:
	•	rotational motion
	•	quadratic equations
	•	Pythagorean theorem
	2.	Choose the detail level: Basic, Intermediate, or Special topic
	3.	Click Generate Video
	4.	Wait while Gemini, Manim, ElevenLabs, and FFmpeg do the work
	5.	Your new video will appear in the gallery when done

Video Gallery tab
	•	Browse all generated videos
	•	Each entry shows the title and level
	•	Click a video to play it with voice and subtitles
	•	Use the download button to save the file locally

API usage

Generate a video

curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Your video description here"}'

Response:

{
  "video_url": "/videos/GeneratedScene.mp4"
}

Get list of videos

curl http://127.0.0.1:5000/videos

Response:

[
  {
    "title": "Your video description...",
    "url": "/videos/GeneratedScene.mp4",
    "filename": "GeneratedScene.mp4"
  }
]


⸻

🏗️ Project structure

Main files and folders:
	•	app.py
Flask app entry point
	•	utils.py
Gemini and ElevenLabs integration plus video pipeline helpers
	•	requirements.txt
Python package list
	•	videos.json
Stored metadata for generated videos
	•	templates/index.html
Front end template
	•	media/videos
Final rendered video files
	•	media/images
Temporary Manim output and frames

⸻

🔧 How it works
	1.	User input
You provide a plain text description of the content you want.
	2.	Gemini content and code generation
Gemini creates both explanation content and Manim Python code for the animation.
	3.	Manim rendering
Manim renders the animation to an MP4 video.
	4.	Voice over generation
ElevenLabs converts the explanation text into speech audio.
	5.	Audio and video merge
FFmpeg combines the animation and audio track into the final video.
	6.	Storage and gallery
The resulting video is stored on disk and listed in the gallery through videos.json.

⸻

🎯 Example prompts

Try prompts like:
	•	A blue circle that grows and shrinks while the word Welcome appears
	•	Animated explanation of the equation e = mc²
	•	Colorful geometric shapes moving in patterns
	•	Step by step explanation of photosynthesis with simple diagrams
	•	Introduction to Newton third law with force pair examples

⸻

🐛 Troubleshooting

Failed to generate audio
	•	Check that your ElevenLabs API key is correct
	•	Confirm you have enough credits in your ElevenLabs account

Failed to render video
	•	Ensure Manim is installed and callable from your environment
	•	Confirm FFmpeg is installed and in your PATH

No text provided
	•	For API calls make sure the JSON body includes a "text" field

Where to check logs
	•	Look at the Flask server console output
	•	Errors from Manim, FFmpeg, or the APIs are printed there

⸻

🤝 Contributing

Contributions are welcome.
	1.	Fork the repo
	2.	Create a feature branch

git checkout -b feature-name


	3.	Make and test your changes
	4.	Commit your work

git commit -am "Add new feature"


	5.	Push to your fork

git push origin feature-name


	6.	Open a pull request

⸻

📄 License

This project is released under the MIT License.
See the LICENSE file for full details.

⸻

🙏 Acknowledgments
	•	Manim Community for the animation engine
	•	Google Gemini AI for content and code generation
	•	ElevenLabs for high quality text to speech
	•	Flask for the web framework


