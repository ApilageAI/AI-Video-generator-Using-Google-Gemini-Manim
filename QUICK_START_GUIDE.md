# Quick Start Guide - Video Customization

## 30-Second Overview

The system now supports **6 video styles** with **custom colors** and **visual elements** instead of using the same template for everything.

---

## 5-Minute Setup

### Step 1: Update Your API Call

**Old way (still works):**
```json
{
    "text": "Your Topic",
    "level": "basic"
}
```

**New way (with customization):**
```json
{
    "text": "Your Topic",
    "level": "basic",
    "style": "animated",
    "colors": ["GOLD", "BLUE_B", "GREEN_B"],
    "duration": 60
}
```

### Step 2: Choose Your Style

Pick one of these 6:

| Style | Best For | Look |
|-------|----------|------|
| **animated** | General topics | Colorful, lively |
| **minimal** | Business, corporate | Clean, professional |
| **mathematical** | Math, physics | Formulas, equations |
| **creative** | Arts, history | Artistic, visual |
| **technical** | Programming, IT | Code, diagrams |
| **storytelling** | Narratives, cases | Scene-based |

### Step 3: Pick Your Colors

Choose any 3-5 Manim colors:

```
Primary: WHITE, BLACK, BLUE, RED, GREEN, YELLOW, ORANGE, PINK, PURPLE, GOLD, TEAL

Light: BLUE_A, RED_A, GREEN_A... (add _A for lighter)
Dark:  BLUE_E, RED_E, GREEN_E... (add _E for darker)

Special: DARK_GRAY, LIGHT_GRAY, GRAY
```

### Step 4: Select Visual Elements

Choose what to include in your video:

```json
"objects": [
    "boxes",           // RoundedRectangle shapes
    "arrows",          // Direction indicators
    "circles",         // Circular elements
    "stars",           // Decorative stars
    "icons",           // Simple symbols
    "formulas",        // Math equations
    "diagrams",        // Visual diagrams
    "code_blocks",     // Code snippets
    "flowcharts",      // Process flows
    "text"             // Just text
]
```

### Step 5: Set Duration

Target video length in seconds (will auto-adjust to match audio):

```json
"duration": 60  // or 45, 75, 90, etc.
```

### Step 6: Send Request

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your topic",
    "level": "basic",
    "style": "animated",
    "duration": 60,
    "colors": ["GOLD", "BLUE_B", "GREEN_B"],
    "objects": ["circles", "arrows", "text"]
  }'
