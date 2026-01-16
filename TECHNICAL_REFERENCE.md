# Technical Reference - Video Generation System

## Function Signatures

### `_get_style_guide(style: str) -> str`

Returns style-specific design instructions from the style guides dictionary.

**Parameters:**
- `style` (str): One of: "animated", "minimal", "mathematical", "creative", "technical", "storytelling"

**Returns:**
- `str`: Multi-line style guide text for use in prompt

**Example:**
```python
guide = _get_style_guide("mathematical")
# Returns: "MATHEMATICAL STYLE (Precise, Analytical...)"
```

---

### `generate_manim_code(text_input, level="basic", style=None, duration=None, colors=None, objects=None) -> tuple`

Generates Manim animation code and voice script using Gemini AI with customizable styling.

**Parameters:**
- `text_input` (str, required): Topic or content for the video
- `level` (str, optional): "basic", "intermediate", or "special_topic" (default: "basic")
- `style` (str, optional): "animated", "minimal", "mathematical", "creative", "technical", "storytelling" (default: "animated")
- `duration` (int, optional): Target video length in seconds (default: 60)
- `colors` (list, optional): List of Manim color names (default: style-specific)
- `objects` (list, optional): List of visual element types (default: style-specific)

**Returns:**
- `tuple[str, str, str]`: (manim_code, voice_script, subtitles)

**Raises:**
- `ValueError`: If GEMINI_API_KEY not set
- `Exception`: If Gemini API call fails

**Example:**
```python
code, script, subs = generate_manim_code(
    "Understanding Photosynthesis",
    level="intermediate",
    style="creative",
    duration=75,
    colors=["GREEN_B", "GOLD", "BLUE_B"],
    objects=["circles", "arrows", "text"]
)
```

---

## API Endpoint: POST /generate

### Request Format
```json
{
    "text": "string (required, 3-500 chars)",
    "level": "string (optional: 'basic'|'intermediate'|'special_topic')",
    "style": "string (optional: style name)",
    "duration": "integer (optional: seconds)",
    "colors": "array of strings (optional)",
    "objects": "array of strings (optional)"
}
```

### Response Format (Success: 200)
```json
{
    "video_url": "string (relative path to video)",
    "subtitles": "string (WebVTT format)",
    "title": "string (first 50 chars of text)",
    "level": "string (echoed from request)",
    "style": "string (echoed from request)",
    "duration": "integer (actual video duration in seconds)"
}
```

### Response Format (Error: 4xx/5xx)
```json
{
    "error": "string (user-friendly error message)"
}
```

**Error Codes:**
- `400`: Missing text or invalid input
- `429`: Rate limit exceeded
- `500`: Video generation failed

### Example Requests

#### Minimal Request
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "What is Photosynthesis"}'
```

#### Complete Request
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Understanding DNA Replication",
    "level": "intermediate",
    "style": "mathematical",
    "duration": 70,
    "colors": ["BLUE_E", "WHITE", "RED_B", "GREEN_B"],
    "objects": ["formulas", "diagrams", "arrows"]
  }'
```

---

## Style Definitions

### Default Color Palettes
```python
{
    "animated": ["GOLD", "BLUE_B", "GREEN_B", "PINK", "ORANGE", "TEAL_A", "YELLOW"],
    "minimal": ["WHITE", "DARK_GRAY", "LIGHT_GRAY", "BLUE_E"],
    "mathematical": ["BLUE_E", "WHITE", "YELLOW", "RED_B", "GREEN_B"],
    "creative": ["PINK", "PURPLE_A", "GOLD", "TEAL_A", "RED_A"],
    "technical": ["BLUE_B", "DARK_GRAY", "GREEN_B", "ORANGE"],
    "storytelling": ["GOLD", "RED_B", "GREEN_A", "BLUE_A", "PURPLE_A"]
}
```

