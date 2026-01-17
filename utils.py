import os
import re
import ast
import json
import shutil
import struct
import tempfile
import time
import subprocess
import textwrap
from typing import List, Tuple, Optional

import google.generativeai as genai
from google import genai as genai_new
from google.genai import types as genai_types
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please create a .env file with your API key.")

# Configure Gemini clients
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_TTS_CLIENT = genai_new.Client(api_key=GEMINI_API_KEY)

# Paths
UPLOADS_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


def validate_python_syntax(code: str) -> Tuple[bool, str]:
    """Validate Python syntax and return (is_valid, error_message)."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as exc:
        return False, f"Syntax error at line {exc.lineno}: {exc.msg}"


def sanitize_manim_code(code: str) -> str:
    """Clean Gemini output into runnable Manim code without branded outros."""
    code = re.sub(r"^```python\s*", "", code, flags=re.MULTILINE)
    code = re.sub(r"^```\s*$", "", code, flags=re.MULTILINE)

    # Drop any non-code leading chatter (e.g., "1)" lists or explanations)
    leading_pattern = re.compile(r"^\s*(from\b|class\b|def\b|import\b|#|@|[A-Za-z_])")
    trailing_noise_patterns = (
        re.compile(r"^\s*```"),
        re.compile(r"^\s*\d+\)"),
        re.compile(r"^\s*- "),
        re.compile(r"^\s*Explanation", re.IGNORECASE),
    )
    lines = code.splitlines()
    while lines and not leading_pattern.match(lines[0]):
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and any(pat.match(lines[-1]) for pat in trailing_noise_patterns):
        lines.pop()
    code = "\n".join(lines)

    if "from manim import" not in code:
        code = "from manim import *\n\n" + code

    if "class MathExplanationScene" not in code:
        code = re.sub(r"class\s+\w+\s*\(\s*Scene\s*\)", "class MathExplanationScene(Scene)", code, count=1)

    code = re.sub(r"ImageMobject\s*\([^)]*\)", "Circle()", code)
    code = re.sub(r"SVGMobject\s*\([^)]*\)", "Circle()", code)
    
    # Remove Color() constructor calls - just use hex strings directly
    # Pattern: Color("#RRGGBB") -> "#RRGGBB"
    code = re.sub(r'Color\s*\(\s*(["\'][#A-Za-z0-9]+["\'])\s*\)', r'\1', code)

    return code.strip()


def wrap_text_for_manim(text: str, max_chars: int = 46) -> str:
    """Wrap plain text into lines so it stays readable and within frame."""
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if not cleaned:
        return ""
    # Heuristic wrap: prefer fewer, longer lines to reduce vertical overflow.
    # IMPORTANT: return literal '\n' so generated Python stays syntactically valid.
    return "\\n".join(textwrap.wrap(cleaned, width=max_chars, break_long_words=False, break_on_hyphens=False))


def extract_focus_terms(text: str, max_terms: int = 4) -> List[str]:
    """Derive concise keywords to display on screen when narration covers details."""
    words = [re.sub(r"[^A-Za-z0-9-]", "", w) for w in (text or "").split()]
    words = [w for w in words if w]
    if not words:
        return ["Key Idea"]

    primary = []
    seen = set()
    for word in words:
        candidate = word.capitalize()
        if len(candidate) <= 3:
            continue
        if candidate in seen:
            continue
        primary.append(candidate)
        seen.add(candidate)
        if len(primary) >= max_terms:
            break

    if not primary:
        primary = [words[0].capitalize()]

    return primary


def stabilize_text_objects_in_manim_code(code: str) -> str:
    """Best-effort: ensure Text/MathTex/Tex/Paragraph objects scale to fit the frame.

    This is intentionally conservative: it only touches simple assignments like
    `t = Text(...)` and inserts scale_to_fit calls if they are not already present.
    """
    lines = (code or "").splitlines()
    out: List[str] = []
    assign_re = re.compile(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(Text|MathTex|Tex|Paragraph|VGroup|Group)\(")

    for i, line in enumerate(lines):
        out.append(line)
        m = assign_re.match(line)
        if not m:
            continue

        indent, var_name, _kind = m.group(1), m.group(2), m.group(3)

        # Check if the assignment is complete (has closing parenthesis on same line or is multi-line)
        # For multi-line assignments, we need to find where the statement ends
        is_complete = False
        if ')' in line:
            # Try to count parentheses to see if balanced on this line
            open_count = line.count('(')
            close_count = line.count(')')
            if close_count >= open_count:
                is_complete = True
        
        # If not complete on the same line, look ahead to find where it ends
        if not is_complete:
            # Multi-line statement - find the closing parenthesis
            open_count = line.count('(') - line.count(')')
            j = i + 1
            while j < len(lines) and open_count > 0:
                open_count += lines[j].count('(') - lines[j].count(')')
                j += 1
            # If we found the end, check if scaling already exists after that point
            if j < len(lines):
                window = "\n".join(lines[j : j + 5])
                if f"{var_name}.scale_to_fit_width" in window or f"{var_name}.scale_to_fit_height" in window:
                    continue
                # Skip ahead - we'll add scaling after the complete statement
                continue
            else:
                # Statement doesn't close properly, skip it
                continue

        # If the next few lines already scale this variable, don't add duplicates.
        window = "\n".join(lines[i + 1 : i + 5])
        if f"{var_name}.scale_to_fit_width" in window or f"{var_name}.scale_to_fit_height" in window:
            continue

        # Keep proper margin to avoid cropping and ensure readability.
        # Use intermediate variables to avoid breaking expressions
        # Use larger margins (2.0 instead of 1.5) to prevent overlapping
        out.append(f"{indent}max_width = config.frame_width - 2.0")
        out.append(f"{indent}max_height = config.frame_height - 2.0")
        out.append(f"{indent}if {var_name}.width > max_width:")
        out.append(f"{indent}    {var_name}.scale_to_fit_width(max_width)")
        out.append(f"{indent}if {var_name}.height > max_height:")
        out.append(f"{indent}    {var_name}.scale_to_fit_height(max_height)")

    stabilized = "\n".join(out)

    font_size_re = re.compile(r"(font_size\s*=\s*)(\d+(?:\.\d+)?)")

    def clamp_font_size(match: re.Match) -> str:
        raw_value = match.group(2)
        try:
            value = float(raw_value)
        except ValueError:
            return match.group(0)
        if value <= 28:
            return match.group(0)
        clamped = 28
        if raw_value.isdigit() or raw_value.endswith(".0"):
            return f"{match.group(1)}{clamped}"
        return f"{match.group(1)}{float(clamped):.1f}"

    return font_size_re.sub(clamp_font_size, stabilized)


def fix_manim_code_with_ai(code: str, error_message: str) -> str:
    """Ask Gemini to patch Manim code based on an error message."""
    prompt = f"""
    Fix the Manim code below based on the error. Return only corrected Python.

    Error: {error_message}

    Common issues to check:
    - Incomplete VGroup/Text/MathTex definitions (missing closing parenthesis)
    - Unbalanced parentheses
    - Missing commas in VGroup arguments
    - Incomplete statements

    ```python
    {code}
    ```

    Return ONLY the corrected code, ensuring:
    1. All parentheses are balanced
    2. All VGroup, Text, MathTex definitions are complete before any other code
    3. All statements are syntactically valid Python
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt, generation_config={"temperature": 0.3})
    fixed = response.text or code
    fixed = sanitize_manim_code(fixed)
    # Don't apply stabilize here as it might cause issues - the AI fix should handle it
    return fixed


