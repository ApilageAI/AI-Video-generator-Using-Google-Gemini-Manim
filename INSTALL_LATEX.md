# Installing LaTeX for Manim on AlmaLinux

## Why LaTeX is Needed

Manim uses LaTeX to render mathematical equations and formulas. Without LaTeX, any scene with `MathTex` or `Tex` objects will fail.

---

## Installation Steps

### 1. Install LaTeX Distribution

```bash
# Update system packages
sudo dnf update -y

# Install required LaTeX packages
sudo dnf install -y texlive \
    texlive-latex \
    texlive-xetex \
    texlive-collection-latexextra \
    texlive-collection-fontsextra \
    dvisvgm
```

If the above packages are not found, try the minimal installation:

```bash
# Minimal LaTeX installation
sudo dnf install -y texlive-scheme-medium dvisvgm
```

### 2. Verify Installation

```bash
# Check LaTeX installation
latex --version
pdflatex --version
xelatex --version

# Check dvisvgm (required by Manim)
dvisvgm --version
```

### 3. Test with Manim

Create a simple test script:

```bash
cd /home/nova/public_html
cat > test_latex.py << 'EOF'
from manim import *

class TestLatex(Scene):
    def construct(self):
        # Test basic math
        eq = MathTex(r"E = mc^2")
        self.add(eq)
EOF

# Run test (activate venv first)
source venv/bin/activate
manim test_latex.py TestLatex -ql
```

If it works, you'll see output without errors.

### 4. Restart Video Generator Service

```bash
# Restart the service to pick up LaTeX
sudo systemctl restart video-generator

# Check logs
sudo journalctl -u video-generator -n 50 --no-pager
```

---

## Minimal Installation (Recommended)

If you want to save space and only install what's absolutely necessary:

```bash
# Install only core LaTeX packages needed for Manim
sudo dnf install -y \
    texlive-latex \
    texlive-amsmath \
    texlive-amsfonts \
    texlive-geometry \
    texlive-standalone \
    dvisvgm
```

---

## Troubleshooting

### Error: "latex: command not found"

LaTeX is not installed or not in PATH:
```bash
# Find latex binary
which latex

# If not found, reinstall
sudo dnf install -y texlive-latex
```

### Error: "dvisvgm: command not found"

```bash
# Install dvisvgm separately
sudo dnf install -y dvisvgm

# Verify
dvisvgm --version
```

### Error: LaTeX package missing (e.g., "amsmath.sty not found")

```bash
# Install additional LaTeX packages
sudo dnf install -y texlive-collection-latexrecommended
```

### Check what LaTeX packages are available

```bash
# List all texlive packages
dnf search texlive | grep -i latex

# Or search for specific package
dnf search texlive-amsmath
```

---

## Disk Space Consideration

- **Full Installation (~2-3 GB):** `texlive-scheme-full`
- **Medium Installation (~1 GB):** `texlive-scheme-medium` (Recommended)
- **Minimal (~300-500 MB):** Individual packages listed above

For production use, the medium installation is recommended as it includes most commonly used packages.

---

## Testing Math Rendering

After installation, test if math rendering works:

```bash
cd /home/nova/public_html
source venv/bin/activate

# Quick Python test
python3 << 'EOF'
from manim import MathTex
import tempfile
import os

try:
    # Create a temporary scene
    tex = MathTex(r"\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
    print("✅ LaTeX is working! Math rendering successful.")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

---

## Common LaTeX Packages Used by Manim

These are automatically used by Manim when rendering math:

- `amsmath` - Advanced math typesetting
- `amssymb` - Math symbols
- `geometry` - Page layout
- `xcolor` - Colors
- `standalone` - Standalone document class

---

## Quick Install (Copy & Paste)

```bash
# One-line installation for Manim math support
sudo dnf install -y texlive-scheme-medium dvisvgm && \
latex --version && \
dvisvgm --version && \
echo "✅ LaTeX installed successfully!"
```

Then restart your video generator:

```bash
sudo systemctl restart video-generator
sudo journalctl -u video-generator -f
```

Now try generating a video with math equations - it should work! 🎉

---

## Alternative: Check if LaTeX is Already Installed

Before installing, check if LaTeX might already be installed:

```bash
# Check if latex commands exist
which latex
which pdflatex
which dvisvgm

# Check installed texlive packages
dnf list installed | grep texlive
```

If commands are found but math still doesn't work, you might just need specific packages:

```bash
sudo dnf install -y texlive-collection-latexextra
```

---

**Last Updated:** January 27, 2026
