"""
common.py — Shared utilities for all EUDI knowledge skill generators.

Provides: fetching (markdown + HTML), HTML-to-markdown conversion,
token counting, section extraction, and skill file writing.
"""

import html
import re
import shutil
import tiktoken
import requests
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────

OUTPUT_BASE = Path(".opencode/skills")
ENCODER = tiktoken.get_encoding("cl100k_base")
TOKEN_WARN = 8_000

ARF_REPO_RAW = (
    "https://raw.githubusercontent.com/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/main/docs"
)
ARF_MEDIA_RAW = f"{ARF_REPO_RAW}/media"
ARF_RELEASES_API = (
    "https://api.github.com/repos/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/releases/latest"
)


# ── Token counting ─────────────────────────────────────────────────────────


def count_tokens(text: str) -> int:
    return len(ENCODER.encode(text))


# ── Fetching ───────────────────────────────────────────────────────────────


def get_arf_version() -> str:
    try:
        r = requests.get(ARF_RELEASES_API, timeout=10)
        if r.ok:
            return r.json().get("tag_name", "unknown")
    except Exception:
        pass
    return "unknown"


def fetch_markdown(url: str) -> str:
    """Fetch a markdown file and strip YAML frontmatter if present."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    text = r.text
    if text.startswith("---"):
        m = re.search(r"\n(?:---|\.\.\.) *\n", text)
        if m:
            text = text[m.end() :]
    return text.strip()


def fetch_html_as_markdown(url: str, source_url: str | None = None) -> str:
    """Fetch an HTML spec and convert it to markdown-like plain text.

    Args:
        url: The URL to fetch.
        source_url: Base URL for expanding internal #fragment links.
                    Defaults to url if not provided.
    """
    if source_url is None:
        source_url = url

    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"
    text = r.text

    # Strip non-content HTML elements (scripts, styles, nav, head, footer)
    text = re.sub(r"<head[^>]*>.*?</head>", "", text, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<nav[^>]*>.*?</nav>", "", text, flags=re.DOTALL)
    text = re.sub(r"<footer[^>]*>.*?</footer>", "", text, flags=re.DOTALL)
    text = re.sub(r"<header[^>]*>.*?</header>", "", text, flags=re.DOTALL)

    # Protect <pre> blocks from link conversion
    pre_blocks: list[str] = []

    def _stash_pre(m: re.Match) -> str:
        pre_blocks.append(m.group(0))
        return f"__PRE_BLOCK_{len(pre_blocks) - 1}__"

    text = re.sub(r"<pre[^>]*>.*?</pre>", _stash_pre, text, flags=re.DOTALL)

    # Remove pilcrow paragraph markers entirely (tag + content)
    text = re.sub(
        r'<a[^>]*class="[^"]*pilcrow[^"]*"[^>]*>.*?</a>', "", text, flags=re.DOTALL
    )

    # Remove selfRef navigation links — keep inner HTML for heading converter
    text = re.sub(
        r'<a[^>]*class="[^"]*selfRef[^"]*"[^>]*>(.*?)</a>',
        r"\1",
        text,
        flags=re.DOTALL,
    )

    # Convert <a href="...">text</a> to markdown [text](url)
    def _link_to_md(m: re.Match) -> str:
        href = m.group(1)
        inner = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not inner or not href:
            return inner or ""
        if href.startswith("#"):
            href = source_url + href
        return f"[{inner}]({href})"

    text = re.sub(
        r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        _link_to_md,
        text,
        flags=re.DOTALL,
    )

    # Convert headings to markdown — strip inner tags and normalize whitespace
    def _heading(level: int):
        prefix = "#" * level

        def replacer(m: re.Match) -> str:
            content = re.sub(r"<[^>]+>", "", m.group(1))
            content = " ".join(content.split())
            return f"{prefix} {content}"

        return replacer

    for lvl in range(1, 7):
        tag = f"h{lvl}"
        text = re.sub(
            rf"<{tag}[^>]*>(.*?)</{tag}>", _heading(lvl), text, flags=re.DOTALL
        )

    # Convert inline HTML tags to markdown equivalents
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text, flags=re.DOTALL)

    # Convert list items
    text = re.sub(r"<li[^>]*>", "- ", text)

    # Strip remaining tags
    text = re.sub(r"<[^>]+>", "", text)

    # Ensure headings start at the beginning of their line
    text = re.sub(r"^ +(#{1,6} )", r"\1", text, flags=re.MULTILINE)

    # Decode HTML entities
    text = html.unescape(text)

    # Remove any remaining pilcrow characters
    text = re.sub(r"\s*[¶]", "", text)

    # Restore <pre> blocks as code fences
    for i, block in enumerate(pre_blocks):
        inner = re.sub(r"<[^>]+>", "", block)
        inner = html.unescape(inner)
        text = text.replace(f"__PRE_BLOCK_{i}__", f"```\n{inner.strip()}\n```")

    # Collapse excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    return text.strip()


# ── Section extraction ─────────────────────────────────────────────────────


def extract_section(text: str, patterns: list) -> str:
    """Extract a section from markdown text matching any of the given heading patterns.

    Collects all lines from the first matching heading until a heading of equal
    or higher level is encountered.
    """
    lines = text.split("\n")
    result: list[str] = []
    collecting = False
    current_depth: int | None = None
    for line in lines:
        if any(re.match(p, line) for p in patterns):
            collecting, current_depth = True, len(line) - len(line.lstrip("#"))
            result.append(line)
            continue
        if collecting:
            m = re.match(r"^(#{1,6}) ", line)
            if m and current_depth is not None and len(m.group(1)) <= current_depth:
                break
            result.append(line)
    return "\n".join(result).strip()


def extract_all_sections_at_level(text: str, level: int) -> list[tuple[str, str]]:
    """Split markdown text into sections at a given heading level.

    Returns a list of (heading_text, section_content) tuples.
    Each section includes content from the heading until the next heading
    of the same or higher level.
    """
    pattern = re.compile(rf"^({'#' * level}) (.+)", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return []

    sections = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading = m.group(2).strip()
        content = text[start:end].strip()
        sections.append((heading, content))
    return sections


# ── Heading extraction ─────────────────────────────────────────────────────


def extract_headings(content: str, max_depth: int = 2) -> list[str]:
    """Extract headings from markdown content up to max_depth levels deep."""
    headings = []
    min_depth = None
    for line in content.split("\n"):
        m = re.match(r"^(#{1,6}) (.+)", line)
        if m:
            depth = len(m.group(1))
            if min_depth is None:
                min_depth = depth
            if depth <= (min_depth + max_depth - 1):
                headings.append(m.group(2).strip())
    return headings


# ── Skill writing ──────────────────────────────────────────────────────────


def write_skill(
    skill_dir: Path, name: str, description: str, content: str, version: str
) -> None:
    """Write a SKILL.md file with YAML frontmatter."""
    content = enrich_arf_diagrams(content)
    tokens = count_tokens(content)
    is_large = tokens > TOKEN_WARN
    skill_dir.mkdir(parents=True, exist_ok=True)
    headings = extract_headings(content)
    if headings:
        sections_lines = "\n".join(
            f'  - "{h.replace(chr(92), chr(92) + chr(92)).replace(chr(34), chr(92) + chr(34))}"'
            for h in headings
        )
        sections_block = f"\nsections:\n{sections_lines}"
    else:
        sections_block = ""
    skill_md = (
        f'---\nname: "{name}"\ndescription: "{description}"{sections_block}\n---\n\n'
        f"<!-- ARF version: {version} -->\n"
        f"<!-- Tokens: ~{tokens}{'(LARGE)' if is_large else ''} -->\n\n"
        f"{content}\n"
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    flag = "⚠" if is_large else "✓"
    print(
        f"  {flag}  {name}: ~{tokens} tokens"
        f"{'  ← consider splitting' if is_large else ''}"
    )


# ── Cleanup ────────────────────────────────────────────────────────────────


def clean_old_skills(output_base: Path | None = None) -> None:
    """Remove all existing skill directories under output_base."""
    base = output_base or OUTPUT_BASE
    if not base.exists():
        return
    for d in base.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            shutil.rmtree(d)


def clean_skills_with_prefix(prefix: str, output_base: Path | None = None) -> None:
    """Remove skill directories whose name starts with prefix."""
    base = output_base or OUTPUT_BASE
    if not base.exists():
        return
    for d in base.iterdir():
        if d.is_dir() and d.name.startswith(prefix) and (d / "SKILL.md").exists():
            shutil.rmtree(d)


def slugify(text: str) -> str:
    """Convert text to a URL/filename-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