def split_narration_into_segments(text: str) -> List[str]:
    """Split narration into sentence-sized chunks."""
    cleaned = re.sub(r"\s+", " ", text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    return [s.strip() for s in sentences if s.strip()]


def generate_voice_script_only(topic: str) -> str:
    """Generate a structured 3-part narration: intro → content → summary."""
    prompt = f"""
    Write a natural-sounding educational video narration with this 3-part structure:

    Topic: {topic}

    Structure:
    1) INTRODUCTION (10-15 seconds): Start by explaining what you're going to teach. Set expectations.
    2) CONTENT (40-50 seconds): Main explanation with examples, details, and concepts.
    3) KEY POINTS & SUMMARY (10-15 seconds): Recap the most important takeaways briefly.

    Requirements:
    - Spoken words only (no section labels or headings in the narration)
    - Natural flow between sections (don't say "now let's move to...", just transition smoothly)
    - Total duration: 60-80 seconds
    - No timestamps, no stage directions, no brand names

    Return just the complete narration as one flowing paragraph.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    try:
        resp = model.generate_content(prompt, generation_config={"temperature": 0.7})
        script = (resp.text or "").strip()
        script = re.sub(r"\s+", " ", script)
        if script:
            return script
    except Exception:
        pass

    # Local fallback with 3-part structure
    fallback = (
        f"In this video, we're going to explore {topic} and understand how it works. "
        f"Let's break it down step by step. {topic} is a fundamental concept that appears in many contexts. "
        f"The key idea is to understand the relationship between the components and how they interact. "
        f"We'll look at a practical example to make this concrete. "
        f"To summarize, remember these key points: understand the basic definition, recognize the pattern, "
        f"and apply it in context. That's the essence of {topic}."
    )
    return fallback


def segment_script_with_ai(voice_script: str) -> List[str]:
    """Split narration into short spoken segments (fallbacks to sentence split)."""
    def merge_to_max(parts: List[str], max_segments: int) -> List[str]:
        cleaned = [re.sub(r"\s+", " ", p).strip() for p in parts if p and str(p).strip()]
        if len(cleaned) <= max_segments:
            return cleaned

        # Merge adjacent segments to reduce count while preserving order.
        merged: List[str] = []
        bucket = ""
        target_size = max(1, int(len(cleaned) / max_segments + 0.999))
        for i, seg in enumerate(cleaned, start=1):
            bucket = (bucket + " " + seg).strip() if bucket else seg
            if i % target_size == 0 and len(merged) < max_segments - 1:
                merged.append(bucket)
                bucket = ""
        if bucket:
            merged.append(bucket)

        # Safety: if still too many, keep folding into last.
        while len(merged) > max_segments:
            merged[-2] = (merged[-2] + " " + merged[-1]).strip()
            merged.pop()
        return merged

    base = split_narration_into_segments(voice_script)
    if len(base) >= 4:
        return merge_to_max(base, max_segments=6)

    prompt = f"""
    Split the narration into 4 to 7 short spoken segments.

    Rules:
    - Keep wording the same (only split, do not rewrite)
    - Each segment should be one sentence or a short clause
    - Return JSON array of strings ONLY

    Narration:
    {voice_script}
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content(prompt, generation_config={"temperature": 0.1})
        raw = (resp.text or "").strip()
        raw = re.sub(r"^```json\s*|```$", "", raw, flags=re.MULTILINE).strip()
        segments = json.loads(raw)
        if isinstance(segments, list):
            cleaned = [re.sub(r"\s+", " ", str(s)).strip() for s in segments]
            cleaned = [s for s in cleaned if s]
            if len(cleaned) >= 3:
                return merge_to_max(cleaned, max_segments=6)
    except Exception:
        pass

    return merge_to_max(split_narration_into_segments(voice_script) or [voice_script], max_segments=6)


def fallback_manim_code_for_segment(segment_text: str, duration: float) -> str:
    """Always-valid Manim code for a segment (Text only), lasts exactly duration seconds."""
    dur = max(0.8, float(duration))
    focus_terms = extract_focus_terms(segment_text)
    palette = ["#4C6EF5", "#2FBF71", "#FFB454", "#FF6B6B"]
    bullet_lines = []
    for idx, term in enumerate(focus_terms):
        # Escape single quotes and backslashes to prevent syntax errors
        safe_term = term.replace("\\", "\\\\").replace("'", "\\'")
        color = palette[idx % len(palette)]
        bullet_lines.append(f"{{'text': '{safe_term}', 'color': '{color}'}}")
    bullet_literal = "[" + ", ".join(bullet_lines) + "]"
    # Build code without any post-processing that might break it
    code = f"""from manim import *

class MathExplanationScene(Scene):
    def construct(self):
        background = RoundedRectangle(
            corner_radius=0.4,
            width=config.frame_width - 1.2,
            height=config.frame_height - 1.2,
            fill_color="#0F172A",
            fill_opacity=0.88,
            stroke_color="#1E293B",
            stroke_width=4,
        )
        background.set_z_index(-1)

        title = Text("Key Ideas", font_size=26, color="#E0E7FF")
        title.move_to(UP * 2.5)
        max_width = config.frame_width - 2.0
        max_height = config.frame_height - 2.0
        if title.width > max_width:
            title.scale_to_fit_width(max_width)
        if title.height > max_height:
            title.scale_to_fit_height(max_height)

        bullets = VGroup()
        data = {bullet_literal}
        for item in data:
            bullet = Text(item['text'], font_size=22, color=item['color'])
            if bullet.width > max_width:
                bullet.scale_to_fit_width(max_width)
            if bullet.height > max_height:
                bullet.scale_to_fit_height(max_height)
            bullets.add(bullet)

        if len(bullets) > 0:
            bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
            bullets.next_to(title, DOWN, buff=0.8)

        timeline = Rectangle(width=config.frame_width - 1.0, height=0.12, color="#E0E7FF")
        timeline.move_to(DOWN * 3.2)
        progress = Rectangle(
            width=0.2,
            height=0.12,
            fill_color="#38BDF8",
            fill_opacity=1.0,
            color="#38BDF8",
        )
        progress.set_z_index(2)
        progress.move_to(timeline.get_left())

        appear = min(0.7, {dur:.2f} * 0.2)
        self.play(FadeIn(background), FadeIn(title), run_time=appear)
        if len(bullets) > 0:
            self.play(LaggedStartMap(FadeIn, bullets, shift=UP*0.2), run_time=appear)
        self.play(FadeIn(timeline), run_time=0.3)
        self.play(GrowFromPoint(progress, timeline.get_left()), run_time=0.3)
        self.add(progress)
        hold_time = max(0.0, {dur:.2f} - (appear * 2 + 0.6))
        if hold_time > 0:
            self.wait(hold_time)
"""
    # Don't sanitize or stabilize - it's already correct
    return code.strip()


def generate_manim_code_for_segment(
    topic: str,
    segment_text: str,
    duration: float,
    segment_index: int,
    total_segments: int,
) -> str:
    """Generate Manim code for a single segment that lasts exactly duration seconds."""
    dur = max(0.8, float(duration))

    fallback_code = fallback_manim_code_for_segment(segment_text, dur)

    prompt = f"""
    Create Manim code for ONE segment of a larger video.

    Topic: {topic}
    Segment {segment_index}/{total_segments} narration:
    {segment_text}

    CRITICAL RULES - TEXT LAYOUT:
    - SMALL TEXT ONLY: Use font_size 20-24 for ALL text, 26-28 for titles MAXIMUM. Never exceed 28.
    - NO OVERLAPPING: Space text elements at least 0.8 units apart vertically using buff parameter.
    - LIMIT TEXT COUNT: Maximum 3 text items on screen. Fewer is better.
    - SINGLE FOCUS: Show ONE concept at a time. Fade out everything before showing next concept.
    - Use .arrange(DOWN, buff=0.8) for vertical spacing.
    - Position carefully: title at UP*2.5, content between UP*1 and DOWN*1, avoid edges.

    TECHNICAL RULES:
    - Presentation style: show diagrams, shapes, timelines, or 2-3 short keywords. Let audio explain details.
    - Use only built-in Manim objects (Text, MathTex, Axes, Circle, Square, Arrow, etc.). No images/SVG.
    - CRITICAL: All VGroup, Text, MathTex objects MUST be fully defined with closing parenthesis before any other code.
    - CRITICAL: Use hex color strings directly (e.g., color="#FF5733") NOT Color() constructor.
    - Scale ALL text objects: after creating any Text/MathTex/VGroup, immediately add:
      max_width = config.frame_width - 2.0
      max_height = config.frame_height - 2.0
      if obj.width > max_width: obj.scale_to_fit_width(max_width)
      if obj.height > max_height: obj.scale_to_fit_height(max_height)
    - Fade out previous content: self.play(*[FadeOut(m) for m in self.mobjects]) before new content.
    - Keep all content centered within x [-4,4], y [-2.5,2.5].
    - Total scene runtime MUST equal exactly {dur:.2f} seconds.
    - Use a simple pattern: quick appear animation (<=30% of duration), then hold using self.wait(remaining).
    - IMPORTANT: Ensure all Python syntax is valid - check that all parentheses are balanced and statements are complete.

    Return ONLY Python code.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    try:
        resp = model.generate_content(prompt, generation_config={"temperature": 0.7, "max_output_tokens": 2048})
        code = sanitize_manim_code(resp.text or "")
        code = stabilize_text_objects_in_manim_code(code)
        if code.strip():
            return code
    except Exception:
        pass

    return fallback_code


def build_webvtt(segments: List[str], durations: List[float]) -> str:
    subtitles = "WEBVTT\n\n"
    start_time = 0.0
    for seg, dur in zip(segments, durations):
        end_time = start_time + float(dur)
        start_ts = f"00:00:{start_time:05.2f}".replace(".", ",")
        end_ts = f"00:00:{end_time:05.2f}".replace(".", ",")
        subtitles += f"{start_ts} --> {end_ts}\n{seg}\n\n"
        start_time = end_time
    return subtitles.strip()


def generate_manim_code_with_timing(topic: str, voice_script: str, total_duration: float, segment_durations: List[float]) -> Tuple[str, str]:
    """Generate Manim code timed to the narration; returns (code, subtitles)."""
    timeline = []
    start = 0.0
    durations = segment_durations or [total_duration]
    for idx, dur in enumerate(durations):
        end = start + dur
        timeline.append(f"Segment {idx+1}: {start:.1f}s–{end:.1f}s (~{dur:.1f}s)")
        start = end
    timeline_text = "\n".join(timeline)

    prompt = f"""
    Create Manim code that follows the recorded narration exactly. Match timings.

    TOPIC: {topic}

    NARRATION (already recorded):
    {voice_script}

    SEGMENT TIMELINE:
    {timeline_text}

    Rules:
    - No canned templates or branded endings.
    - One focused visual per segment; brief entrance (<=30% of segment) then hold with self.wait() for remainder.
    - Each segment's total runtime must equal its timeline duration; use self.wait() to fill any remaining seconds.
    - Fade out everything before next segment: self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6).
    - Keep content centered within x [-5,5], y [-3,3]; break long lines with "\n"; font sizes 26-38.
    - Total runtime (animations + waits) must equal {total_duration:.1f} seconds.

    Respond with:
    MANIM_CODE:
    ```python
    [code]
    ```

    SUBTITLES:
    WEBVTT
    [captions]
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    resp = model.generate_content(prompt, generation_config={"temperature": 0.8, "top_p": 0.9, "max_output_tokens": 4096})
    content = resp.text or ""

    manim_code = ""
    subtitles = ""
    if "MANIM_CODE:" in content:
        part = content.split("MANIM_CODE:", 1)[1]
        if "SUBTITLES:" in part:
            part, sub_part = part.split("SUBTITLES:", 1)
            subtitles = sub_part.strip()
        code_block = part.split("```python")[-1]
        manim_code = code_block.split("```", 1)[0]
    manim_code = sanitize_manim_code(manim_code)

    if not subtitles:
        subtitles = "WEBVTT\n\n"
        start_time = 0.0
        script_segments = split_narration_into_segments(voice_script) or [voice_script]
        for seg, dur in zip(script_segments, durations):
            end_time = start_time + dur
            start_ts = f"00:00:{start_time:05.2f}".replace(".", ",")
            end_ts = f"00:00:{end_time:05.2f}".replace(".", ",")
            subtitles += f"{start_ts} --> {end_ts}\n{seg}\n\n"
            start_time = end_time

    return manim_code, subtitles.strip()


