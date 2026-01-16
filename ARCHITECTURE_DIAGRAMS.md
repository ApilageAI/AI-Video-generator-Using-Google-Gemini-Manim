# System Architecture Diagram

## Overview Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     VIDEO GENERATION SYSTEM                     │
│                    (FLEXIBLE TEMPLATE VERSION)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────────┐    ┌─────────────┐    ┌──────────────────┐
   │  User Input │    │   Optional  │    │  Customization   │
   ├─────────────┤    │ Parameters  │    │  Parameters      │
   │ • text      │    ├─────────────┤    ├──────────────────┤
   │ • level     │    │ • style     │    │ • colors         │
   │             │    │ • duration  │    │ • objects        │
   └─────────────┘    └─────────────┘    └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Style Selection     │
                   ├──────────────────────┤
                   │ animated             │
                   │ minimal              │
                   │ mathematical         │
                   │ creative             │
                   │ technical            │
                   │ storytelling         │
                   └──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Load Style Guide     │
                   │ _get_style_guide()   │
                   └──────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
   │ Color        │  │ Elements     │  │ Style Guidelines │
   │ Palette      │  │ Selection    │  │ (70+ lines)      │
   └──────────────┘  └──────────────┘  └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Build Dynamic Prompt │
                   ├──────────────────────┤
                   │ • Topic              │
                   │ • Style guide        │
                   │ • Colors             │
                   │ • Elements           │
                   │ • Duration           │
                   │ • [PAUSE] markers    │
                   │ • Timing rules       │
                   └──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   Gemini API Call    │
                   │ generate_manim_code()│
                   └──────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
   │ Manim Code   │  │ Voice Script │  │ WebVTT Subtitles │
   │ (Custom      │  │ (with        │  │ (Synchronized)   │
   │  styled)     │  │  [PAUSE]     │  │                  │
   │              │  │  markers)    │  │                  │
   └──────────────┘  └──────────────┘  └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Audio Generation    │
                   │ generate_audio_with_ │
                   │ gemini()             │
                   └──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Duration Detection  │
                   │ Get audio duration   │
                   └──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Dynamic Adjustment  │
                   │ Extend/Compress      │
                   │ video to match audio │
                   └──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Combine Audio+Video  │
                   │ with perfect sync    │
                   └──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Return Response      │
                   ├──────────────────────┤
                   │ • video_url          │
                   │ • subtitles          │
                   │ • title              │
                   │ • level              │
                   │ • style (NEW)        │
                   │ • duration (NEW)     │
                   └──────────────────────┘
```

---

## Request Flow Diagram

```
┌──────────────────────────────────────┐
│      POST /api/generate              │
│  ┌────────────────────────────────┐  │
│  │ {                              │  │
│  │   "text": "My Topic",          │  │
│  │   "level": "intermediate",     │  │
│  │   "style": "technical",        │  │
│  │   "duration": 75,              │  │
│  │   "colors": ["BLUE_B", ...],   │  │
│  │   "objects": ["code_blocks"]   │  │
│  │ }                              │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│    Input Validation                  │
│  ✓ text present & valid length       │
│  ✓ level valid                       │
│  ✓ style valid (or use default)      │
│  ✓ duration valid (or use default)   │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  generate_manim_code(                │
│    text_input,                       │
│    level,                            │
│    style,          ← NEW              │
│    duration,       ← NEW              │
│    colors,         ← NEW              │
│    objects         ← NEW              │
│  )                                   │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  render_video(code, voice_script)    │
│  ├─ Compile Manim code               │
│  ├─ Generate audio                   │
│  ├─ Detect audio duration            │
│  ├─ Adjust video duration            │
│  └─ Combine audio + video            │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│      Response (200 OK)               │
│  ┌────────────────────────────────┐  │
│  │ {                              │  │
│  │   "video_url": "...",          │  │
│  │   "subtitles": "...",          │  │
│  │   "title": "...",              │  │
│  │   "level": "...",              │  │
│  │   "style": "technical",        │ (NEW)
│  │   "duration": 77               │ (NEW)
│  │ }                              │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

