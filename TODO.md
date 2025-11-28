# TODO: Math Video Generator with Level Selection and Subtitles

## Tasks
- [x] Update requirements.txt to include elevenlabs SDK
- [x] Modify utils.py to import ElevenLabs and set API key
- [x] Add generate_audio function in utils.py to create voice over from text
- [x] Modify render_video function to generate audio and combine with video using ffmpeg
- [x] Ensure ffmpeg is available for audio-video muxing
- [x] Test the integration by generating a video with voice over
- [x] Modify generate_manim_code to create math explanation videos with level selection
- [x] Add subtitle generation and timing in utils.py
- [x] Update app.py to handle level parameter and store subtitle data
- [x] Update templates/index.html to add level selection dropdown
- [x] Add download button and subtitle display in video player
- [x] Test with rotational motion example at different levels
