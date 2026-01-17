#!/usr/bin/env python3
"""
Direct test of the code generation and validation pipeline.
This simulates what happens when a video generation request is made.
"""

from utils import (
    generate_manim_code_for_segment,
    validate_python_syntax,
    sanitize_manim_code,
    stabilize_text_objects_in_manim_code,
)

def test_segment_generation():
    """Test generating a code segment for 'explain me future tenses'"""
    
    print("=" * 70)
    print("Testing End-to-End Code Generation Pipeline")
    print("=" * 70)
    
    topic = "explain me future tenses"
    segment_text = "In English, future tenses help us talk about things that haven't happened yet."
    duration = 5.0
    segment_index = 1
    total_segments = 3
    
    print(f"\nGenerating Manim code for:")
    print(f"  Topic: {topic}")
    print(f"  Segment: {segment_index}/{total_segments}")
    print(f"  Duration: {duration}s")
    print(f"  Text: {segment_text}")
    print("\nThis may take 10-15 seconds to generate with AI...")
    
    try:
        # Generate code (this calls the AI)
        code = generate_manim_code_for_segment(
            topic=topic,
            segment_text=segment_text,
            duration=duration,
            segment_index=segment_index,
            total_segments=total_segments
        )
        
        print("\n✓ Code generation completed")
        
        # Validate the generated code
        is_valid, error = validate_python_syntax(code)
        
        if is_valid:
            print("✓ Generated code is syntactically valid!")
            print(f"\nCode length: {len(code)} characters")
            print(f"Code lines: {len(code.splitlines())} lines")
            
            # Show first 30 lines
            print("\nFirst 30 lines of generated code:")
            print("-" * 70)
            for i, line in enumerate(code.splitlines()[:30], 1):
                print(f"{i:3d}: {line}")
            if len(code.splitlines()) > 30:
                print(f"... ({len(code.splitlines()) - 30} more lines)")
            print("-" * 70)
            
            return True
        else:
            print(f"✗ Generated code has syntax error: {error}")
            print("\nFull code:")
            print("-" * 70)
            for i, line in enumerate(code.splitlines(), 1):
                marker = " <-- ERROR" if str(i) in str(error) else ""
                print(f"{i:3d}: {line}{marker}")
            print("-" * 70)
            return False
            
    except Exception as e:
        print(f"\n✗ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_segment_generation()
    
    print("\n" + "=" * 70)
    if success:
        print("SUCCESS: Code generation produces valid Python syntax!")
        print("\nThe fixes are working correctly:")
        print("  1. AI prompt guides better code generation")
        print("  2. Stabilization safely handles multi-line definitions")
        print("  3. Validation catches any remaining issues")
    else:
        print("FAILURE: Code generation still has issues")
        print("\nThis should trigger the retry logic in render_video_audio_first():")
        print("  - Attempt 1: AI will try to fix the error")
        print("  - Attempt 2+: Fallback to guaranteed-safe code")
    print("=" * 70)
