# Video Style and Customization Guide

## Overview

The improved video generation system now supports **flexible templates and custom styling** instead of using the same template for all videos. This allows for better alignment with user requirements and improved audio-video synchronization.

## Key Improvements

### 1. **Flexible Video Styles**

Instead of a one-size-fits-all template, choose from 6 distinct styles:

#### Available Styles:

- **`animated`** - Colorful, Lively, Engaging
  - Bright, vibrant colors with high saturation
  - Multiple animation types (Write, FadeIn, GrowFromCenter, Transform, Create, Indicate)
  - Decorative elements (stars, circles, arrows, bouncing effects)
  - Smooth, flowing transitions with pulse effects
  - Best for: General educational content, younger audiences

- **`minimal`** - Clean, Simple, Professional
  - Grayscale or monochrome color scheme
  - Basic animations (Write, FadeIn, FadeOut)
  - Single object per slide
  - Professional, elegant transitions
  - Best for: Corporate training, technical documentation

- **`mathematical`** - Precise, Analytical, Diagram-focused
  - Mathematical color conventions (blue, red, green)
  - Formulas, equations, MathTex notation
  - Axes, grids, graphs, coordinate systems
  - Step-by-step derivations using Transform
  - Best for: Math, Physics, Engineering content

- **`creative`** - Artistic, Imaginative, Visually Rich
  - Diverse, complementary color palettes
  - Unusual animations and transitions
  - Artistic elements, gradients, patterns
  - Visual metaphors and symbolic representations
  - Best for: Creative subjects, storytelling content

- **`technical`** - Structured, Code-focused, Diagram-heavy
  - Dark backgrounds with bright accent colors
  - Code blocks, syntax highlighting
  - Flowcharts, diagrams, system architecture
  - Hierarchical relationships and data structures
  - Best for: Programming, Software Architecture, IT content

- **`storytelling`** - Narrative-driven, Scene-based, Character-focused
  - Warm, inviting color palettes
  - Narrative scenes and scenarios
  - Character elements and personas
  - Suspenseful reveals with gradual information
  - Best for: History, Literature, narrative content

### 2. **Custom Color Palettes**

Define your own color scheme for the video:

```python
# Example: Modern tech colors
colors = ["BLUE_B", "DARK_GRAY", "GREEN_B", "ORANGE"]

# Example: Warm creative colors
colors = ["GOLD", "RED_A", "PURPLE_A", "TEAL_A"]

# Example: Mathematical style
colors = ["BLUE_E", "WHITE", "YELLOW", "RED_B", "GREEN_B"]
```

Supported color names include all Manim colors:
- Primary: `WHITE`, `BLACK`, `BLUE`, `RED`, `GREEN`, `YELLOW`, `ORANGE`, `PINK`, `PURPLE`, `GOLD`, `TEAL`
- Variations: `BLUE_A`, `BLUE_B`, `BLUE_C`, `BLUE_D`, `BLUE_E` (light to dark)
- Special: `DARK_GRAY`, `LIGHT_GRAY`, `GRAY`

### 3. **Custom Visual Elements**

Specify which visual elements to include:

```python
# Example: Animated style with decorative elements
objects = ["boxes", "arrows", "circles", "stars", "icons"]

# Example: Mathematical style with formulas
objects = ["formulas", "diagrams", "axes", "graphs"]

# Example: Technical style with code
objects = ["code_blocks", "flowcharts", "data_structures"]
```

Available elements by category:
- **Basic**: text, lines, rectangles, circles
- **Decorative**: stars, arrows, icons, patterns
- **Diagrams**: boxes, graphs, axes, flowcharts
- **Math**: formulas, equations, geometric shapes
- **Code**: code blocks, syntax highlighting
- **Advanced**: gradients, textures, transformations

### 4. **Dynamic Duration Management**

Video length now adapts to match audio narration:

```python
# Request with specific target duration
{
    "text": "Understanding Photosynthesis",
    "level": "basic",
    "style": "animated",
    "duration": 60  // Target 60 seconds (auto-adjusted to match audio)
}
```

The system:
- ✅ Calculates expected narration duration
- ✅ Adjusts animation timing to match
- ✅ Ensures clean audio-video synchronization
- ✅ Adds pauses where needed for visual emphasis

### 5. **Improved Audio-Video Synchronization**

New features for better sync:

- **Timing Calculations**: Narration is timed based on word count (~150 words/minute)
- **[PAUSE] Markers**: Voice script includes pause timing cues
- **Animation Duration**: Each animation matched to speech content
- **Synchronized Subtitles**: WebVTT subtitles align with both audio and video
- **Natural Pacing**: Automatic adjustment to prevent rushed animations

## API Usage

### Basic Request (Using Defaults)
```json
POST /generate
{
    "text": "The Water Cycle",
    "level": "basic"
}
```
Result: Uses default animated style with standard colors

