import google.generativeai as genai
from google import genai as genai_new
from google.genai import types as genai_types
import os
import tempfile
import subprocess
import re
import ast
import struct
import mimetypes
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Gemini API
gemini_key = os.getenv("GEMINI_API_KEY", "")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please create a .env file with your API key.")
genai.configure(api_key=gemini_key)

# Set up new Gemini client for TTS
gemini_tts_client = genai_new.Client(api_key=gemini_key)


def validate_python_syntax(code):
    """
    Validate Python syntax and return any errors.
    Returns (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"


def sanitize_manim_code(code):
    """
    Clean and sanitize generated Manim code to fix common issues.
    Also ensures the Apilage AI ending is present and proper video structure.
    """
    # Remove any markdown code blocks if present
    code = re.sub(r'^```python\s*', '', code, flags=re.MULTILINE)
    code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
    
    # Ensure proper imports
    if 'from manim import' not in code and 'import manim' not in code:
        code = 'from manim import *\n\n' + code
    
    # Fix common issues
    # Remove any print statements that might interfere
    # code = re.sub(r'^\s*print\s*\(.*\)\s*$', '', code, flags=re.MULTILINE)
    
    # Ensure the class name is correct
    if 'class MathExplanationScene' not in code:
        # Try to find any Scene class and rename it
        code = re.sub(
            r'class\s+(\w+)\s*\(\s*Scene\s*\)',
            'class MathExplanationScene(Scene)',
            code,
            count=1
        )
    
    # Remove any external file references (images, SVGs, etc.)
    code = re.sub(r'ImageMobject\s*\([^)]*\)', 'Circle()', code)
    code = re.sub(r'SVGMobject\s*\([^)]*\)', 'Circle()', code)
    
    # Fix common color issues - replace invalid colors with valid ones
    invalid_colors = {
        'DARK_BLUE': 'BLUE_E',
        'LIGHT_BLUE': 'BLUE_A', 
        'DARK_GREEN': 'GREEN_E',
        'LIGHT_GREEN': 'GREEN_A',
        'DARK_RED': 'RED_E',
        'LIGHT_RED': 'RED_A',
    }
    for invalid, valid in invalid_colors.items():
        code = code.replace(invalid, valid)
    
    # Ensure Apilage AI ending is present
    if 'Apilage AI Video' not in code:
        # Find the last self.wait or end of construct method and add ending
        ending_code = '''
        # ===== APILAGE AI ENDING =====
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
        ending_bg = Rectangle(width=14, height=8, fill_color=BLUE_E, fill_opacity=0.5)
        ending_text = Text("Apilage AI Video", font_size=48, color=GOLD)
        ending_text.move_to(ORIGIN)
        self.play(FadeIn(ending_bg), run_time=0.5)
        self.play(FadeIn(ending_text, scale=0.8), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(ending_text), FadeOut(ending_bg))
        self.wait(0.5)
'''
        # Try to insert before the final line of the construct method
        if 'def construct(self):' in code:
            # Find position to insert ending
            lines = code.split('\n')
            insert_index = len(lines) - 1
            
            # Find the last non-empty line that's inside the construct method
            for i in range(len(lines) - 1, -1, -1):
                line = lines[i].strip()
                if line and not line.startswith('#'):
                    insert_index = i + 1
                    break
            
            # Get the indentation of the construct method body
            indent = '        '  # 8 spaces default
            for line in lines:
                if 'self.play' in line or 'self.wait' in line:
                    indent = line[:len(line) - len(line.lstrip())]
                    break
            
            # Add the ending code with proper indentation
            ending_lines = ending_code.strip().split('\n')
            indented_ending = '\n'.join([indent + line.strip() for line in ending_lines])
            
            lines.insert(insert_index, indented_ending)
            code = '\n'.join(lines)
    
    return code.strip()


def fix_manim_code_with_ai(code, error_message):
    """
    Use AI to fix Manim code based on the error message.
    """
    fix_prompt = f"""
    The following Manim code has an error. Please fix it and return ONLY the corrected Python code.
    
    Error: {error_message}
    
    Original Code:
    ```python
    {code}
    ```
    
    CRITICAL REQUIREMENTS:
    1. Fix the specific error mentioned
    2. Keep all animations and visual elements
    3. Ensure the class is named 'MathExplanationScene' and inherits from Scene
    4. Use only built-in Manim objects (no external images, SVGs, or files)
    5. Return ONLY the corrected Python code, no explanations
    6. Make sure all imports are correct (from manim import *)
    7. Ensure all variables are defined before use
    
    ABSOLUTE ZERO-OVERLAP RULES (MOST IMPORTANT):
    8. BEFORE every new section, add: self.play(*[FadeOut(mob) for mob in self.mobjects])
    9. NEVER show two text elements unless in a VGroup with buff=0.8+
    10. Show ONE thing at a time: title → fade → content → fade → next
    11. For derivations, use Transform(old, new), NOT add new elements
    12. Wait 0.3 seconds after every FadeOut: self.wait(0.3)
    
    VISUAL DESIGN RULES:
    13. Use colorful elements: GOLD for titles, GREEN_B for examples, BLUE_E for backgrounds
    14. Add RoundedRectangle backgrounds behind important text
    15. Use Dot(color=X) for bullet points
    16. Use Arrow() for showing relationships
    
    TEXT AND LAYOUT RULES:
    17. Titles: font_size=42 max, body: font_size=28-32
    18. Use .scale(0.7) for MathTex to ensure formulas fit
    19. Center everything: .move_to(ORIGIN)
    20. For long text (>40 chars), use line breaks: "Line1\\nLine2"
    21. SAFE ZONES: content must stay within x: -5 to 5, y: -2.5 to 2.5
    
    VIDEO TIMING (FOR AUDIO SYNC):
    22. Total video: 50-70 seconds
    23. Use self.wait(2) to self.wait(4) between sections
    24. Animation run_time: 1.0 to 2.0 seconds (not faster!)
    
    MANDATORY ENDING:
    25. MUST end with this exact code:
    ```python
    self.play(*[FadeOut(mob) for mob in self.mobjects])
    self.wait(0.5)
    ending_bg = Rectangle(width=14, height=8, fill_color=DARK_BLUE, fill_opacity=0.5)
    ending_text = Text("Apilage AI Video", font_size=48, color=GOLD)
    ending_text.move_to(ORIGIN)
    self.play(FadeIn(ending_bg), run_time=0.5)
    self.play(SpinInFromNothing(ending_text), run_time=1.5)
    self.wait(2.5)
    self.play(FadeOut(ending_text), FadeOut(ending_bg))
    self.wait(0.5)
    ```
    
    Common fixes:
    - If Text indexing fails, recreate the text or use separate Text objects
    - If color not found, use: RED, BLUE, GREEN, YELLOW, WHITE, ORANGE, PURPLE, GOLD, TEAL, PINK
    - If font issues, remove font parameter or use default
    - Always use self.play() for animations with run_time >= 0.8
    - Use self.wait() between animations (minimum 1 second)
    - ALWAYS FadeOut ALL elements before creating new ones
    
    Return ONLY the fixed Python code:
    """
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(fix_prompt)
    fixed_code = response.text.strip()
    
    # Clean up the response
    fixed_code = sanitize_manim_code(fixed_code)
    
    return fixed_code


def generate_manim_code(text_input, level="basic"):
    """
    Use Gemini to generate Manim Python code and a voice script based on the user's topic and level.
    Works for any educational topic: math, grammar, science, history, etc.
    Returns a tuple: (manim_code, voice_script, subtitles)
    """
    level_descriptions = {
        "basic": "fundamental concepts, simple explanations, basic terminology, suitable for beginners with colorful visuals",
        "intermediate": "detailed explanations with diagrams, relationships between concepts, intermediate complexity with visual aids",
        "special_topic": "advanced concepts, complex relationships, in-depth analysis with sophisticated visualizations"
    }
    
    # Create a unique identifier for this request
    import time
    request_id = int(time.time() * 1000)

    prompt = f"""
    REQUEST ID: {request_id}
    
    YOUR TASK: Create an engaging, colorful educational explainer video for THIS SPECIFIC TOPIC:
    
    ===== TOPIC =====
    {text_input}
    =================
    
    Level: {level} ({level_descriptions[level]})
    
    YOU MUST create content about "{text_input}" - not about any other topic.
    
    This can be ANY educational topic - math, grammar, language, science, history, programming, etc.

    Generate THREE things:

    1. A Manim Python script that creates a visually STUNNING educational video:
    
    STRICT REQUIREMENTS:
    - MUST start with: from manim import *
    - Define a class named exactly 'MathExplanationScene' that inherits from Scene
    - Implement the construct method with beautiful, engaging animations
    
    ====== VISUAL DESIGN RULES (MAKE IT BEAUTIFUL!) ======
    COLOR PALETTE - Use these consistently:
    - TITLES: Use gradients or GOLD, BLUE_B, TEAL_A
    - MAIN TEXT: WHITE or BLUE_A for readability
    - HIGHLIGHTS: YELLOW, ORANGE, PINK for emphasis
    - EXAMPLES: GREEN_B, GREEN_C for positive examples
    - ERRORS/WRONG: RED_B, RED_C for negative examples
    - BACKGROUNDS: Create colored rectangles behind text for emphasis
    - Use at least 4-5 different colors throughout the video
    
    SHAPES AND VISUAL AIDS:
    - Add colored BOXES (RoundedRectangle) around important concepts
    - Use ARROWS to show relationships and flow
    - Add UNDERLINES (Line or Underline) for key terms
    - Use CIRCLES or ELLIPSES to highlight items
    - Create ICONS with simple shapes (Circle, Square, Star, Triangle)
    - Add BULLET POINTS with colored dots
    - Use BRACKETS (Brace) for grouping concepts
    - Create TIMELINES or FLOWCHARTS for processes
    
    ANIMATION VARIETY:
    - FadeIn with scale, shift, or direction
    - Write for text appearing character by character
    - GrowFromCenter for shapes
    - DrawBorderThenFill for filled shapes
    - Create for geometric constructions
    - Indicate to highlight (pulsing effect)
    - Circumscribe to draw attention
    - Flash for emphasis
    - SpinInFromNothing for dramatic reveals
    - Transform for smooth transitions between content
    
    BACKGROUND ENHANCEMENTS:
    - Add subtle color backgrounds: Rectangle(width=14, height=8, fill_color=DARK_BLUE, fill_opacity=0.3)
    - Create section dividers with horizontal lines
    - Use gradient backgrounds for titles
    
    ====== CRITICAL: ZERO OVERLAP RULES (STRICTLY ENFORCED) ======
    RULE 1 - ONE THING AT A TIME:
    - NEVER show more than ONE main element on screen
    - Show title → fade out → show content → fade out → show next
    - Each section must be COMPLETELY cleared before next section
    
    RULE 2 - MANDATORY FADE OUT:
    - Before EVERY new element, run: self.play(*[FadeOut(mob) for mob in self.mobjects])
    - Wait 0.3 seconds after fading: self.wait(0.3)
    - This is NOT optional - do it between EVERY section
    
    RULE 3 - VERTICAL STACKING ONLY:
    - If showing 2+ items together, use VGroup with arrange(DOWN, buff=0.8)
    - MINIMUM buff=0.8 between stacked elements
    - Maximum 3 items in a VGroup
    
    RULE 4 - SCREEN ZONES (strictly enforce):
    - CENTER only: move_to(ORIGIN) for main content
    - Title zone: to_edge(UP, buff=0.8) - ONLY for titles, clear before content
    - NEVER use LEFT, RIGHT positioning together
    
    RULE 5 - TRANSFORM, DON'T ADD:
    - For step-by-step content, use Transform(old, new)
    - For derivations: show step1 → Transform to step2 → Transform to step3
    - NEVER add new elements while old ones exist
    
    CORRECT PATTERN (FOLLOW EXACTLY):
    ```python
    def construct(self):
        # SECTION 1: Title (clear screen first is automatic at start)
        title = Text("My Title", font_size=42, color=GOLD)
        title.move_to(ORIGIN)
        self.play(Write(title), run_time=1.5)
        self.wait(2)
        
        # CLEAR SCREEN - MANDATORY before section 2
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.3)
        
        # SECTION 2: Definition with colored background
        bg_rect = RoundedRectangle(width=10, height=2, fill_color=BLUE_E, fill_opacity=0.3, corner_radius=0.3)
        definition = Text("This is the definition", font_size=30, color=WHITE)
        definition.move_to(ORIGIN)
        bg_rect.move_to(definition.get_center())
        self.play(FadeIn(bg_rect), Write(definition), run_time=1.5)
        self.wait(3)
        
        # CLEAR SCREEN - MANDATORY before section 3
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.3)
        
        # SECTION 3: Example with icon
        icon = Circle(radius=0.3, fill_color=GREEN, fill_opacity=1).shift(LEFT * 4)
        example = Text("Example: This is correct", font_size=28, color=GREEN_B)
        example.move_to(ORIGIN)
        self.play(GrowFromCenter(icon), Write(example), run_time=1.5)
        self.wait(3)
        
        # CLEAR SCREEN - MANDATORY before next section
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.3)
    ```
    
    ====== TEXT RULES (PREVENT OVERFLOW) ======
    FONT SIZES:
    - Titles: font_size=42 maximum
    - Section headers: font_size=36
    - Body text: font_size=28-32
    - Small notes: font_size=24
    - NEVER exceed these sizes
    
    TEXT LENGTH:
    - Maximum 40 characters per line
    - For longer text: use "Line1\\nLine2\\nLine3"
    - Maximum 3 lines per text element
    
    MATH FORMULAS:
    - Always use .scale(0.7) or .scale(0.8) on MathTex
    - Center formulas: .move_to(ORIGIN)
    
    ====== VIDEO TIMING & SYNC (CRITICAL FOR AUDIO SYNC) ======
    TOTAL DURATION: 50-70 seconds (match narration length)
    
    TIMING BREAKDOWN:
    - Title intro: 5 seconds (write + wait)
    - Each content section: 8-10 seconds
    - Each example: 6-8 seconds  
    - Summary: 10-12 seconds
    - Ending: 5 seconds
    
    WAIT TIMES:
    - After title: self.wait(2)
    - After definition/explanation: self.wait(3)
    - After each example: self.wait(4)
    - After bullet points: self.wait(2) each
    - Before ending: self.wait(2)
    
    ANIMATION DURATIONS:
    - Write animations: run_time=1.5 to run_time=2
    - FadeIn/FadeOut: run_time=0.8 to run_time=1
    - Transform: run_time=1 to run_time=1.5
    - DO NOT use fast animations (run_time < 0.5)
    
    SYNC PRINCIPLE:
    - Narration describes what's on screen
    - Each spoken sentence = one visual element shown
    - Wait times allow narration to complete before transition
    
    ====== MANDATORY ENDING SEQUENCE ======
    At the VERY END, you MUST add this exact ending:
    ```python
    # ===== FINAL ENDING =====
    self.play(*[FadeOut(mob) for mob in self.mobjects])
    self.wait(0.5)
    
    # Branded ending with style
    ending_bg = Rectangle(width=14, height=8, fill_color=DARK_BLUE, fill_opacity=0.5)
    ending_text = Text("Apilage AI Video", font_size=48, color=GOLD)
    ending_text.move_to(ORIGIN)
    self.play(FadeIn(ending_bg), run_time=0.5)
    self.play(SpinInFromNothing(ending_text), run_time=1.5)
    self.wait(2.5)
    self.play(FadeOut(ending_text), FadeOut(ending_bg))
    self.wait(0.5)
    ```
    
    ====== COMPLETE VIDEO STRUCTURE TEMPLATE ======
    ```python
    from manim import *
    
    class MathExplanationScene(Scene):
        def construct(self):
            # ===== INTRO (5 seconds) =====
            # Colorful title with background
            title_bg = RoundedRectangle(width=12, height=2, fill_color=BLUE_E, fill_opacity=0.4, corner_radius=0.3)
            title = Text("[TOPIC TITLE]", font_size=42, color=GOLD)
            title.move_to(ORIGIN)
            title_bg.move_to(title.get_center())
            
            self.play(FadeIn(title_bg), Write(title), run_time=2)
            self.wait(2)
            
            # CLEAR SCREEN
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.3)
            
            # ===== DEFINITION (10 seconds) =====
            def_header = Text("What is it?", font_size=36, color=TEAL_A)
            def_header.to_edge(UP, buff=0.8)
            self.play(Write(def_header), run_time=1)
            self.wait(0.5)
            
            # Show definition with box
            def_box = RoundedRectangle(width=11, height=2.5, fill_color=BLUE_E, fill_opacity=0.2, corner_radius=0.2)
            definition = Text("[Definition here - max 40 chars per line]\\n[Second line if needed]", font_size=28, color=WHITE)
            definition.move_to(ORIGIN)
            def_box.move_to(definition.get_center())
            
            self.play(FadeIn(def_box), Write(definition), run_time=2)
            self.wait(4)
            
            # CLEAR SCREEN
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.3)
            
            # ===== EXAMPLES (25-30 seconds) =====
            # Example 1 with green checkmark icon
            ex1_header = Text("Example 1", font_size=34, color=GREEN_B)
            ex1_header.to_edge(UP, buff=0.8)
            self.play(Write(ex1_header), run_time=0.8)
            
            checkmark = Text("✓", font_size=48, color=GREEN)
            checkmark.move_to(LEFT * 4 + UP * 0.5)
            example1 = Text("[Example sentence here]", font_size=28, color=WHITE)
            example1.move_to(DOWN * 0.3)
            
            self.play(Write(checkmark), Write(example1), run_time=1.5)
            self.wait(4)
            
            # CLEAR SCREEN
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.3)
            
            # Example 2 (similar pattern)
            ex2_header = Text("Example 2", font_size=34, color=ORANGE)
            ex2_header.to_edge(UP, buff=0.8)
            self.play(Write(ex2_header), run_time=0.8)
            
            example2 = Text("[Second example here]", font_size=28, color=WHITE)
            example2.move_to(ORIGIN)
            highlight_box = SurroundingRectangle(example2, color=YELLOW, buff=0.3)
            
            self.play(Write(example2), run_time=1.5)
            self.play(Create(highlight_box), run_time=0.8)
            self.wait(4)
            
            # CLEAR SCREEN
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.3)
            
            # Example 3 with arrow
            ex3_header = Text("Example 3", font_size=34, color=PINK)
            ex3_header.to_edge(UP, buff=0.8)
            self.play(Write(ex3_header), run_time=0.8)
            
            before = Text("[Before]", font_size=26, color=RED_B)
            before.move_to(LEFT * 3)
            arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=YELLOW)
            after = Text("[After]", font_size=26, color=GREEN_B)
            after.move_to(RIGHT * 3)
            
            self.play(Write(before), run_time=1)
            self.play(GrowArrow(arrow), run_time=0.8)
            self.play(Write(after), run_time=1)
            self.wait(4)
            
            # CLEAR SCREEN
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.3)
            
            # ===== KEY POINTS SUMMARY (12 seconds) =====
            summary_title = Text("Key Points", font_size=38, color=GOLD)
            summary_title.to_edge(UP, buff=0.7)
            self.play(Write(summary_title), run_time=1)
            
            # Bullet points with colored dots
            bullet1 = VGroup(
                Dot(color=BLUE, radius=0.12),
                Text("First key point here", font_size=26, color=WHITE)
            ).arrange(RIGHT, buff=0.3)
            
            bullet2 = VGroup(
                Dot(color=GREEN, radius=0.12),
                Text("Second key point here", font_size=26, color=WHITE)
            ).arrange(RIGHT, buff=0.3)
            
            bullet3 = VGroup(
                Dot(color=ORANGE, radius=0.12),
                Text("Third key point here", font_size=26, color=WHITE)
            ).arrange(RIGHT, buff=0.3)
            
            bullets = VGroup(bullet1, bullet2, bullet3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
            bullets.move_to(DOWN * 0.3)
            
            for bullet in bullets:
                self.play(FadeIn(bullet, shift=RIGHT * 0.5), run_time=0.8)
                self.wait(1.5)
            
            self.wait(2)
            
            # CLEAR SCREEN
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.3)
            
            # ===== BRANDED ENDING (5 seconds) =====
            ending_bg = Rectangle(width=14, height=8, fill_color=DARK_BLUE, fill_opacity=0.5)
            ending_text = Text("Apilage AI Video", font_size=48, color=GOLD)
            ending_text.move_to(ORIGIN)
            
            self.play(FadeIn(ending_bg), run_time=0.5)
            self.play(SpinInFromNothing(ending_text), run_time=1.5)
            self.wait(2.5)
            self.play(FadeOut(ending_text), FadeOut(ending_bg))
            self.wait(0.5)
    ```
    
    FOR MATH TOPICS - USE TRANSFORM FOR DERIVATIONS:
    ```python
    # Show formula step by step using Transform
    step1 = MathTex(r"x^2 + 5x + 6 = 0").scale(0.8)
    step1.move_to(ORIGIN)
    self.play(Write(step1), run_time=1.5)
    self.wait(3)
    
    # Transform to next step (not add new!)
    step2 = MathTex(r"(x + 2)(x + 3) = 0").scale(0.8)
    step2.move_to(ORIGIN)
    self.play(Transform(step1, step2), run_time=1.5)
    self.wait(3)
    
    # Transform to solution
    step3 = MathTex(r"x = -2 \\text{{ or }} x = -3").scale(0.8)
    step3.move_to(ORIGIN)
    self.play(Transform(step1, step3), run_time=1.5)
    self.wait(3)
    ```
    
    VISUAL ELEMENTS LIBRARY:
    - Checkmark: Text("✓", color=GREEN)
    - Cross: Text("✗", color=RED)  
    - Star: Star(n=5, fill_color=YELLOW, fill_opacity=1)
    - Arrow: Arrow(start, end, color=YELLOW)
    - Box: RoundedRectangle(width=w, height=h, fill_color=color, fill_opacity=0.3, corner_radius=0.2)
    - Underline: Underline(mobject, color=YELLOW)
    - Highlight: SurroundingRectangle(mobject, color=YELLOW, buff=0.2)
    - Brace: Brace(mobject, direction=DOWN, color=WHITE)

    2. A VOICE SCRIPT (SPOKEN NARRATION ONLY):
    - Write ONLY the words to be spoken aloud - NO timestamps
    - Write natural, conversational narration that matches the video EXACTLY
    - Each visual element should have corresponding narration
    - Duration: 50-70 seconds of speaking to match video length
    - Use clear transitions: "Now let's look at..." "Here's an example..." "To summarize..."
    - End with: "This video was created by Apilage AI."
    
    VOICE SCRIPT EXAMPLE:
    "Welcome to this lesson on [topic]. Let's explore what [topic] means and how it works. 
    [Topic] is defined as [definition]. This is important because [reason].
    Let's look at our first example. [Explain example 1 in detail].
    Here's another example. [Explain example 2].
    For our third example, notice how [explain transformation or comparison].
    Let's summarize the key points. First, [point 1]. Second, [point 2]. And third, [point 3].
    Now you understand [topic]. Practice with more examples to master this concept.
    This video was created by Apilage AI."

    3. SUBTITLES (WebVTT format):
    - Break narration into 3-4 second segments
    - Include proper WebVTT timing that matches video pacing
    - Start with "WEBVTT" header

    Format your response EXACTLY as:
    MANIM_CODE:
    ```python
    [Python code here]
    ```

    VOICE_SCRIPT:
    [Natural spoken narration here - NO timestamps]

    SUBTITLES:
    [WebVTT subtitle content here]
    
    IMPORTANT: Generate UNIQUE content for "{text_input}". Make it visually engaging with colors and shapes!
    """

    print(f"[DEBUG] Generating content for topic: '{text_input}' at {level} level")
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Generate with specific settings to avoid caching
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )
    content = response.text.strip()
    
    print(f"[DEBUG] Received response of length: {len(content)}")

    # Parse the response to extract code, voice script, and subtitles
    manim_code = ""
    voice_script = ""
    subtitles = ""

    if "MANIM_CODE:" in content:
        manim_part = content.split("MANIM_CODE:")[1]
        if "VOICE_SCRIPT:" in manim_part:
            manim_part = manim_part.split("VOICE_SCRIPT:")[0]
        manim_part = manim_part.strip()
        
        # Extract code from markdown blocks
        if "```python" in manim_part:
            manim_code = manim_part.split("```python")[1]
            if "```" in manim_code:
                manim_code = manim_code.split("```")[0]
        elif "```" in manim_part:
            manim_code = manim_part.split("```")[1]
            if "```" in manim_code:
                manim_code = manim_code.split("```")[0]
        else:
            manim_code = manim_part
        
        manim_code = manim_code.strip()

    if "VOICE_SCRIPT:" in content:
        voice_part = content.split("VOICE_SCRIPT:")[1]
        if "SUBTITLES:" in voice_part:
            voice_part = voice_part.split("SUBTITLES:")[0]
        voice_script = voice_part.strip()

    if "SUBTITLES:" in content:
        subtitles = content.split("SUBTITLES:")[1].strip()

    # Sanitize and validate the code
    manim_code = sanitize_manim_code(manim_code)
    
    return manim_code, voice_script, subtitles


def parse_audio_mime_type(mime_type):
    """Parses bits per sample and rate from an audio MIME type string."""
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def convert_to_wav(audio_data, mime_type):
    """Converts raw audio data to WAV format."""
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        chunk_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size
    )
    return header + audio_data


def generate_audio_with_gemini(text):
    """
    Generate audio using Gemini TTS API.
    Returns the path to the generated audio file (converted to MP3 for compatibility).
    """
    print("[AUDIO] Trying Gemini TTS...")
    
    model = "gemini-2.5-flash-preview-tts"
    contents = [
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text=text),
            ],
        ),
    ]
    
    generate_content_config = genai_types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=genai_types.SpeechConfig(
            voice_config=genai_types.VoiceConfig(
                prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
                    voice_name="Kore"  # Clear, professional voice
                )
            )
        ),
    )
    
    audio_data = b""
    mime_type = None
    
    for chunk in gemini_tts_client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        
        part = chunk.candidates[0].content.parts[0]
        if part.inline_data and part.inline_data.data:
            audio_data += part.inline_data.data
            if mime_type is None:
                mime_type = part.inline_data.mime_type
    
    if not audio_data:
        raise Exception("No audio data received from Gemini TTS")
    
    # Convert to WAV format first
    wav_data = convert_to_wav(audio_data, mime_type or "audio/L16;rate=24000")
    
    # Save WAV to temp file
    wav_path = tempfile.mktemp(suffix='.wav')
    with open(wav_path, 'wb') as f:
        f.write(wav_data)
    
    # Convert WAV to MP3 for better compatibility
    mp3_path = tempfile.mktemp(suffix='.mp3')
    try:
        cmd = [
            "ffmpeg", "-y", "-i", wav_path,
            "-acodec", "libmp3lame", "-b:a", "192k",
            mp3_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        os.unlink(wav_path)  # Clean up WAV file
        print(f"[AUDIO] Gemini TTS audio generated and converted to MP3: {mp3_path} ({os.path.getsize(mp3_path)} bytes)")
        return mp3_path
    except Exception as conv_error:
        print(f"[AUDIO] WAV to MP3 conversion failed: {conv_error}, using WAV")
        if os.path.exists(mp3_path):
            os.unlink(mp3_path)
        print(f"[AUDIO] Gemini TTS audio generated: {wav_path} ({os.path.getsize(wav_path)} bytes)")
        return wav_path


def generate_audio(text_input):
    """
    Generate audio from text using Gemini TTS with gTTS fallback.
    """
    # Clean the text input thoroughly
    clean_text = text_input
    
    # Remove all timestamp formats: [00:00], [0:00], (00:00), etc.
    clean_text = re.sub(r'\[\d{1,2}:\d{2}\]', '', clean_text)
    clean_text = re.sub(r'\(\d{1,2}:\d{2}\)', '', clean_text)
    clean_text = re.sub(r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}', '', clean_text)
    
    # Remove WebVTT timing lines
    clean_text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', '', clean_text)
    
    # Remove any remaining timestamp-like patterns
    clean_text = re.sub(r'^\s*\d+\s*$', '', clean_text, flags=re.MULTILINE)
    
    # Remove "WEBVTT" header if present
    clean_text = re.sub(r'^WEBVTT\s*', '', clean_text, flags=re.IGNORECASE)
    
    # Remove markdown formatting
    clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_text)  # **bold**
    clean_text = re.sub(r'\*([^*]+)\*', r'\1', clean_text)      # *italic*
    clean_text = re.sub(r'`([^`]+)`', r'\1', clean_text)        # `code`
    
    # Remove extra whitespace and newlines
    clean_text = re.sub(r'\n+', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.strip()
    
    if not clean_text:
        raise Exception("Voice script is empty after cleaning")
    
    print(f"[AUDIO] Generating audio for text ({len(clean_text)} chars)")
    
    # Try Gemini TTS first
    try:
        audio_path = generate_audio_with_gemini(clean_text)
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return audio_path
        else:
            raise Exception("Gemini audio file too small")
            
    except Exception as e:
        print(f"[AUDIO] Gemini TTS failed: {e}, falling back to gTTS")
        
        # Fallback to gTTS
        try:
            print("[AUDIO] Trying gTTS...")
            tts = gTTS(text=clean_text, lang='en', slow=False)
            audio_path = tempfile.mktemp(suffix='.mp3')
            tts.save(audio_path)
            
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
                print(f"[AUDIO] gTTS audio generated: {audio_path} ({os.path.getsize(audio_path)} bytes)")
                return audio_path
            else:
                raise Exception("gTTS audio file too small")
                
        except Exception as gtts_error:
            print(f"[AUDIO] gTTS also failed: {gtts_error}")
            raise Exception(f"Both Gemini TTS and gTTS failed: {e}, {gtts_error}")


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


def get_audio_duration(audio_path):
    """
    Get the duration of an audio file using ffprobe.
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        import json
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"Warning: Could not get audio duration: {e}")
        return 30.0  # Default fallback