---

## Data Flow Diagram

```
                    INPUT
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌────────┐   ┌────────┐   ┌────────────┐
   │  text  │   │ level  │   │ optional:  │
   │        │   │        │   │ style,     │
   │        │   │        │   │ colors,    │
   │        │   │        │   │ duration,  │
   │        │   │        │   │ objects    │
   └────────┘   └────────┘   └────────────┘
        │             │             │
        │             │      ┌──────┴──────┐
        │             │      │             │
        │             │      ▼             ▼
        │             │  ┌────────────────────────┐
        │             │  │ Set Defaults by Style  │
        │             │  ├────────────────────────┤
        │             │  │ colors = color_palette │
        │             │  │ objects = elem_list    │
        │             │  └────────────────────────┘
        │             │      │             │
        └─────────────┼──────┼─────────────┘
                      │      │
                      ▼      ▼
             ┌──────────────────────────┐
             │  Load Style Guidelines   │
             │  _get_style_guide()      │
             └──────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │ Style   │  │ Color    │  │ Element  │
   │ Tips    │  │ Info     │  │ Tips     │
   └─────────┘  └──────────┘  └──────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Build Dynamic Prompt    │
             │  with all parameters     │
             └──────────────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Call Gemini API         │
             │  model.generate_content()│
             └──────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ Manim    │  │ Voice    │  │ Subtitles│
   │ Code     │  │ Script   │  │          │
   └──────────┘  └──────────┘  └──────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Generate Audio          │
             │  from Voice Script       │
             └──────────────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Render Manim Video      │
             └──────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
   ┌──────────────┐        ┌────────────────┐
   │ Video File   │        │ Audio Duration │
   │ (before sync)│        │ (in seconds)   │
   └──────────────┘        └────────────────┘
         │                         │
         └────────────┬────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │ Compare Durations        │
             │ If video < audio:        │
             │   Extend video           │
             │ If video > audio:        │
             │   (rare, trim/speed up)  │
             └──────────────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Combine Audio + Video   │
             │  ffmpeg merge            │
             └──────────────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Final MP4 Video         │
             │  (perfect sync)          │
             └──────────────────────────┘
                      │
                      ▼
             ┌──────────────────────────┐
             │  Return Response         │
             │  ├─ video_url            │
             │  ├─ subtitles            │
             │  ├─ title                │
             │  ├─ level                │
             │  ├─ style (NEW)          │
             │  └─ duration (NEW)       │
             └──────────────────────────┘
```

---

## Style Selection Flow

```
┌─────────────────────────────────────────┐
│         User Requests Video             │
│  Specifies: style = "mathematical"      │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│   _get_style_guide("mathematical")      │
└─────────────────────────────────────────┘
                 │
     ┌───────────┼───────────┬───────────┐
     │           │           │           │
     ▼           ▼           ▼           ▼
 ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
 │Use     │ │Include │ │Show    │ │Precise │
 │blue/   │ │formulas│ │step-by │ │        │
 │red/    │ │axes    │ │step    │ │position│
 │green   │ │graphs  │ │using   │ │        │
 │        │ │        │ │Transf  │ │        │
 └────────┘ └────────┘ └────────┘ └────────┘
     │           │           │           │
     └───────────┼───────────┴───────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ MATHEMATICAL STYLE GUIDE:      │
    │                                │
    │ "Use mathematical color        │
    │ conventions: blue for unknowns, │
    │ red for errors/special,        │
    │ green for solutions.           │
    │ Include formulas, equations... │
    │ Show step-by-step derivations  │
    │ using Transform. Include       │
    │ geometric diagrams and ...     │
    │ Precise positioning and        │
    │ alignment."                    │
    └────────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ Insert into Prompt             │
    │ "STYLE: mathematical           │
    │ {style_guide_text}"            │
    └────────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ Send to Gemini with full       │
    │ mathematical instructions      │
    └────────────────────────────────┘
```

---

## Component Interaction Diagram

