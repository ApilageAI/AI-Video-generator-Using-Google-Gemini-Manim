#!/usr/bin/env python3
"""Test the exact problematic case from the error log."""

from utils import stabilize_text_objects_in_manim_code, validate_python_syntax

# This is the EXACT problematic code pattern from the error log
problematic_code = """from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        # Title
        title = Text("Future Tenses", font_size=36, color=TEAL)
        max_width = config.frame_width - 1.5
        max_height = config.frame_height - 1.5
        if title.width > max_width:
            title.scale_to_fit_width(max_width)
        if title.height > max_height:
            title.scale_to_fit_height(max_height)
        title.move_to(UP * 2.5)

        # Keywords
        keywords = VGroup(
"""

# Add more incomplete cases
incomplete_vgroup_no_close = """from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        items = VGroup(
            Text("Item 1"),
            Text("Item 2")
"""

print("=" * 70)
print("Testing Problematic Code Patterns")
print("=" * 70)

# Test 1: The exact error case (incomplete VGroup with no content)
print("\n[Test 1] Incomplete VGroup (no content, just opening):")
print("Original code has incomplete VGroup definition...")
is_valid_before, error_before = validate_python_syntax(problematic_code)
print(f"Before stabilization - Valid: {is_valid_before}")
if not is_valid_before:
    print(f"  Error: {error_before}")

stabilized = stabilize_text_objects_in_manim_code(problematic_code)
is_valid_after, error_after = validate_python_syntax(stabilized)
print(f"After stabilization - Valid: {is_valid_after}")
if not is_valid_after:
    print(f"  Error: {error_after}")
    print("\n  First 25 lines of stabilized code:")
    for i, line in enumerate(stabilized.splitlines()[:25], 1):
        marker = " <-- ERROR" if i == 18 else ""
        print(f"    {i:3d}: {line}{marker}")

# Test 2: Incomplete VGroup with elements but no closing
print("\n[Test 2] Incomplete VGroup (has elements, no closing paren):")
is_valid_before, error_before = validate_python_syntax(incomplete_vgroup_no_close)
print(f"Before stabilization - Valid: {is_valid_before}")
if not is_valid_before:
    print(f"  Error: {error_before}")

stabilized = stabilize_text_objects_in_manim_code(incomplete_vgroup_no_close)
is_valid_after, error_after = validate_python_syntax(stabilized)
print(f"After stabilization - Valid: {is_valid_after}")
if not is_valid_after:
    print(f"  Error: {error_after}")

# Test 3: What the AI should have generated (complete VGroup)
complete_code = """from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        # Title
        title = Text("Future Tenses", font_size=36, color=TEAL)
        title.move_to(UP * 2.5)

        # Keywords
        keywords = VGroup(
            Text("Will", font_size=28, color=BLUE),
            Text("Going to", font_size=28, color=GREEN),
            Text("Future Continuous", font_size=28, color=YELLOW)
        )
        keywords.arrange(DOWN, buff=0.3)
        keywords.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(FadeIn(keywords))
        self.wait(2)
"""

print("\n[Test 3] Complete proper VGroup (what AI should generate):")
is_valid_before, _ = validate_python_syntax(complete_code)
print(f"Before stabilization - Valid: {is_valid_before}")

stabilized = stabilize_text_objects_in_manim_code(complete_code)
is_valid_after, error_after = validate_python_syntax(stabilized)
print(f"After stabilization - Valid: {is_valid_after}")
if not is_valid_after:
    print(f"  Error: {error_after}")
else:
    print("  ✓ Code remains valid after stabilization")

print("\n" + "=" * 70)
print("Summary:")
print("=" * 70)
print("The stabilization function should:")
print("1. Skip incomplete VGroup definitions (can't be stabilized)")
print("2. Only add scaling code to complete, closed definitions")
print("3. Never break valid Python syntax")
print("=" * 70)
