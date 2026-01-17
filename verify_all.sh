#!/bin/bash
# Complete verification script - runs all checks

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          Video Generation System - Complete Verification          ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

cd '/Users/dinethgunawardana/Downloads/download-2026.1.16_21.46.26-gen-(server.apilageai.com)'

PASSED=0
FAILED=0

# Test 1: Fallback code validation
echo "[Test 1] Fallback Code Validation"
if python3 -c "from utils import fallback_manim_code_for_segment, validate_python_syntax; code = fallback_manim_code_for_segment('test', 3.0); valid, err = validate_python_syntax(code); exit(0 if valid else 1)" 2>/dev/null; then
    echo "  ✅ PASSED - Fallback code is syntactically valid"
    ((PASSED++))
else
    echo "  ❌ FAILED - Fallback code has syntax errors"
    ((FAILED++))
fi
echo ""

# Test 2: Color() removal
echo "[Test 2] Color() Constructor Removal"
if python3 -c "from utils import sanitize_manim_code; code = 'text = Text(\"hello\", color=Color(\"#FF0000\"))'; result = sanitize_manim_code(code); exit(0 if 'Color(' not in result else 1)" 2>/dev/null; then
    echo "  ✅ PASSED - Color() successfully removed"
    ((PASSED++))
else
    echo "  ❌ FAILED - Color() still present after sanitization"
    ((FAILED++))
fi
echo ""

# Test 3: String escaping
echo "[Test 3] String Escaping"
if python3 -c "from utils import fallback_manim_code_for_segment, validate_python_syntax; code = fallback_manim_code_for_segment(\"it's working with 'quotes'\", 3.0); valid, err = validate_python_syntax(code); exit(0 if valid else 1)" 2>/dev/null; then
    echo "  ✅ PASSED - Special characters properly escaped"
    ((PASSED++))
else
    echo "  ❌ FAILED - String escaping broken"
    ((FAILED++))
fi
echo ""

# Test 4: Full fallback test suite
echo "[Test 4] Comprehensive Fallback Tests"
if python3 test_fallback.py 2>&1 | grep -q "All fallback code tests passed"; then
    echo "  ✅ PASSED - All fallback edge cases handled"
    ((PASSED++))
else
    echo "  ❌ FAILED - Some fallback tests failed"
    ((FAILED++))
fi
echo ""

# Test 5: Full pipeline test
echo "[Test 5] Complete Pipeline Test"
if python3 test_comprehensive.py 2>&1 | grep -q "ALL TESTS PASSED"; then
    echo "  ✅ PASSED - Full pipeline working (with Manim rendering)"
    ((PASSED++))
else
    echo "  ❌ FAILED - Pipeline test failed"
    ((FAILED++))
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                        VERIFICATION RESULTS                        ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "  Tests Passed: $PASSED / $((PASSED + FAILED))"
echo "  Tests Failed: $FAILED / $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║  ✅ ALL VERIFICATIONS PASSED - System is ready for production!    ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Next steps:"
    echo "  1. Start Flask server: python3 app.py"
    echo "  2. Test with: curl -X POST http://localhost:5002/generate \\"
    echo "                -H 'Content-Type: application/json' \\"
    echo "                -d '{\"text\":\"Explain me past tenses\"}'"
    echo ""
    echo "Or visit http://localhost:5002 in your browser"
    exit 0
else
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║  ❌ SOME TESTS FAILED - Review output above                       ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    exit 1
fi