def extend_video_to_audio(video_path, audio_duration):
    """
    Extend video duration to match audio by freezing the last frame.
    This ensures the full audio plays without cutting.
    """
    video_duration = get_video_duration(video_path)
    
    if audio_duration <= video_duration:
        print(f"[EXTEND] Video ({video_duration:.1f}s) is already >= audio ({audio_duration:.1f}s)")
        return video_path  # Video is already long enough
    
    duration_diff = audio_duration - video_duration
    print(f"[EXTEND] Need to extend video by {duration_diff:.1f}s (from {video_duration:.1f}s to {audio_duration:.1f}s)")
    
    extended_path = video_path.replace('.mp4', '_extended.mp4')
    
    # Use ffmpeg to extend video by freezing the last frame
    # tpad filter adds padding by cloning the last frame
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"tpad=stop_mode=clone:stop_duration={duration_diff + 0.5}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-an",  # No audio in this step
        extended_path
    ]
    
    try:
        result = subprocess.run(cmd, check=True, cwd=os.getcwd(), capture_output=True, text=True, timeout=120)
        
        if os.path.exists(extended_path) and os.path.getsize(extended_path) > 1000:
            # Verify the extended duration
            new_duration = get_video_duration(extended_path)
            print(f"[EXTEND] Extended video duration: {new_duration:.1f}s")
            
            # Replace original with extended
            os.unlink(video_path)
            os.rename(extended_path, video_path)
            print(f"[EXTEND] Successfully extended video from {video_duration:.1f}s to {new_duration:.1f}s")
            return video_path
        else:
            print(f"[EXTEND] WARNING: Extended file missing or too small")
            return video_path
            
    except subprocess.CalledProcessError as e:
        print(f"[EXTEND] Warning: Could not extend video with tpad: {e.stderr}")
        
        # Try alternative method: loop video or slow it down slightly
        try:
            # Alternative: use setpts to slow down video slightly
            slowdown_factor = audio_duration / video_duration
            if slowdown_factor < 1.5:  # Only slow down if not too extreme
                print(f"[EXTEND] Trying alternative: slowing video by factor {slowdown_factor:.2f}")
                alt_cmd = [
                    "ffmpeg", "-y", "-i", video_path,
                    "-filter:v", f"setpts={slowdown_factor}*PTS",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                    "-an",
                    extended_path
                ]
                subprocess.run(alt_cmd, check=True, cwd=os.getcwd(), capture_output=True, timeout=120)
                if os.path.exists(extended_path) and os.path.getsize(extended_path) > 1000:
                    os.unlink(video_path)
                    os.rename(extended_path, video_path)
                    print(f"[EXTEND] Extended video using slowdown method")
                    return video_path
        except Exception as alt_e:
            print(f"[EXTEND] Alternative extension also failed: {alt_e}")
        
        return video_path
    except Exception as e:
        print(f"[EXTEND] Warning: Could not extend video: {e}")
        return video_path