```
┌─────────────────┐
│   app.py        │
│  /generate      │
│  endpoint       │
└────────┬────────┘
         │
         │ calls
         ▼
┌─────────────────────────────────┐
│   utils.py                      │
│  generate_manim_code()          │
├─────────────────────────────────┤
│ 1. Calls _get_style_guide()    │
│ 2. Loads default colors/elements│
│ 3. Builds dynamic prompt        │
│ 4. Calls Gemini API             │
│ 5. Parses response              │
│ 6. Sanitizes code               │
│ 7. Returns (code, script, subs) │
└────────┬────────────────────────┘
         │
         │ returns
         ▼
┌─────────────────────────────────┐
│   utils.py                      │
│  render_video()                 │
├─────────────────────────────────┤
│ 1. Saves Manim code to file     │
│ 2. Runs Manim compiler          │
│ 3. Renders video                │
│ 4. Calls generate_audio_with_   │
│    gemini()                     │
│ 5. Gets audio duration          │
│ 6. Extends video if needed      │
│ 7. Combines audio + video       │
│ 8. Returns video path           │
└────────┬────────────────────────┘
         │
         │ returns
         ▼
┌─────────────────────────────────┐
│   app.py                        │
│  Return Response                │
├─────────────────────────────────┤
│ {                               │
│   "video_url": "...",           │
│   "subtitles": "...",           │
│   "title": "...",               │
│   "level": "...",               │
│   "style": "...",  ← NEW        │
│   "duration": ...   ← NEW       │
│ }                               │
└─────────────────────────────────┘
```

---

## Synchronization Timeline

```
Voice Script with [PAUSE] Markers:
"Welcome to this lesson. [PAUSE 2s]
Let me explain. [PAUSE 3s]
Here's an example. [PAUSE 2s]
Summary. [PAUSE 2s]"

Timeline:
0s ─────────────── 2s ─────────────── 5s ─────────────── 7s ─────────────── 9s

Narration:
"Welcome to     [quiet]    "Let me      [quiet]    "Here's an  [quiet]    "Summary"
 this lesson"              explain"                example"

Animation:
FadeIn(intro)   [PAUSE]    Write(def)    [PAUSE]   Show(ex)     [PAUSE]   Text(sum)
└─── 1s ───┘    2s        └──── 2s ─────┘ 3s       └─ 1.5s ──┘   2s       └─ 1s ──┘
  Total: 1+2=3s    3+2=5s    5+2.5=7.5s  7.5+2=9.5s
```

This ensures perfect synchronization between narration and visuals!

---

## Benefits Comparison Diagram

```
BEFORE (Single Template)          AFTER (Flexible Templates)
─────────────────────────────     ──────────────────────────

Math Video:                       Math Video:
┌──────────────────────┐         ┌──────────────────────┐
│ Animated style       │         │ Mathematical style   │
│ Generic colors       │    →    │ Custom colors        │
│ Generic elements     │         │ Math elements        │
│ No sync              │         │ Perfect sync         │
└──────────────────────┘         └──────────────────────┘

Code Video:                       Code Video:
┌──────────────────────┐         ┌──────────────────────┐
│ Animated style       │         │ Technical style      │
│ Generic colors       │    →    │ Professional colors  │
│ Generic elements     │         │ Code blocks          │
│ No sync              │         │ Perfect sync         │
└──────────────────────┘         └──────────────────────┘

History Video:                    History Video:
┌──────────────────────┐         ┌──────────────────────┐
│ Animated style       │         │ Storytelling style   │
│ Generic colors       │    →    │ Warm colors          │
│ Generic elements     │         │ Narrative elements   │
│ No sync              │         │ Perfect sync         │
└──────────────────────┘         └──────────────────────┘

Result:                           Result:
❌ All look the same              ✅ Each looks perfect
❌ Generic                        ✅ Specialized
❌ No customization               ✅ Full control
❌ Basic sync                      ✅ Perfect sync
```

---

**Architecture Complete!** ✅

All diagrams show how the flexible template system works with:
- Multiple style options
- Customizable parameters
- Dynamic prompt generation
- Perfect audio-video synchronization