_drawio_mermaid_cache: dict[str, str | None] = {}
_convert2mermaid_cmd: list[str] | None = None
_convert2mermaid_bootstrap_attempted = False
_convert2mermaid_tmpdir = None


def enrich_arf_diagrams(content: str) -> str:
    if "media/Figure_" not in content and f"{ARF_MEDIA_RAW}/Figure_" not in content:
        return content

    normalized = re.sub(r"\]\(media/", f"]({ARF_MEDIA_RAW}/", content)
    return _append_mermaid_for_figure_images(normalized)


def _append_mermaid_for_figure_images(content: str) -> str:
    image_re = re.compile(
        rf"!\[([^\]]*)\]\(({re.escape(ARF_MEDIA_RAW)}/Figure_[^)]+\.png)\)",
        re.IGNORECASE,
    )

    def repl(m):
        full = m.group(0)
        png_url = m.group(2)
        xml_url = re.sub(r"\.png$", ".xml", png_url, flags=re.IGNORECASE)
        mermaid = _drawio_xml_to_mermaid(xml_url)
        if not mermaid:
            return full
        return f"{full}\n\n```mermaid\n{mermaid}\n```"

    return image_re.sub(repl, content)


def _drawio_xml_to_mermaid(xml_url: str) -> str | None:
    cached = _drawio_mermaid_cache.get(xml_url)
    if cached is not None or xml_url in _drawio_mermaid_cache:
        return cached

    converter_cmd = _get_convert2mermaid_cmd()
    if converter_cmd is None:
        _drawio_mermaid_cache[xml_url] = None
        return None

    import subprocess
    import tempfile

    try:
        r = requests.get(xml_url, timeout=20)
        if not r.ok:
            _drawio_mermaid_cache[xml_url] = None
            return None

        with tempfile.TemporaryDirectory() as td:
            input_path = Path(td) / "diagram.drawio"
            output_path = Path(td) / "diagram.mmd"
            _ = input_path.write_text(r.text, encoding="utf-8")

            cmd = converter_cmd + [
                "-i",
                str(input_path),
                "-o",
                str(output_path),
                "-f",
                "mmd",
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if res.returncode != 0 or not output_path.exists():
                _drawio_mermaid_cache[xml_url] = None
                return None

            mermaid = output_path.read_text(encoding="utf-8").strip()
            if mermaid.startswith("```"):
                mermaid = re.sub(r"^```[a-zA-Z]*\s*", "", mermaid)
                mermaid = re.sub(r"\s*```$", "", mermaid).strip()

            _drawio_mermaid_cache[xml_url] = mermaid if mermaid else None
            return _drawio_mermaid_cache[xml_url]
    except Exception:
        _drawio_mermaid_cache[xml_url] = None
        return None


def _get_convert2mermaid_cmd() -> list[str] | None:
    global _convert2mermaid_cmd
    global _convert2mermaid_bootstrap_attempted
    global _convert2mermaid_tmpdir

    if _convert2mermaid_cmd is not None:
        return _convert2mermaid_cmd

    import shutil as _shutil

    installed = _shutil.which("convert2mermaid")
    if installed:
        _convert2mermaid_cmd = [installed]
        return _convert2mermaid_cmd

    if _convert2mermaid_bootstrap_attempted:
        return None
    _convert2mermaid_bootstrap_attempted = True

    if (
        not _shutil.which("git")
        or not _shutil.which("node")
        or not _shutil.which("npm")
    ):
        print("  ⚠  git/node/npm not found; skipping draw.io -> Mermaid conversion")
        return None

    import subprocess
    import tempfile

    try:
        _convert2mermaid_tmpdir = tempfile.TemporaryDirectory(prefix="convert2mermaid-")
        repo_dir = Path(_convert2mermaid_tmpdir.name) / "convert2mermaid"
        clone = subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/jgreywolf/convert2mermaid.git",
                str(repo_dir),
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if clone.returncode != 0:
            print("  ⚠  failed to clone convert2mermaid; skipping diagram conversion")
            return None

        install = subprocess.run(
            ["npm", "install"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if install.returncode != 0:
            print("  ⚠  failed to install convert2mermaid; skipping diagram conversion")
            return None

        build = subprocess.run(
            ["npm", "run", "build"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        cli = repo_dir / "dist" / "index.js"
        if build.returncode != 0 or not cli.exists():
            print("  ⚠  failed to build convert2mermaid; skipping diagram conversion")
            return None

        _convert2mermaid_cmd = ["node", str(cli)]
        return _convert2mermaid_cmd
    except Exception:
        print("  ⚠  error preparing convert2mermaid; skipping diagram conversion")
        return None
