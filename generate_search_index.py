import os
import json
import re
from datetime import datetime

CONTENT_DIR = "content"
STATIC_DIR = "content/static"


def simple_slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", text)


if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

posts = []
for filename in os.listdir(CONTENT_DIR):
    if filename.endswith(".rst") and not filename.startswith("."):
        filepath = os.path.join(CONTENT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines()
        metadata = {}
        title = None
        body_start = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(":") and ":" in stripped:
                key, value = [p.strip() for p in stripped[1:].split(":", 1)]
                metadata[key] = value
                continue
            if (
                not title
                and stripped
                and not stripped.startswith("=")
                and not stripped.startswith("-")
            ):
                title = stripped
            elif (
                not title
                and i > 0
                and (stripped.startswith("=") or stripped.startswith("-"))
            ):
                title = lines[i - 1].strip()
            if title and body_start == 0:
                body_start = i
                break

        title = title or "Untitled"
        date_str = metadata.get("date")
        try:
            date = (
                datetime.fromisoformat(date_str.replace(" ", "T"))
                if date_str
                else datetime.now()
            )
        except:
            date = datetime.now()

        category = metadata.get("category", "Uncategorized")
        tags = (
            [t.strip() for t in metadata.get("tags", "").split(",")]
            if metadata.get("tags")
            else []
        )

        slug = simple_slugify(title)
        url = f"posts/{date.strftime('%Y/%m')}/{slug}/"

        content_text = " ".join(lines[body_start:])

        posts.append(
            {
                "title": title,
                "url": url,
                "date": date.strftime("%Y-%m-%d"),
                "category": category,
                "tags": tags,
                "content": content_text[:800] + "..."
                if len(content_text) > 800
                else content_text,
            }
        )

with open(os.path.join(STATIC_DIR, "search_index.json"), "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"Generated search index with {len(posts)} posts")