def parse_audio_mime_type(mime_type: str) -> dict:
    bits_per_sample = 16
    rate = 24000
    for part in mime_type.split(";"):
        p = part.strip().lower()
        if p.startswith("rate="):
            try:
                rate = int(p.split("=", 1)[1])
            except ValueError:
                pass
        elif p.startswith("audio/l"):
            try:
                bits_per_sample = int(p.split("l", 1)[1])
            except ValueError:
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    params = parse_audio_mime_type(mime_type or "audio/L16;rate=24000")
    bits_per_sample = params["bits_per_sample"]
    sample_rate = params["rate"]
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
        data_size,
    )
    return header + audio_data


def generate_audio_with_gemini(text: str) -> str:
    model = "gemini-2.5-flash-preview-tts"
    contents = [genai_types.Content(role="user", parts=[genai_types.Part.from_text(text=text)])]
    config = genai_types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=genai_types.SpeechConfig(
            voice_config=genai_types.VoiceConfig(
                prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(voice_name="Kore")
            )
        ),
    )

    attempt = 0
    last_exc = None
    while attempt < 3:
        attempt += 1
        audio_data = b""
        mime_type = None
        try:
            for chunk in GEMINI_TTS_CLIENT.models.generate_content_stream(model=model, contents=contents, config=config):
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                part = chunk.candidates[0].content.parts[0]
                if getattr(part, "inline_data", None) and part.inline_data.data:
                    audio_data += part.inline_data.data
                    mime_type = mime_type or part.inline_data.mime_type

            if not audio_data:
                raise RuntimeError("No audio data received from Gemini TTS")

            wav_data = convert_to_wav(audio_data, mime_type or "audio/L16;rate=24000")
            wav_path = tempfile.mktemp(suffix=".wav")
            with open(wav_path, "wb") as fh:
                fh.write(wav_data)
            return wav_path
        except Exception as exc:
            last_exc = exc
            if attempt >= 3:
                break
            time.sleep(1.5 * attempt)

    raise last_exc