### Default Visual Elements
```python
{
    "animated": ["boxes", "arrows", "circles", "stars", "icons"],
    "minimal": ["text", "lines", "rectangles"],
    "mathematical": ["formulas", "diagrams", "axes", "graphs"],
    "creative": ["shapes", "gradients", "patterns", "decorative elements"],
    "technical": ["diagrams", "code blocks", "flowcharts", "data structures"],
    "storytelling": ["scenes", "characters", "transitions", "narrative elements"]
}
```

---

## Voice Script Format

### With Pause Markers
```
[narration text] [PAUSE Xs] [more narration] [PAUSE Ys]
```

### Pause Duration Guide
- `[PAUSE 1s]` - Quick transition, short animation
- `[PAUSE 2s]` - Standard animation, normal pace
- `[PAUSE 3s]` - Complex animation, emphasis
- `[PAUSE 4s+]` - Extended animation, long explanation

### Duration Calculation
```
Total words ÷ 2.5 = Duration in seconds
Example: 150 words ÷ 2.5 = 60 seconds
```

---

## Manim Color Reference

### Primary Colors
- `WHITE`, `BLACK`
- `RED`, `BLUE`, `GREEN`, `YELLOW`, `ORANGE`, `PINK`, `PURPLE`, `TEAL`, `GOLD`

### Color Variations (Light to Dark)
- `BLUE_A` (lightest), `BLUE_B`, `BLUE_C`, `BLUE_D`, `BLUE_E` (darkest)
- Same pattern for: RED, GREEN, YELLOW, ORANGE, PINK, PURPLE, TEAL

### Special Colors
- `DARK_GRAY`, `LIGHT_GRAY`, `GRAY`
- `DARK_BLUE`, `DARK_GREEN`, `DARK_RED`

---

## Manim Animation Types by Style

### Animated Style
- `Write` - Text appears character by character
- `FadeIn`, `FadeOut` - Smooth fade transitions
- `GrowFromCenter` - Shape grows from center
- `Create` - Draw geometric shapes
- `Indicate` - Pulse/highlight effect
- `Transform` - Morph between objects
- `SpinInFromNothing` - Dramatic spin entrance

### Minimal Style
- `Write` - Text animation
- `FadeIn`, `FadeOut` - Fade effects only
- `Create` - Basic shape drawing
- No decorative animations

### Mathematical Style
- `Write` - For text and formulas
- `Transform` - Step-by-step derivations
- `FadeIn`, `FadeOut` - Transitions
- `Create` - For geometric shapes
- `DrawBorderThenFill` - For highlighted areas

### Creative Style
- All animation types allowed
- Multiple simultaneous animations
- Unusual transitions
- Decorative effects

### Technical Style
- `Write` - For code and text
- `FadeIn`, `FadeOut` - Clean transitions
- `Create` - For diagrams
- `Transform` - Between diagrams

### Storytelling Style
- `FadeIn`, `FadeOut` - Scene transitions
- `Write` - Narration-synchronized
- `Transform` - Scene changes
- `Create` - Adding story elements

---

## WebVTT Subtitle Format

```
WEBVTT

00:00:00.000 --> 00:00:03.000
First subtitle text

00:00:03.000 --> 00:00:06.500
Second subtitle text

00:00:06.500 --> 00:00:10.000
Third subtitle text
```

**Timing Considerations:**
- Sync with narration timing
- 3-5 second segments typical
- Account for animation duration
- Include [PAUSE] markers as timing references

---

## System Prompt Sections

The Gemini prompt includes these key sections:

1. **Request Metadata** (ID, topic, level)
2. **Style Guidelines** (from _get_style_guide)
3. **Color Palette Instructions**
4. **Visual Element Instructions**
5. **Timing & Sync Rules** (using duration parameter)
6. **Zero Overlap Rules** (prevent animation conflicts)
7. **Text Rules** (prevent overflow)
8. **Animation Duration Specifications**
9. **Mandatory Ending Sequence** (Apilage AI branding)
10. **Complete Template Example**
11. **Math/Derivation Examples** (for mathematical style)
12. **Visual Elements Library**
13. **Voice Script Format** (with pause markers)
14. **Subtitles Format** (WebVTT)

