# Audio-First Video Generation Workflow

## Overview

The system has been refactored to use an **audio-first workflow** instead of the traditional animation-first approach. This ensures perfect synchronization between narration and animations, and allows for adaptive video templates that adjust to the actual audio duration.

## New Workflow Steps

### Previous Flow (Animation-First) ❌
```
Generating video...
  → Rendering animation...
  → Adding voice narration...
  → Finalizing video...
```

### New Flow (Audio-First) ✓
```
1. Generating audio script
   ↓
2. Rendering voice
   ↓
3. Analyzing audio timing
   ↓
4. Generating adaptive Manim code (matches audio duration)
   ↓
5. Rendering animations
   ↓
6. Combining audio and video
   ↓
Final Output
```

## Key Components

### 1. Audio Script Generation
**Function:** `generate_audio_script_with_timing(topic, level, style)`

- Generates a structured narration script optimized for speech
- Includes segment breakdown with timing information
- Estimates total duration (50-90 seconds)
- Returns JSON with:
  - `script`: Full narration text
  - `segments`: List of content segments with timing
  - `total_duration_estimate`: Estimated video duration
  - `words_count`: Word count for pacing reference
  - `voice_type`: Recommended voice characteristics

**Output Example:**
```json
{
  "script": "Today we'll learn about fractions...",
  "segments": [
    {
      "time_start": 0,
      "duration": 5,
      "type": "title",
      "description": "Introduction to fractions",
      "visual_description": "Title with colorful background"
    },
    ...
  ],
  "total_duration_estimate": 78,
  "words_count": 195,
  "voice_type": "Clear, professional, engaging (like Kore)",
  "pace": "Normal - about 130-150 words per minute"
}
```

### 2. Voice Rendering
**Function:** `generate_audio(text_input)`

- Converts script to high-quality voice narration
- Uses Gemini TTS (with gTTS fallback)
- Returns path to audio file (MP3 or WAV)
- Extracts actual audio duration for adaptive code generation

### 3. Audio Timing Analysis
**Function:** `get_audio_timing_info(audio_path)`

- Analyzes rendered audio to get exact duration
- Suggests segment breaks based on actual timing
- Returns:
  - `duration`: Actual audio duration in seconds
  - `suggested_segments`: Timing boundaries for segments

### 4. Adaptive Manim Code Generation
**Function:** `generate_adaptive_manim_code(topic, level, script_data, audio_duration, style)`

**This is the key innovation!**

Instead of using a fixed template, the AI generates Manim code that:
- ✓ Matches the actual audio duration exactly
- ✓ Aligns animations with narration segments
- ✓ Uses proportional timing (if audio is 90s instead of 70s, animation durations scale)
- ✓ Avoids template repetition - creates unique animation for each topic
- ✓ Adapts animation complexity to available time

**Features:**
- Generates custom animations based on content
- Scales animations proportionally to audio length
- Uses `self.wait()` times that sum exactly to audio duration
- Creates segment-specific animations
- Doesn't use cookie-cutter templates

### 5. Video Rendering
**Function:** `render_video(code, text_input=None)`

- Renders Manim animations to video
- With audio-first workflow, called WITHOUT text_input
- Produces video without audio (to avoid re-encoding delays)
- Returns path to generated MP4

### 6. Audio-Video Combination
**Function:** `combine_audio_video(video_path, audio_path)`

- Combines pre-rendered audio and video
- Extends or compresses video to match audio duration
- Uses ffmpeg for efficient combination
- Returns path to final video with embedded audio

## Job Processing Flow

In `app.py`, the `process_job()` function now:

1. **Generates audio script** with timing information
2. **Renders voice** from the script
3. **Analyzes audio** to get actual duration
4. **Generates adaptive Manim code** based on audio timing
5. **Renders video** animations
6. **Combines** audio and video
7. **Copies** to uploads folder

### Progress Updates
Job status shows real-time progress:
- "Generating audio script..." (Step 1)
- "Rendering voice narration..." (Step 2)
- "Analyzing audio timing..." (Step 3)
- "Generating adaptive animations..." (Step 4)
- "Rendering video animations..." (Step 5)
- "Combining audio and video..." (Step 6)
- "Completed!" (Done)

## Benefits of Audio-First Workflow

### 1. **Perfect Synchronization**
- Animations are designed AFTER audio is created
- Every animation duration matches narration timing
- No more awkward silences or rushed explanations

### 2. **Adaptive Templates**
- No more using the same video structure for all topics
- Each video is uniquely generated based on content
- Animations adjust to audio length automatically

### 3. **Dynamic Duration Adjustment**
- Videos scale naturally from 50-90 seconds
- Longer scripts = slower animations = more time for explanation
- Shorter scripts = faster animations = concise videos
- Perfect pacing regardless of content

### 4. **Content-Aware Animations**
- Manim code knows the exact narration for each segment
- Creates specific visuals for each explanation
- Animations complement speech, not the other way around