def copy_to_uploads(video_path):
    """
    Copy the final video to the uploads/ folder with a unique timestamped name.
    Returns the path to the copied file.
    """
    import shutil
    from datetime import datetime
    
    # Create uploads directory if it doesn't exist
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = os.path.basename(video_path)
    base_name = os.path.splitext(original_name)[0]
    new_filename = f"{base_name}_{timestamp}.mp4"
    upload_path = os.path.join(uploads_dir, new_filename)
    
    try:
        # Copy the video file to uploads
        shutil.copy2(video_path, upload_path)
        print(f"[UPLOAD] Video copied to: {upload_path}")
        
        # Verify the copy
        if os.path.exists(upload_path):
            original_size = os.path.getsize(video_path)
            copy_size = os.path.getsize(upload_path)
            print(f"[UPLOAD] Original: {original_size} bytes, Copy: {copy_size} bytes")
            
            if copy_size == original_size:
                print(f"[UPLOAD] ✓ Successfully uploaded to uploads/ folder")
            else:
                print(f"[UPLOAD] WARNING: File sizes don't match!")
        
        return video_path  # Return original path for serving
        
    except Exception as e:
        print(f"[UPLOAD] ERROR: Could not copy to uploads: {e}")
        return video_path


def render_video(code, scene_name="MathExplanationScene", text_input=None, subtitles=None, max_retries=3):
    """
    Save the generated code to a temporary file and render the video using Manim.
    If text_input is provided, generate audio and combine with video.
    Returns the path to the rendered video.
    Includes retry logic with AI-based code fixing.
    Also copies final video to uploads/ folder.
    """
    temp_file = None
    audio_path = None
    current_code = code
    last_error = None
    
    for attempt in range(max_retries):
        try:
            # Validate syntax first
            is_valid, syntax_error = validate_python_syntax(current_code)
            if not is_valid:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1}: Syntax error - {syntax_error}")
                    current_code = fix_manim_code_with_ai(current_code, syntax_error)
                    continue
                else:
                    raise Exception(f"Invalid Python syntax after {max_retries} attempts: {syntax_error}")
            
            # Create temp file with the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(current_code)
                temp_file = f.name

            # Run Manim to render the video
            output_dir = "media/videos/generated"
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(f"{output_dir}/480p15", exist_ok=True)

            cmd = [
                "manim", temp_file, scene_name, "-ql", "--media_dir", "media"
            ]

            result = subprocess.run(
                cmd, 
                check=True, 
                cwd=os.getcwd(), 
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for longer videos
            )

            # Find the rendered video
            import glob
            video_files = glob.glob("media/videos/*/480p15/*.mp4")
            
            if not video_files:
                raise Exception("No video file was generated")
            
            latest_video = max(video_files, key=os.path.getctime)
            final_path = f"{output_dir}/480p15/{os.path.basename(latest_video)}"
            
            # Move the video to the final location
            if os.path.exists(final_path):
                os.unlink(final_path)
            os.rename(latest_video, final_path)

            # If text_input is provided, generate audio and combine
            if text_input:
                print(f"[RENDER] Starting audio generation for video: {final_path}")
                try:
                    audio_path = generate_audio(text_input)
                    print(f"[RENDER] Audio generated: {audio_path}")
                    
                    # Combine audio with video (will extend video if needed)
                    final_path_with_audio = combine_audio_video(final_path, audio_path)
                    print(f"[RENDER] Final video with audio: {final_path_with_audio}")
                    
                    # Clean up audio file
                    if audio_path and os.path.exists(audio_path):
                        try:
                            os.unlink(audio_path)
                            print(f"[RENDER] Cleaned up audio file")
                        except:
                            pass
                    
                    # Copy to uploads folder
                    final_path_with_audio = copy_to_uploads(final_path_with_audio)
                    
                    return final_path_with_audio
                except Exception as audio_error:
                    print(f"[RENDER] WARNING: Audio generation/combination failed: {audio_error}")
                    import traceback
                    traceback.print_exc()
                    # Return video without audio (still copy to uploads)
                    final_path = copy_to_uploads(final_path)
                    return final_path
            else:
                print(f"[RENDER] No text_input provided, returning video without audio")
                # Still copy to uploads
                final_path = copy_to_uploads(final_path)
                return final_path
                
        except subprocess.TimeoutExpired:
            last_error = "Video rendering timed out (exceeded 2 minutes)"
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1}: {last_error}")
                # Try to simplify the code
                current_code = fix_manim_code_with_ai(
                    current_code, 
                    "The animation is too complex and timed out. Please simplify it."
                )
        except subprocess.CalledProcessError as e:
            error_output = e.stderr if e.stderr else str(e)
            last_error = f"Manim rendering error: {error_output}"
            
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1}: Manim error - trying to fix...")
                current_code = fix_manim_code_with_ai(current_code, error_output)
            else:
                raise Exception(f"Failed to render video after {max_retries} attempts. Last error: {last_error}")
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1}: Error - {last_error}")
                current_code = fix_manim_code_with_ai(current_code, last_error)
            else:
                raise Exception(f"Failed to render video after {max_retries} attempts: {last_error}")
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    raise Exception(f"Failed to render video after {max_retries} attempts: {last_error}")