---

## Error Handling

### Input Validation
```python
if not text_input:
    return {'error': 'No text provided'}

if len(text_input) < 3:
    return {'error': 'Description too short'}

if len(text_input) > 500:
    return {'error': 'Description too long'}
```

### API Error Masking
Gemini/API errors are caught and replaced with user-friendly messages:
- Syntax errors → "Problem with animation code"
- Timeout → "Rendering took too long"
- Manim errors → "Animation rendering failed"
- Other → Generic error message

### Logging Format
```
[GENERATE REQUEST]
Topic: 'Topic here'
Level: level
Style: style
Duration: Xs (will adjust to match audio)
Colors: [COLOR1, COLOR2]
Objects: [ELEMENT1, ELEMENT2]
```

---

## Performance Considerations

### Processing Time
- API call to Gemini: 5-15 seconds
- Manim rendering: 10-30 seconds (varies with complexity)
- Audio generation: 2-5 seconds
- Audio+Video combine: 3-10 seconds
- **Total: 20-60 seconds per video**

### Rate Limiting
- 10 requests per hour per IP
- Returns 429 status if exceeded
- Limits are in-memory (reset on restart)

### Resource Usage
- Temporary file creation for intermediate files
- Automatic cleanup of temp files
- Video storage in `/uploads` and `/videos` directories

---

## Integration Example

```python
import requests
import json

# Configuration
API_URL = "http://localhost:5000/api/generate"
HEADERS = {"Content-Type": "application/json"}

# Request data
payload = {
    "text": "Understanding Blockchain",
    "level": "intermediate",
    "style": "technical",
    "duration": 75,
    "colors": ["BLUE_B", "DARK_GRAY", "GREEN_B"],
    "objects": ["diagrams", "code_blocks", "flowcharts"]
}

# Make request
response = requests.post(API_URL, json=payload, headers=HEADERS)

# Handle response
if response.status_code == 200:
    data = response.json()
    print(f"Video URL: {data['video_url']}")
    print(f"Style: {data['style']}")
    print(f"Duration: {data['duration']}s")
    print(f"Subtitles: {data['subtitles'][:100]}...")
else:
    print(f"Error: {response.json()['error']}")
```

---

## Debugging Tips

### 1. Check Prompt Construction
```python
# In generate_manim_code, before sending to Gemini:
print(f"Prompt length: {len(prompt)}")
print(f"Style guide length: {len(style_guide)}")
```

### 2. Validate Response Parsing
```python
# Check if response contains all three parts:
has_code = "MANIM_CODE:" in content
has_script = "VOICE_SCRIPT:" in content
has_subs = "SUBTITLES:" in content
```

### 3. Monitor File Operations
```python
# Check generated files exist:
print(f"Code file exists: {os.path.exists(code_path)}")
print(f"Audio file exists: {os.path.exists(audio_path)}")
print(f"Video file exists: {os.path.exists(video_path)}")
```

### 4. Validate Audio Sync
```python
# Check durations match:
print(f"Video duration: {video_duration}s")
print(f"Audio duration: {audio_duration}s")
print(f"Match: {abs(video_duration - audio_duration) < 1}")
```

---

## Environment Variables

Required in `.env`:
```
GEMINI_API_KEY=your_api_key_here
AUTH_CODE=your_auth_code
API_KEY=your_api_key
```

---

## Success Criteria

✅ API accepts new parameters
✅ Style guides applied correctly
✅ Custom colors used in video
✅ Custom objects included in video
✅ Voice script has [PAUSE] markers
✅ Subtitles sync with audio
✅ Video duration matches audio
✅ Backward compatible (old requests work)
✅ Error handling robust
✅ Logging informative
