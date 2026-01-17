#!/usr/bin/env python3
"""Test script to verify syntax error fixes in Manim code generation."""

from utils import stabilize_text_objects_in_manim_code, validate_python_syntax

# Test case 1: Incomplete VGroup definition (the problematic case)
test_code_incomplete_vgroup = """from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        # Title
        title = Text("Future Tenses", font_size=36, color=TEAL)
        title.move_to(UP * 2.5)

        # Keywords
        keywords = VGroup(
            Text("Will", font_size=28),
            Text("Going to", font_size=28),
            Text("Future continuous", font_size=28)
        )
        keywords.arrange(DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(FadeIn(keywords))
        self.wait(2)
"""

# Test case 2: Complete simple Text definition
test_code_simple_text = """from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        title = Text("Future Tenses", font_size=36, color=TEAL)
        title.move_to(UP * 2.5)
        
        self.play(Write(title))
        self.wait(2)
"""

# Test case 3: Multi-line VGroup that's properly closed
test_code_multiline_vgroup = """from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        items = VGroup(
            Text("Item 1"),
            Text("Item 2"),
            Text("Item 3")
        )
        items.arrange(DOWN)
        self.play(FadeIn(items))
        self.wait(2)
"""

def test_syntax_validation():
    """Test the syntax validation and stabilization functions."""
    print("=" * 60)
    print("Testing Syntax Validation and Stabilization")
    print("=" * 60)
    
    # Test 1: Incomplete VGroup (should still be valid Python)
    print("\n[Test 1] Complete VGroup with elements:")
    stabilized = stabilize_text_objects_in_manim_code(test_code_incomplete_vgroup)
    is_valid, error = validate_python_syntax(stabilized)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error}")
        print("\nStabilized code (first 30 lines):")
        for i, line in enumerate(stabilized.splitlines()[:30], 1):
            print(f"{i:3d}: {line}")
    else:
        print("✓ Code is syntactically valid")
    
    # Test 2: Simple Text
    print("\n[Test 2] Simple Text definition:")
    stabilized = stabilize_text_objects_in_manim_code(test_code_simple_text)
    is_valid, error = validate_python_syntax(stabilized)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error}")
    else:
        print("✓ Code is syntactically valid")
    
    # Test 3: Multi-line VGroup
    print("\n[Test 3] Multi-line VGroup:")
    stabilized = stabilize_text_objects_in_manim_code(test_code_multiline_vgroup)
    is_valid, error = validate_python_syntax(stabilized)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error}")
        print("\nStabilized code (first 30 lines):")
        for i, line in enumerate(stabilized.splitlines()[:30], 1):
            print(f"{i:3d}: {line}")
    else:
        print("✓ Code is syntactically valid")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_syntax_validation()
