import google.generativeai as genai
import os
import tempfile
import subprocess
from elevenlabs import ElevenLabs, play
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Gemini API
gemini_key = os.getenv("GEMINI_API_KEY", "")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please create a .env file with your API key.")
genai.configure(api_key=gemini_key)

# Set up ElevenLabs API
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY", "")
if not elevenlabs_key:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set. Please create a .env file with your API key.")
elevenlabs = ElevenLabs(api_key=elevenlabs_key)

def generate_manim_code(text_input, level="basic"):
    """
    Use Gemini to generate Manim Python code and a voice script based on the user's math topic and level.
    Returns a tuple: (manim_code, voice_script, subtitles)
    """
    level_descriptions = {
        "basic": "fundamental concepts, simple explanations, basic terminology",
        "intermediate": "more detailed explanations, some mathematical relationships, intermediate concepts",
        "special_topic": "advanced concepts, complex relationships, in-depth analysis"
    }

    prompt = f"""
    Create an explanatory math video for the topic: "{text_input}" at {level} level ({level_descriptions[level]}).

    Generate THREE things:

    1. A Manim Python script that creates an educational video scene:
    - Import from manim: from manim import *
    - Define a class that inherits from Scene, e.g., class MathExplanationScene(Scene):
    - Implement the construct method with educational animations and visualizations
    - Use appropriate Manim objects like Text, Circle, Square, Arrow, etc., with colors and animations
    - Create step-by-step visual explanations suitable for the {level} level
    - Include title, main content, and summary sections
    - Keep animations smooth and educational, not just decorative
    - Ensure the code is syntactically correct and runnable
    - Never use images, SVG, PNG, or external media
    - Make the total animation duration approximately 10-15 seconds

    2. A voice script (narrative text) that would be spoken over the video:
    - Write clear, educational narration that explains the math concept
    - Structure it to match the video's sections (introduction, explanation, conclusion)
    - Use appropriate language for {level} level understanding
    - Keep it engaging and suitable for text-to-speech
    - Include timing markers in the format [MM:SS] at the start of each segment
    - Ensure the total narration time matches the video duration (10-15 seconds)
    - Example: [00:00] Welcome to this math explanation. [00:03] Let's start with the basics.

    3. Subtitles with timing (in WebVTT format):
    - Break the voice script into subtitle segments (2-3 seconds each)
    - Include start and end times for each subtitle based on the timing markers
    - Format as WebVTT with proper timing
    - Ensure timing aligns with the voice script markers

    Format your response as:
    MANIM_CODE:
    ```python
    [Python code here]
    ```

    VOICE_SCRIPT:
    [Voice script text here]

    SUBTITLES:
    [WebVTT subtitle content here]
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    content = response.text.strip()

    # Parse the response to extract code, voice script, and subtitles
    manim_code = ""
    voice_script = ""
    subtitles = ""

    if "MANIM_CODE:" in content:
        manim_part = content.split("MANIM_CODE:")[1].split("VOICE_SCRIPT:")[0].strip()
        if manim_part.startswith("```python"):
            manim_code = manim_part[9:]
        if manim_code.endswith("```"):
            manim_code = manim_code[:-3]
        manim_code = manim_code.strip()

    if "VOICE_SCRIPT:" in content:
        voice_part = content.split("VOICE_SCRIPT:")[1].split("SUBTITLES:")[0].strip()
        voice_script = voice_part.strip()

    if "SUBTITLES:" in content:
        subtitles = content.split("SUBTITLES:")[1].strip()

    return manim_code, voice_script, subtitles

def generate_audio(text_input):
    """
    Generate audio from text using ElevenLabs API.
    """
    try:
        audio = elevenlabs.text_to_speech.convert(
            voice_id='JBFqnCBsd6RMkjVDRZzb',  # voice_id
            optimize_streaming_latency=0,
            output_format='mp3_44100_128',
            text=text_input,
            model_id='eleven_multilingual_v2',
        )
        # Save audio to a temporary file
        audio_path = tempfile.mktemp(suffix='.mp3')
        with open(audio_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        return audio_path
    except Exception as e:
        raise Exception(f"Failed to generate audio: {e}")

def get_video_duration(video_path):
    """
    Get the duration of a video file using ffprobe.
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        import json
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"Warning: Could not get video duration: {e}")
        return 10.0  # Default fallback

def adjust_audio_to_video(audio_path, video_duration):
    """
    Adjust audio duration to match video duration using ffmpeg.
    """
    adjusted_audio_path = audio_path.replace('.mp3', '_adjusted.mp3')
    cmd = [
        "ffmpeg", "-i", audio_path, "-t", str(video_duration), "-c:a", "libmp3lame", adjusted_audio_path
    ]
    try:
        subprocess.run(cmd, check=True, cwd=os.getcwd(), capture_output=True)
        return adjusted_audio_path
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not adjust audio duration: {e}")
        return audio_path

def render_video(code, scene_name="MathExplanationScene", text_input=None, subtitles=None):
    """
    Save the generated code to a temporary file and render the video using Manim.
    If text_input is provided, generate audio and combine with video.
    Returns the path to the rendered video.
    """
    temp_file = None
    audio_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Run Manim to render the video
        output_dir = "media/videos/generated"
        os.makedirs(output_dir, exist_ok=True)

        cmd = [
            "manim", temp_file, scene_name, "-pql", "--media_dir", "media"
        ]

        subprocess.run(cmd, check=True, cwd=os.getcwd(), capture_output=True)

        # The video is saved in a temp dir like tmpcbjrryc3, but we need to move it to generated
        # Find the actual video path
        import glob
        video_files = glob.glob("media/videos/*/480p15/*.mp4")
        if video_files:
            latest_video = max(video_files, key=os.path.getctime)
            final_path = f"{output_dir}/480p15/{os.path.basename(latest_video)}"
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            if os.path.exists(final_path):
                os.unlink(final_path)
            os.rename(latest_video, final_path)

            # If text_input is provided, generate audio and combine
            if text_input:
                audio_path = generate_audio(text_input)
                # Get video duration and adjust audio to match
                video_duration = get_video_duration(final_path)
                adjusted_audio_path = adjust_audio_to_video(audio_path, video_duration)
                final_path_with_audio = combine_audio_video(final_path, adjusted_audio_path)
                # Clean up audio files
                for path in [audio_path, adjusted_audio_path]:
                    if path and os.path.exists(path) and path != adjusted_audio_path:
                        os.unlink(path)
                return final_path_with_audio
            else:
                return final_path
        else:
            raise Exception("Video file not found after rendering")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to render video with Manim: {str(e)}")
    except Exception as e:
        # Clean up on any error
        if audio_path and os.path.exists(audio_path):
            os.unlink(audio_path)
        raise
    finally:
        # Clean up temp file
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)

def combine_audio_video(video_path, audio_path):
    """
    Combine audio and video using ffmpeg.
    """
    output_path = video_path.replace('.mp4', '_with_audio.mp4')
    cmd = [
        "ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-shortest", output_path
    ]
    try:
        subprocess.run(cmd, check=True, cwd=os.getcwd())
        # Replace original video with the one with audio
        os.rename(output_path, video_path)
        return video_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to combine audio and video: {e}")