def synthesize_segment(text: str) -> str:
    """Synthesize a single segment; prefer Gemini, fallback to gTTS. Returns wav path."""
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        raise ValueError("Voice script segment is empty after cleaning")

    try:
        path = generate_audio_with_gemini(cleaned)
        if os.path.exists(path) and os.path.getsize(path) > 400:
            return path
        raise RuntimeError("Gemini audio too small")
    except Exception as exc:
        print(f"[AUDIO] Gemini TTS failed: {exc}; falling back to gTTS")
        tts = gTTS(text=cleaned, lang="en", slow=False)
        mp3_path = tempfile.mktemp(suffix=".mp3")
        tts.save(mp3_path)
        wav_path = tempfile.mktemp(suffix=".wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", mp3_path,
            "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
            wav_path
        ], check=True, capture_output=True)
        try:
            os.unlink(mp3_path)
        except Exception:
            pass
        return wav_path


def concat_audio_segments(wav_paths: List[str]) -> str:
    """Concat pre-normalized wav segments into one m4a."""
    if not wav_paths:
        raise ValueError("No audio segments to concatenate")

    list_file = tempfile.mktemp(suffix="_concat.txt")
    with open(list_file, "w") as fh:
        for p in wav_paths:
            fh.write(f"file '{p}'\n")

    concat_wav = tempfile.mktemp(suffix="_concat.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", concat_wav
    ], check=True, capture_output=True)

    final_m4a = tempfile.mktemp(suffix=".m4a")
    subprocess.run([
        "ffmpeg", "-y", "-i", concat_wav,
        "-c:a", "aac", "-b:a", "192k",
        final_m4a
    ], check=True, capture_output=True)

    try:
        os.unlink(list_file)
        os.unlink(concat_wav)
    except Exception:
        pass

    return final_m4a