```

---

## Real-World Examples

### Example 1: Math Tutorial
```json
{
    "text": "Solving Quadratic Equations",
    "level": "intermediate",
    "style": "mathematical",
    "duration": 70,
    "colors": ["BLUE_E", "WHITE", "RED_B", "GREEN_B"],
    "objects": ["formulas", "arrows", "diagrams"]
}
```

### Example 2: Programming Lesson
```json
{
    "text": "REST API Design Patterns",
    "level": "advanced",
    "style": "technical",
    "duration": 75,
    "colors": ["BLUE_B", "DARK_GRAY", "GREEN_B"],
    "objects": ["code_blocks", "flowcharts", "arrows"]
}
```

### Example 3: History Lecture
```json
{
    "text": "The Industrial Revolution",
    "level": "intermediate",
    "style": "storytelling",
    "duration": 80,
    "colors": ["GOLD", "RED_B", "PURPLE_A"],
    "objects": ["text", "circles", "decorative elements"]
}
```

### Example 4: Science Explanation
```json
{
    "text": "The Water Cycle",
    "level": "basic",
    "style": "creative",
    "duration": 60,
    "colors": ["BLUE_B", "GREEN_B", "GOLD", "TEAL_A"],
    "objects": ["circles", "arrows", "decorative elements"]
}
```

### Example 5: Business Training
```json
{
    "text": "Project Management Best Practices",
    "level": "intermediate",
    "style": "minimal",
    "duration": 60,
    "colors": ["WHITE", "DARK_GRAY", "BLUE_E"],
    "objects": ["rectangles", "text", "arrows"]
}
```

---

## Cheat Sheet

### Copy-Paste Templates

#### Math Content
```json
{
    "text": "YOUR_TOPIC",
    "level": "intermediate",
    "style": "mathematical",
    "duration": 70,
    "colors": ["BLUE_E", "WHITE", "RED_B", "GREEN_B"],
    "objects": ["formulas", "diagrams", "arrows"]
}
```

#### Programming Content
```json
{
    "text": "YOUR_TOPIC",
    "level": "intermediate",
    "style": "technical",
    "duration": 75,
    "colors": ["BLUE_B", "DARK_GRAY", "GREEN_B"],
    "objects": ["code_blocks", "flowcharts", "arrows"]
}
```

#### Creative Content
```json
{
    "text": "YOUR_TOPIC",
    "level": "basic",
    "style": "creative",
    "duration": 65,
    "colors": ["GOLD", "PURPLE_A", "TEAL_A", "PINK"],
    "objects": ["shapes", "gradients", "decorative elements"]
}
```

#### Business Content
```json
{
    "text": "YOUR_TOPIC",
    "level": "intermediate",
    "style": "minimal",
    "duration": 60,
    "colors": ["WHITE", "DARK_GRAY", "BLUE_E"],
    "objects": ["rectangles", "text", "arrows"]
}
```

#### General Content
```json
{
    "text": "YOUR_TOPIC",
    "level": "basic",
    "style": "animated",
    "duration": 60,
    "colors": ["GOLD", "BLUE_B", "GREEN_B", "ORANGE"],
    "objects": ["boxes", "arrows", "circles", "icons"]
}
```

---

## Parameter Reference

```
text           (REQUIRED) - Your topic (3-500 characters)
level          (optional) - "basic" | "intermediate" | "special_topic"
style          (optional) - See 6 styles below
duration       (optional) - Seconds (30-120, default: 60)
colors         (optional) - Array of Manim color names
objects        (optional) - Array of visual element types
```

### 6 Styles Quick Reference
```
animated       → Colorful, lively, decorative elements
minimal        → Clean, professional, monochrome
mathematical   → Formulas, equations, precise
creative       → Artistic, visual, metaphors
technical      → Code, diagrams, professional
storytelling   → Scenes, narrative, characters
```

### Common Colors
```
Warm:   GOLD, ORANGE, RED_B, PINK, PURPLE_A
Cool:   BLUE_B, TEAL_A, GREEN_B, CYAN
Neutral: WHITE, DARK_GRAY, LIGHT_GRAY, BLUE_E
```

### Common Visual Elements
```
Basic:      text, rectangles, circles, lines
Shapes:     boxes, arrows, stars, icons
Diagrams:   flowcharts, code_blocks, diagrams
Advanced:   gradients, patterns, decorative elements
```

---

## How It Works

1. **You send:** Custom parameters (style, colors, objects, duration)
2. **System loads:** Style-specific guidelines
3. **AI creates:** Unique video matching your specs
4. **Generator:** Builds animations with your colors
5. **Audio:** Narration auto-syncs with video
6. **Result:** Professional video matching your requirements

---

## What Changed

**Before:** Same template for every video
```
Math video → animated style with generic colors
Programming video → animated style with generic colors  
History video → animated style with generic colors
(All look the same)
```

**After:** Custom template per video
```
Math video → mathematical style with blue/red/green + formulas
Programming video → technical style with dark colors + code
History video → storytelling style with warm colors + scenes
(Each looks perfect for its type)
```

---

## Pro Tips

### ✅ DO:
- Use style matching your content type
- Pick 3-5 colors for consistency
- Include relevant visual elements
- Set duration close to expected narration
- Test with simple topics first

### ❌ DON'T:
- Mix conflicting styles (technical + creative)
- Use too many colors (stick to 5 max)
- Set duration too short (min 30s)
- Request elements unrelated to style
- Forget to include the "text" parameter

---

## Common Combinations

### 🎓 Educational
- Style: `animated` or `mathematical`
- Colors: `BLUE_B`, `WHITE`, `GREEN_B`
- Objects: `boxes`, `arrows`, `text`

### 💼 Corporate
- Style: `minimal`
- Colors: `WHITE`, `DARK_GRAY`, `BLUE_E`
- Objects: `rectangles`, `text`, `arrows`

### 🎨 Creative
- Style: `creative`
- Colors: `GOLD`, `PURPLE_A`, `TEAL_A`
- Objects: `shapes`, `gradients`, `decorative elements`

### 💻 Technical
- Style: `technical`
- Colors: `BLUE_B`, `DARK_GRAY`, `GREEN_B`
- Objects: `code_blocks`, `flowcharts`, `diagrams`

### 📖 Storytelling
- Style: `storytelling`
- Colors: `GOLD`, `RED_B`, `GREEN_A`
- Objects: `circles`, `arrows`, `text`

---

## Testing

### Quick Test
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World", "style": "animated"}'
```

### Full Test
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Understanding Gravity",
    "level": "basic",
    "style": "creative",
    "duration": 60,
    "colors": ["GOLD", "BLUE_B", "GREEN_B"],
    "objects": ["circles", "arrows", "decorative elements"]
  }'
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Video looks rushed | Increase duration parameter |
| Colors don't show | Use valid Manim color names |
| Elements missing | Check objects parameter spelling |
| Audio out of sync | Video auto-adjusted, this is normal |
| Style not applied | Restart server, check style spelling |

---

## Next Steps

1. ✅ Read [STYLE_AND_CUSTOMIZATION_GUIDE.md](STYLE_AND_CUSTOMIZATION_GUIDE.md) for details
2. ✅ Check [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md) for API specs
3. ✅ Review [BEFORE_AND_AFTER.md](BEFORE_AND_AFTER.md) for comparisons
4. 🚀 Start creating custom videos!

---

## Support

For detailed information:
- **User Guide:** STYLE_AND_CUSTOMIZATION_GUIDE.md
- **Developer Guide:** IMPLEMENTATION_CHANGES.md
- **Technical Reference:** TECHNICAL_REFERENCE.md
- **API Examples:** TECHNICAL_REFERENCE.md
- **Architecture:** BEFORE_AND_AFTER.md

---

## Success! 🎉

You now have a flexible, customizable video generation system that creates unique, professional videos matching your exact requirements!

**Key Benefits:**
✅ No more generic templates
✅ Videos match content type
✅ Perfect audio sync
✅ Brand customization
✅ Professional quality
✅ Full user control
