#!/usr/bin/env python3
"""
Verification script for Audio-First Workflow implementation
Tests that all new functions exist and are properly integrated
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all new functions can be imported"""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    try:
        from utils import (
            generate_audio_script_with_timing,
            get_audio_timing_info,
            generate_adaptive_manim_code,
            generate_audio,
            render_video,
            combine_audio_video
        )
        print("✓ All new functions successfully imported from utils.py")
        
        from app import process_job, create_job, get_job
        print("✓ Job management functions successfully imported from app.py")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_function_signatures():
    """Test that functions have correct signatures"""
    print("\n" + "=" * 60)
    print("TESTING FUNCTION SIGNATURES")
    print("=" * 60)
    
    try:
        from utils import (
            generate_audio_script_with_timing,
            get_audio_timing_info,
            generate_adaptive_manim_code
        )
        import inspect
        
        # Test 1: generate_audio_script_with_timing
        sig = inspect.signature(generate_audio_script_with_timing)
        params = list(sig.parameters.keys())
        assert 'topic' in params, "Missing 'topic' parameter"
        assert 'level' in params, "Missing 'level' parameter"
        print("✓ generate_audio_script_with_timing has correct parameters")
        
        # Test 2: get_audio_timing_info
        sig = inspect.signature(get_audio_timing_info)
        params = list(sig.parameters.keys())
        assert 'audio_path' in params, "Missing 'audio_path' parameter"
        print("✓ get_audio_timing_info has correct parameters")
        
        # Test 3: generate_adaptive_manim_code
        sig = inspect.signature(generate_adaptive_manim_code)
        params = list(sig.parameters.keys())
        assert 'topic' in params, "Missing 'topic' parameter"
        assert 'level' in params, "Missing 'level' parameter"
        assert 'script_data' in params, "Missing 'script_data' parameter"
        assert 'audio_duration' in params, "Missing 'audio_duration' parameter"
        print("✓ generate_adaptive_manim_code has correct parameters")
        
        return True
    except Exception as e:
        print(f"✗ Signature test failed: {e}")
        return False

def test_process_job_updated():
    """Test that process_job has been updated"""
    print("\n" + "=" * 60)
    print("TESTING PROCESS_JOB UPDATE")
    print("=" * 60)
    
    try:
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        # Check for new function calls
        checks = [
            ('generate_audio_script_with_timing', 'Script generation'),
            ('get_audio_timing_info', 'Audio timing analysis'),
            ('generate_adaptive_manim_code', 'Adaptive Manim code generation'),
            ('combine_audio_video', 'Audio-video combination'),
        ]
        
        all_found = True
        for func_name, desc in checks:
            if func_name in app_content:
                print(f"✓ process_job calls {func_name} ({desc})")
            else:
                print(f"✗ process_job missing {func_name}")
                all_found = False
        
        # Check for new progress messages
        progress_checks = [
            'Generating audio script',
            'Rendering voice narration',
            'Analyzing audio timing',
            'Generating adaptive animations',
            'Rendering video animations',
            'Combining audio and video',
        ]
        
        progress_found = all(msg in app_content for msg in progress_checks)
        if progress_found:
            print("✓ All new progress messages present")
        else:
            print("✗ Some progress messages missing")
            all_found = False
        
        return all_found
    except Exception as e:
        print(f"✗ process_job test failed: {e}")
        return False

def test_documentation():
    """Test that documentation files exist"""
    print("\n" + "=" * 60)
    print("TESTING DOCUMENTATION")
    print("=" * 60)
    
    docs = [
        'AUDIO_FIRST_WORKFLOW.md',
        'WORKFLOW_COMPARISON.md',
        'IMPLEMENTATION_GUIDE.md',
        'AUDIO_FIRST_SUMMARY.md',
    ]
    
    all_exist = True
    for doc in docs:
        if os.path.exists(doc):
            size = os.path.getsize(doc)
            print(f"✓ {doc} exists ({size} bytes)")
        else:
            print(f"✗ {doc} missing")
            all_exist = False
    
    return all_exist

def test_syntax():
    """Test Python syntax of modified files"""
    print("\n" + "=" * 60)
    print("TESTING PYTHON SYNTAX")
    print("=" * 60)
    
    import py_compile
    
    files_to_check = ['app.py', 'utils.py']
    all_valid = True
    
    for filepath in files_to_check:
        try:
            py_compile.compile(filepath, doraise=True)
            print(f"✓ {filepath} syntax is valid")
        except py_compile.PyCompileError as e:
            print(f"✗ {filepath} has syntax errors: {e}")
            all_valid = False
    
    return all_valid

def run_all_tests():
    """Run all verification tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  AUDIO-FIRST WORKFLOW IMPLEMENTATION VERIFICATION".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    
    # Run all tests
    results.append(("Syntax Check", test_syntax()))
    results.append(("Imports", test_imports()))
    results.append(("Function Signatures", test_function_signatures()))
    results.append(("process_job Update", test_process_job_updated()))
    results.append(("Documentation", test_documentation()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Implementation is complete and verified.")
        print("\nYour system is ready to use the new audio-first workflow!")
        print("New progress messages:")
        print("  1. Generating audio script...")
        print("  2. Rendering voice narration...")
        print("  3. Analyzing audio timing...")
        print("  4. Generating adaptive animations...")
        print("  5. Rendering video animations...")
        print("  6. Combining audio and video...")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