### Customized Request
```json
POST /generate
{
    "text": "The Water Cycle",
    "level": "intermediate",
    "style": "creative",
    "duration": 75,
    "colors": ["BLUE_B", "TEAL_A", "WHITE", "GOLD"],
    "objects": ["arrows", "circles", "decorative elements"]
}
```

### Technical Content Example
```json
POST /generate
{
    "text": "HTTP Request Protocol",
    "level": "intermediate",
    "style": "technical",
    "duration": 60,
    "colors": ["BLUE_B", "DARK_GRAY", "GREEN_B"],
    "objects": ["code_blocks", "flowcharts", "arrows"]
}
```

### Mathematical Content Example
```json
POST /generate
{
    "text": "Solving Quadratic Equations",
    "level": "intermediate",
    "style": "mathematical",
    "duration": 70,
    "colors": ["BLUE_E", "WHITE", "RED_B", "GREEN_B"],
    "objects": ["formulas", "diagrams", "arrows"]
}
```

## How It Works

### 1. Style Detection
- AI analyzes the requested style
- Loads style-specific design guidelines
- Applies appropriate animation patterns

### 2. Color Application
- Custom colors override default palettes
- Colors applied consistently throughout
- Ensures visual coherence

### 3. Duration Management
```
User Duration (60s) → Narration Analysis → Animation Timing → Video Rendering
                             ↓
                     Expected Duration
                             ↓
                   Adjust animations if needed
                             ↓
                    Audio+Video Combination
                             ↓
                  Final Duration = Audio Duration
```

### 4. Content Generation
```
Topic + Style + Colors + Objects → Gemini AI → Unique Video Code
                                        ↓
                                  Voice Script with Timing
                                        ↓
                                  Synchronized Subtitles
```

## Voice Script Timing

New voice script format includes timing cues:

```
"Welcome to this lesson on photosynthesis. [PAUSE 1s]
Let's explore what photosynthesis means. [PAUSE 2s]
Photosynthesis is the process where plants convert sunlight into chemical energy. [PAUSE 2s]
There are two main stages: light-dependent and light-independent reactions. [PAUSE 3s]
Let's summarize: Plants need sunlight, water, and carbon dioxide. [PAUSE 2s]
This video was created by Apilage AI. [PAUSE 2s]"
```

Pause markers indicate:
- `[PAUSE 1s]` - Quick visual transition (title change)
- `[PAUSE 2s]` - Standard animation duration (showing content)
- `[PAUSE 3s]` - Complex animation or emphasizing point

## Response Enhancement

API response now includes styling information:

```json
{
    "video_url": "/uploads/video.mp4",
    "title": "The Water Cycle",
    "level": "intermediate",
    "style": "creative",
    "duration": 68,
    "subtitles": "WEBVTT\n00:00:00.000 --> 00:00:03.000\nWelcome to this lesson..."
}
```

## Best Practices

### For Different Content Types:

**Science/Nature Content**
```json
{
    "style": "animated",
    "colors": ["GREEN_B", "BLUE_B", "YELLOW", "ORANGE"],
    "objects": ["circles", "arrows", "decorative elements"]
}
```

**Mathematics**
```json
{
    "style": "mathematical",
    "colors": ["BLUE_E", "WHITE", "RED_B", "GREEN_B"],
    "objects": ["formulas", "diagrams", "arrows"]
}
```

**Business/Corporate**
```json
{
    "style": "minimal",
    "colors": ["WHITE", "DARK_GRAY", "BLUE_B"],
    "objects": ["rectangles", "text", "lines"]
}
```

**Language Learning**
```json
{
    "style": "creative",
    "colors": ["GOLD", "TEAL_A", "PINK", "WHITE"],
    "objects": ["text", "circles", "arrows"]
}
```

**Programming**
```json
{
    "style": "technical",
    "colors": ["BLUE_B", "DARK_GRAY", "GREEN_B"],
    "objects": ["code_blocks", "flowcharts", "arrows"]
}
```

## Troubleshooting

### Issue: Video looks too rushed
**Solution**: Increase duration parameter or simplify narration

### Issue: Animations don't match narration
**Solution**: Check voice script pause markers and adjust duration

### Issue: Colors don't look right
**Solution**: Use official Manim color names with proper contrast

### Issue: Too many visual elements
**Solution**: Reduce objects list or simplify style

## Summary

This improved system provides:
- ✅ **Flexibility**: Choose style matching your content
- ✅ **Customization**: Tailor colors and elements to brand
- ✅ **Better Sync**: Audio and video perfectly matched
- ✅ **Professional Quality**: Style-appropriate animations
- ✅ **Unique Content**: No more same template for all videos
- ✅ **User Requirements**: Full control over visual appearance

Users can now create truly customized educational videos that perfectly match their specific needs and aesthetic preferences!
