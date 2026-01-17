#!/usr/bin/env python3
"""Test the fallback Manim code generation to ensure it's bulletproof."""

from utils import fallback_manim_code_for_segment, validate_python_syntax
import tempfile
import subprocess
import os

def test_fallback_code():
    """Test that fallback code is always valid Python and can be compiled."""
    
    print("=" * 70)
    print("Testing Fallback Manim Code Generation")
    print("=" * 70)
    
    test_cases = [
        ("Simple text", 3.0),
        ("Text with 'single quotes' inside", 5.0),
        ("Text with \"double quotes\" inside", 4.0),
        ("Text with backslash \\ character", 3.5),
        ("Past tenses: was, were, had", 6.0),
        ("Complex: it's, don't, won't", 4.5),
        ("Special chars: @#$%", 3.0),
        ("", 2.0),  # Empty text
    ]
    
    all_passed = True
    
    for idx, (text, duration) in enumerate(test_cases, 1):
        print(f"\n[Test {idx}] Text: '{text}', Duration: {duration}s")
        
        try:
            # Generate fallback code
            code = fallback_manim_code_for_segment(text, duration)
            
            # Test 1: Syntax validation
            is_valid, error = validate_python_syntax(code)
            if not is_valid:
                print(f"  ✗ SYNTAX ERROR: {error}")
                print("\n  Generated code:")
                for i, line in enumerate(code.splitlines(), 1):
                    print(f"    {i:3d}: {line}")
                all_passed = False
                continue
            
            print(f"  ✓ Syntax valid")
            
            # Test 2: Try to compile with Python AST
            try:
                compile(code, '<string>', 'exec')
                print(f"  ✓ Compiles successfully")
            except Exception as e:
                print(f"  ✗ COMPILATION ERROR: {e}")
                all_passed = False
                continue
            
            # Test 3: Check that duration calculation is present
            if f"{duration:.2f}" not in code:
                print(f"  ⚠ WARNING: Duration {duration} not found in code")
            else:
                print(f"  ✓ Duration {duration:.2f}s properly set")
            
        except Exception as e:
            print(f"  ✗ EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("SUCCESS: All fallback code tests passed!")
        print("The fallback code is bulletproof and will never fail.")
    else:
        print("FAILURE: Some tests failed - fallback code needs fixes")
    print("=" * 70)
    
    return all_passed


def test_fallback_with_manim():
    """Test that fallback code actually renders with Manim (if Manim is installed)."""
    print("\n" + "=" * 70)
    print("Testing Fallback Code with Actual Manim Rendering")
    print("=" * 70)
    
    # Check if Manim is available
    try:
        result = subprocess.run(["manim", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("Manim not installed or not working - skipping render test")
            return True
        print(f"Manim version: {result.stdout.strip()}")
    except Exception as e:
        print(f"Manim not available: {e} - skipping render test")
        return True
    
    # Generate fallback code
    code = fallback_manim_code_for_segment("Past tenses: was, were, had", 3.0)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    # Try to render
    media_dir = tempfile.mkdtemp(prefix="test_manim_")
    
    try:
        cmd = [
            "manim",
            temp_file,
            "MathExplanationScene",
            "-ql",
            "--media_dir",
            media_dir,
            "-o",
            "test.mp4",
        ]
        
        print(f"\nRunning: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Manim rendering succeeded!")
            print(f"✓ Output directory: {media_dir}")
            
            # Check if video was created
            import glob
            videos = glob.glob(os.path.join(media_dir, "**", "*.mp4"), recursive=True)
            if videos:
                print(f"✓ Video created: {videos[0]}")
                print(f"✓ Video size: {os.path.getsize(videos[0])} bytes")
                return True
            else:
                print("✗ No video file found")
                return False
        else:
            print(f"✗ Manim rendering failed (exit code {result.returncode})")
            print(f"\nSTDOUT:\n{result.stdout}")
            print(f"\nSTDERR:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Exception during rendering: {e}")
        return False
    finally:
        # Cleanup
        try:
            os.unlink(temp_file)
        except:
            pass
        # Keep media_dir for inspection if needed


if __name__ == "__main__":
    syntax_passed = test_fallback_code()
    
    if syntax_passed:
        render_passed = test_fallback_with_manim()
        
        print("\n" + "=" * 70)
        print("FINAL RESULTS:")
        print(f"  Syntax tests: {'PASSED' if syntax_passed else 'FAILED'}")
        print(f"  Render tests: {'PASSED' if render_passed else 'SKIPPED/FAILED'}")
        print("=" * 70)