### 5. **Better Quality**
- Audio rendered first at optimal quality
- Video animations perfectly timed
- Smooth combination with minimal processing
- Final video has better sync than ever before

## Technical Implementation Details

### Prompt Engineering
The adaptive Manim code generator includes:
- Full script text in prompt
- Exact audio duration
- Segment breakdown with descriptions
- Style-specific guidelines
- Timing requirements

### Automatic Scaling
When audio duration differs from estimated:
```python
scale_factor = audio_duration / estimated_total
actual_duration = segment_duration * scale_factor
```

All segment durations scale proportionally.

### Animation Timing
For a 70-second audio:
- Intro animations: ~5 seconds
- Definition segment: ~15 seconds (with narration)
- Examples: ~25 seconds (with narration)
- Summary: ~15 seconds (with narration)
- Ending: ~10 seconds (with outro)

**Total = Exactly 70 seconds**

## Fallback Handling

### If Audio Generation Fails
1. Job reports error with masked message
2. User sees "Voice rendering failed"
3. Original error details hidden (security)

### If Manim Code Generation Fails
1. Attempts to fix code with AI
2. If fix fails, reports error
3. User sees "Animation generation failed"

### If Audio-Video Combination Fails
1. System tries to use video without audio
2. Logs warning but continues
3. User gets video (without narration)
4. Better than no video at all

## Usage Example

```python
from app import create_job

# Create a job
job_id = create_job("Photosynthesis", "intermediate")

# System automatically:
# 1. Generates script about photosynthesis
# 2. Renders narration with Gemini TTS
# 3. Analyzes audio duration (might be 72 seconds)
# 4. Generates Manim code optimized for 72 seconds
# 5. Renders animations
# 6. Combines audio + video
# 7. Saves to uploads/

# Check job status
job = get_job(job_id)
print(job['progress'])  # Shows current step
print(job['video_url'])  # Final URL when complete
```

## Configuration

No configuration changes needed! The workflow is automatic.

### Optional Parameters (for future enhancement)
```python
# In generate_audio_script_with_timing():
script_data = generate_audio_script_with_timing(
    topic="Photosynthesis",
    level="intermediate",  # basic, intermediate, special_topic
    style="animated"       # animated, minimal, mathematical, creative, technical, storytelling
)

# In generate_adaptive_manim_code():
code, script = generate_adaptive_manim_code(
    topic="Photosynthesis",
    level="intermediate",
    script_data=script_data,
    audio_duration=72.5,
    style="animated"
)
```

## Performance

### Typical Timeline
- Audio script generation: ~5 seconds
- Voice rendering: ~10 seconds
- Audio timing analysis: ~1 second
- Adaptive Manim generation: ~15 seconds
- Video rendering: ~30-60 seconds (depends on complexity)
- Audio-video combination: ~5 seconds

**Total: ~70-90 seconds per video**

This is comparable to the old workflow but with much better results!

## Future Enhancements

Potential improvements to build on this foundation:

1. **Intelligent Segmentation**
   - Automatically detect natural break points in narration
   - Adjust segment timings based on speech patterns

2. **Voice Customization**
   - Select from multiple voice options
   - Adjust speech rate for tighter/looser pacing

3. **Multi-Language Support**
   - Generate scripts in different languages
   - Use language-specific voice models

4. **Custom Styling**
   - Let users define color palettes
   - Customize animation effects per segment

5. **Interactive Timeline**
   - Show animation preview with narration
   - Let users adjust timing before final render

6. **Batch Processing**
   - Queue multiple videos
   - Optimize resource usage

## Troubleshooting

### Video is too long/short
- Check if audio duration is being detected correctly
- Verify `get_audio_duration()` returns expected value
- Check audio_duration being passed to Manim code generator

### Audio out of sync
- Ensure `render_video()` is called without text_input
- Verify `combine_audio_video()` is using correct parameters
- Check ffmpeg command in combine function

### Generic animations not matching topic
- Check if script_data is being passed correctly
- Verify Manim code generator prompt includes full script
- Review generated Manim code for segment alignment

### Always same template
- Verify `generate_adaptive_manim_code()` is being called
- Check if old `generate_manim_code()` is still being used somewhere
- Ensure script_data.segments are being included in prompt

## Migration from Old Workflow

The old `generate_manim_code()` function is still available but not used in the job processing flow. To fully migrate:

1. ✓ `process_job()` in app.py updated to use new workflow
2. ✓ New functions added to utils.py
3. ✓ Progress messages updated
4. Optional: Remove old `generate_manim_code()` after testing
5. Optional: Update frontend to show detailed progress steps

## Summary

The audio-first workflow represents a fundamental shift in how videos are generated:

- **Before:** Generate animation → Add voice → Hope they sync
- **Now:** Generate voice → Create animations to match → Perfect sync

This approach is more natural, more flexible, and produces better results!
