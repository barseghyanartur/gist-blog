import os
import json
import re
from datetime import datetime

CONTENT_DIR = "content"
STATIC_DIR = "static"


def simple_slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s-]+', '-', text)


def parse_rst_file(filepath):
    """Parse an RST file, returning (title, metadata, body_text)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    metadata = {}
    title = None
    body_lines = []
    i = 0

    # --- Phase 1: extract title (first non-blank line + optional underline) ---
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped:
            # Could be the title or a metadata line
            if stripped.startswith(':') and ':' in stripped[1:]:
                # metadata before title — unusual but handle gracefully
                key, value = [p.strip() for p in stripped[1:].split(':', 1)]
                metadata[key] = value
                i += 1
                continue
            title = stripped
            i += 1
            # consume optional RST underline (===, ---, ~~~, etc.)
            if i < len(lines) and lines[i].strip() and all(
                c in '=-~^"\'`#+*' for c in lines[i].strip()
            ):
                i += 1
            break
        i += 1

    # --- Phase 2: consume metadata block (lines starting with :key:) ---
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith(':') and ':' in stripped[1:]:
            key, value = [p.strip() for p in stripped[1:].split(':', 1)]
            metadata[key] = value
            i += 1
        else:
            break

    # --- Phase 3: everything remaining is the body ---
    body_lines = lines[i:]

    return title, metadata, body_lines


def clean_rst_text(lines):
    """Strip RST markup from body lines and return plain text."""
    text_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip pure RST underline/overline rows
        if stripped and all(c in '=-~^"\'`#+*' for c in stripped):
            continue
        # Skip RST directives (.. image::, .. code-block::, etc.)
        if stripped.startswith('.. '):
            continue
        # Strip inline RST markup: ``code``, *em*, **strong**, `ref`_
        cleaned = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)   # **bold**
        cleaned = re.sub(r'\*(.+?)\*', r'\1', cleaned)         # *italic*
        cleaned = re.sub(r'``(.+?)``', r'\1', cleaned)         # ``code``
        cleaned = re.sub(r'`(.+?)`_?', r'\1', cleaned)         # `ref`_
        # Strip role syntax :role:`text`
        cleaned = re.sub(r':\w+:`(.+?)`', r'\1', cleaned)
        if cleaned:
            text_lines.append(cleaned)

    return ' '.join(text_lines)


if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

posts = []
for filename in sorted(os.listdir(CONTENT_DIR)):
    if not filename.endswith('.rst') or filename.startswith('.'):
        continue

    filepath = os.path.join(CONTENT_DIR, filename)
    title, metadata, body_lines = parse_rst_file(filepath)

    title = title or 'Untitled'
    date_str = metadata.get('date', '')
    try:
        date = datetime.fromisoformat(date_str.replace(' ', 'T')) if date_str else datetime.now()
    except Exception:
        date = datetime.now()

    category = metadata.get('category', 'Uncategorized')
    tags = [t.strip() for t in metadata.get('tags', '').split(',')] if metadata.get('tags') else []
    summary = metadata.get('summary', '').strip()

    slug = simple_slugify(title)
    url = f"posts/{date.strftime('%Y/%m')}/{slug}/"

    # Build a clean searchable body: prefer summary, fall back to cleaned body
    body_text = clean_rst_text(body_lines)
    searchable = summary if summary else body_text
    if len(searchable) > 1000:
        searchable = searchable[:1000] + '…'

    posts.append({
        'title': title,
        'url': url,
        'date': date.strftime('%Y-%m-%d'),
        'category': category,
        'tags': tags,
        'summary': summary,
        'content': searchable,
    })

with open(os.path.join(STATIC_DIR, 'search_index.json'), 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"Generated search index with {len(posts)} posts")