def generate_audio_with_segment_timings(segments: List[str]) -> Tuple[str, List[str], List[float], float]:
    """Generate audio per segment to obtain exact timings.

    Returns:
    - combined_audio_path (m4a)
    - segment_audio_paths (wav, one per segment)
    - segment_durations (seconds)
    - total_duration (seconds)
    """
    wav_paths: List[str] = []
    durations: List[float] = []
    try:
        for seg in segments:
            wav = synthesize_segment(seg)
            wav_paths.append(wav)
            durations.append(get_audio_duration(wav))

        audio_path = concat_audio_segments(wav_paths)
        total_duration = get_audio_duration(audio_path)

        # Adjust last duration to absorb encoding drift
        if durations:
            drift = total_duration - sum(durations)
            if abs(drift) > 0.05:
                durations[-1] = max(0.05, durations[-1] + drift)

        return audio_path, wav_paths, durations, total_duration
    except Exception:
        for wav in wav_paths:
            try:
                if os.path.exists(wav):
                    os.unlink(wav)
            except Exception:
                pass
        raise


def get_audio_duration(audio_path: str) -> float:
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def get_video_duration(video_path: str) -> float:
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def extend_video_to_duration(video_path: str, target_duration: float) -> str:
    """Pad video by cloning last frame so it is at least target_duration."""
    gap = max(target_duration - get_video_duration(video_path), 0)
    if gap <= 0.05:
        return video_path

    padded_path = tempfile.mktemp(suffix="_extended.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"tpad=stop_mode=clone:stop_duration={gap:.2f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-an", padded_path
    ], check=True, capture_output=True)
    return padded_path