def combine_audio_video(video_path, audio_path):
    """
    Combine audio and video using ffmpeg.
    Uses the LONGEST duration to ensure NOTHING is cut off.
    Video is extended OR audio is padded to match durations.
    """
    print(f"[COMBINE] Starting audio/video merge")
    print(f"[COMBINE] Video: {video_path}")
    print(f"[COMBINE] Audio: {audio_path}")
    
    # Verify files exist
    if not os.path.exists(video_path):
        print(f"[COMBINE] ERROR: Video file not found: {video_path}")
        return video_path
    if not os.path.exists(audio_path):
        print(f"[COMBINE] ERROR: Audio file not found: {audio_path}")
        return video_path
    
    print(f"[COMBINE] Video size: {os.path.getsize(video_path)} bytes")
    print(f"[COMBINE] Audio size: {os.path.getsize(audio_path)} bytes")
    
    output_path = video_path.replace('.mp4', '_with_audio.mp4')
    
    # Get durations
    audio_duration = get_audio_duration(audio_path)
    video_duration = get_video_duration(video_path)
    
    print(f"[COMBINE] Video duration: {video_duration:.1f}s, Audio duration: {audio_duration:.1f}s")
    
    # Determine the target duration - use the LONGER one to ensure nothing is cut
    target_duration = max(audio_duration, video_duration)
    print(f"[COMBINE] Target duration (longest): {target_duration:.1f}s")
    
    # If audio is longer, extend video by freezing last frame
    if audio_duration > video_duration + 0.5:
        print(f"[COMBINE] Extending video from {video_duration:.1f}s to {audio_duration:.1f}s...")
        video_path = extend_video_to_audio(video_path, audio_duration)
        video_duration = get_video_duration(video_path)
        print(f"[COMBINE] Extended video duration: {video_duration:.1f}s")
    
    # Combine audio and video - NO -shortest flag to ensure full length
    # Add small audio delay to sync better (video renders slightly ahead)
    # Method 1: Copy video stream, encode audio with sync adjustment
    cmd = [
        "ffmpeg", "-y", 
        "-i", video_path, 
        "-i", audio_path,
        "-c:v", "copy",  # Copy video stream without re-encoding
        "-c:a", "aac", "-b:a", "192k",  # Convert audio to AAC
        "-af", "adelay=300|300",  # Delay audio by 300ms to sync with video
        "-map", "0:v:0", "-map", "1:a:0",
        # NO -shortest flag - we want FULL duration
        output_path
    ]
    
    print(f"[COMBINE] Running ffmpeg command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, cwd=os.getcwd(), capture_output=True, text=True, timeout=120)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            # Verify the output duration and audio
            output_duration = get_video_duration(output_path)
            print(f"[COMBINE] Output video duration: {output_duration:.1f}s")
            
            # Verify the output has audio
            verify_cmd = ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", output_path]
            verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
            
            if "audio" in verify_result.stdout:
                print(f"[COMBINE] Audio stream verified in output")
            else:
                print(f"[COMBINE] WARNING: No audio stream detected in output!")
            
            # Check if duration is close to expected
            if abs(output_duration - target_duration) > 2:
                print(f"[COMBINE] WARNING: Output duration ({output_duration:.1f}s) differs from target ({target_duration:.1f}s)")
            
            # Replace original video with the one with audio
            os.unlink(video_path)
            os.rename(output_path, video_path)
            print(f"[COMBINE] SUCCESS! Combined video: {video_path} ({os.path.getsize(video_path)} bytes)")
            return video_path
        else:
            print(f"[COMBINE] ERROR: Output file missing or too small")
            if os.path.exists(output_path):
                print(f"[COMBINE] Output size: {os.path.getsize(output_path)} bytes")
            return video_path
            
    except subprocess.TimeoutExpired:
        print(f"[COMBINE] FFmpeg timed out!")
        return video_path
    except subprocess.CalledProcessError as e:
        print(f"[COMBINE] FFmpeg failed!")
        print(f"[COMBINE] stdout: {e.stdout}")
        print(f"[COMBINE] stderr: {e.stderr}")
        
        # Try alternative command with full re-encoding
        print(f"[COMBINE] Trying alternative ffmpeg command with re-encoding...")
        alt_cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v:0", "-map", "1:a:0",
            # Still no -shortest - we want full video and audio
            output_path
        ]
        try:
            subprocess.run(alt_cmd, check=True, cwd=os.getcwd(), capture_output=True, text=True, timeout=180)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                output_duration = get_video_duration(output_path)
                print(f"[COMBINE] Alternative output duration: {output_duration:.1f}s")
                os.unlink(video_path)
                os.rename(output_path, video_path)
                print(f"[COMBINE] SUCCESS with alternative command! {video_path}")
                return video_path
        except Exception as alt_error:
            print(f"[COMBINE] Alternative command also failed: {alt_error}")
        
        return video_path
