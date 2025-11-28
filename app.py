from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from utils import generate_manim_code, render_video

app = Flask(__name__)

VIDEOS_FILE = 'videos.json'

def load_videos():
    if os.path.exists(VIDEOS_FILE):
        with open(VIDEOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_videos(videos):
    with open(VIDEOS_FILE, 'w') as f:
        json.dump(videos, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    text_input = data.get('text', '')
    level = data.get('level', 'basic')

    if not text_input:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Generate Manim code, voice script, and subtitles using Gemini
        code, voice_script, subtitles = generate_manim_code(text_input, level)

        # Render the video with voice over
        video_path = render_video(code, text_input=voice_script, subtitles=subtitles)

        # Create video metadata
        video_filename = os.path.basename(video_path)
        video_url = f"/videos/{video_filename}"
        video_title = f"{text_input} ({level.title()})"[:50] + ('...' if len(f"{text_input} ({level.title()})") > 50 else '')

        # Load existing videos, add new one, and save
        videos = load_videos()
        videos.insert(0, {
            'title': video_title,
            'url': video_url,
            'filename': video_filename,
            'level': level,
            'subtitles': subtitles
        })
        save_videos(videos)

        # Return the video URL and subtitles
        return jsonify({'video_url': video_url, 'subtitles': subtitles})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/videos')
def get_videos():
    videos = load_videos()
    return jsonify(videos)

@app.route('/videos/<filename>')
def get_video(filename):
    # Handle both files directly in 480p15 and those with _with_audio suffix
    video_path = os.path.join('media/videos/generated/480p15', filename)
    if os.path.exists(video_path):
        return send_from_directory(os.path.dirname(video_path), filename)
    else:
        return jsonify({'error': 'Video not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