def pad_audio_to_duration(audio_path: str, target_duration: float) -> str:
    """Pad audio with silence to reach target_duration."""
    gap = max(target_duration - get_audio_duration(audio_path), 0)
    if gap <= 0.05:
        return audio_path

    padded_path = tempfile.mktemp(suffix="_padded.m4a")
    subprocess.run([
        "ffmpeg", "-y", "-i", audio_path,
        "-af", f"apad=pad_dur={gap:.2f},atrim=0:{target_duration:.2f}",
        "-c:a", "aac", "-b:a", "192k",
        padded_path
    ], check=True, capture_output=True)
    return padded_path


def combine_audio_video(video_path: str, audio_path: str, target_duration: Optional[float] = None) -> str:
    temp_out = tempfile.mktemp(suffix="_av.mp4")
    audio_duration = get_audio_duration(audio_path)
    video_duration = get_video_duration(video_path)
    target = float(target_duration) if target_duration and target_duration > 0 else max(audio_duration, video_duration)

    padded_video = extend_video_to_duration(video_path, target)
    padded_audio = pad_audio_to_duration(audio_path, target)
    temp_to_cleanup = [p for p in (padded_video, padded_audio) if p not in (video_path, audio_path)]

    cmd = [
        "ffmpeg", "-y",
        "-i", padded_video,
        "-i", padded_audio,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-movflags", "+faststart",
        temp_out,
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    for path in temp_to_cleanup:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except Exception:
            pass

    return temp_out


def concat_video_segments(segment_mp4_paths: List[str]) -> str:
    """Concatenate segment mp4s into a single mp4 (re-encodes for safety)."""
    if not segment_mp4_paths:
        raise ValueError("No segment videos to concatenate")

    list_file = tempfile.mktemp(suffix="_video_concat.txt")
    with open(list_file, "w") as fh:
        for p in segment_mp4_paths:
            fh.write(f"file '{p}'\n")

    out_path = tempfile.mktemp(suffix="_final.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        out_path,
    ], check=True, capture_output=True)

    try:
        os.unlink(list_file)
    except Exception:
        pass

    return out_path


def copy_to_uploads(path: str) -> str:
    filename = os.path.basename(path)
    target = os.path.join(UPLOADS_DIR, filename)
    shutil.copy2(path, target)
    return target


def generate_content_audio_first(text_input: str) -> Tuple[str, List[str], List[str], List[float], str, str, float]:
    """Generate narration, segment it, synthesize audio per-segment, and return timings."""
    voice_script = generate_voice_script_only(text_input)
    segments = segment_script_with_ai(voice_script)

    combined_audio_path, segment_audio_paths, segment_durations, total_audio_duration = generate_audio_with_segment_timings(segments)
    if not segment_durations:
        segment_durations = [total_audio_duration or 10.0]
        segment_audio_paths = []

    subtitles = build_webvtt(segments, segment_durations)
    return (
        voice_script,
        segments,
        segment_audio_paths,
        segment_durations,
        combined_audio_path,
        subtitles,
        total_audio_duration,
    )


def render_video_audio_first(text_input: str, max_retries: int = 3):
    """Production-ready workflow:
    1) Generate narration
    2) Split into segments
    3) Generate audio per segment to get exact timings
    4) Generate and render Manim per segment
    5) Mux each segment with its audio
    6) Concatenate segment mp4s

    Returns (final_video_path, voice_script, subtitles)
    """

    (
        voice_script,
        segments,
        segment_audio_paths,
        segment_durations,
        combined_audio_path,
        subtitles,
        total_audio_duration,
    ) = generate_content_audio_first(text_input)

    segment_videos: List[str] = []
    media_dirs: List[str] = []

    try:
        total_segments = len(segments)
        for idx, (seg_text, seg_dur) in enumerate(zip(segments, segment_durations), start=1):
            seg_audio = segment_audio_paths[idx - 1] if idx - 1 < len(segment_audio_paths) else None
            if not seg_audio or not os.path.exists(seg_audio):
                raise RuntimeError("Missing per-segment audio; cannot render synced segments")

            current_code = generate_manim_code_for_segment(text_input, seg_text, seg_dur, idx, total_segments)
            last_error = None

            for attempt in range(max_retries):
                temp_file = None
                media_dir = None
                try:
                    is_valid, err = validate_python_syntax(current_code)
                    if not is_valid:
                        print(f"[DEBUG] Syntax error in segment {idx}: {err}")
                        print(f"[DEBUG] First 20 lines of code:")
                        for i, line in enumerate(current_code.splitlines()[:20], 1):
                            print(f"  {i:3d}: {line}")
                        raise SyntaxError(err)

                    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as fh:
                        fh.write(current_code)
                        temp_file = fh.name

                    media_dir = tempfile.mkdtemp(prefix=f"manim_media_seg_{idx:03d}_")
                    media_dirs.append(media_dir)

                    out_name = f"seg_{idx:03d}.mp4"
                    cmd = [
                        "manim",
                        temp_file,
                        "MathExplanationScene",
                        "-ql",
                        "--media_dir",
                        media_dir,
                        "-o",
                        out_name,
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                    if result.returncode != 0:
                        error_msg = f"Manim rendering failed (exit code {result.returncode})\n"
                        if result.stdout:
                            error_msg += f"STDOUT: {result.stdout[-500:]}\n"  # Last 500 chars
                        if result.stderr:
                            error_msg += f"STDERR: {result.stderr[-500:]}"  # Last 500 chars
                        raise RuntimeError(error_msg)

                    import glob

                    matches = glob.glob(
                        os.path.join(media_dir, "videos", "**", "480p15", out_name),
                        recursive=True,
                    )
                    if not matches:
                        matches = glob.glob(os.path.join(media_dir, "videos", "**", out_name), recursive=True)
                    if not matches:
                        raise RuntimeError("No segment video generated by Manim")

                    segment_video = matches[0]
                    # Copy out to a stable temp file so we can clean media_dir later.
                    stable_segment_video = tempfile.mktemp(suffix=f"_seg_{idx:03d}.mp4")
                    shutil.copy2(segment_video, stable_segment_video)

                    muxed = combine_audio_video(stable_segment_video, seg_audio, target_duration=float(seg_dur))
                    segment_videos.append(muxed)

                    try:
                        os.unlink(stable_segment_video)
                    except Exception:
                        pass

                    break
                except Exception as exc:
                    last_error = str(exc)
                    if attempt < max_retries - 1:
                        print(f"[RENDER] Segment {idx} attempt {attempt+1} failed: {exc}; retrying")
                        # First retry: try an AI fix if available; otherwise fall back to a safe segment scene.
                        if attempt == 0:
                            try:
                                print(f"[DEBUG] Attempting AI fix for segment {idx}")
                                current_code = fix_manim_code_with_ai(current_code, last_error)
                                # Validate the AI fix
                                is_valid_fix, fix_err = validate_python_syntax(current_code)
                                if not is_valid_fix:
                                    print(f"[DEBUG] AI fix produced invalid syntax: {fix_err}; using fallback")
                                    current_code = fallback_manim_code_for_segment(seg_text, seg_dur)
                            except Exception as fix_exc:
                                print(f"[DEBUG] AI fix failed: {fix_exc}; using fallback")
                                current_code = fallback_manim_code_for_segment(seg_text, seg_dur)
                        else:
                            print(f"[DEBUG] Using fallback code for segment {idx}")
                            current_code = fallback_manim_code_for_segment(seg_text, seg_dur)
                        continue
                    # Final attempt failed - log the code for debugging
                    print(f"[ERROR] All {max_retries} attempts failed for segment {idx}")
                    print(f"[ERROR] Last error: {last_error}")
                    print(f"[ERROR] Last code attempt (first 30 lines):")
                    for i, line in enumerate(current_code.splitlines()[:30], 1):
                        print(f"  {i:3d}: {line}")
                    raise
                finally:
                    if temp_file and os.path.exists(temp_file):
                        try:
                            os.unlink(temp_file)
                        except Exception:
                            pass

        final_video = concat_video_segments(segment_videos)
        final_video = copy_to_uploads(final_video)
        return final_video, voice_script, subtitles
    finally:
        for p in segment_audio_paths:
            try:
                if p and os.path.exists(p):
                    os.unlink(p)
            except Exception:
                pass

        try:
            if combined_audio_path and os.path.exists(combined_audio_path):
                os.unlink(combined_audio_path)
        except Exception:
            pass

        for p in segment_videos:
            try:
                if p and os.path.exists(p):
                    os.unlink(p)
            except Exception:
                pass

        for d in media_dirs:
            try:
                if d and os.path.exists(d):
                    shutil.rmtree(d, ignore_errors=True)
            except Exception:
                pass
