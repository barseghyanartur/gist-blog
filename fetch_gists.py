import requests
import os
import shutil

USERNAME = "barseghyanartur"  # ← CHANGE TO YOUR GITHUB USERNAME
GIST_API = f"https://api.github.com/users/{USERNAME}/gists"
CONTENT_DIR = "content"
PAGES_DIR = os.path.join(CONTENT_DIR, "pages")
STATIC_DIR = os.path.join(CONTENT_DIR, "static")
TEMP_PAGES = "temp_pages"
TEMP_STATIC = "temp_static"


def fetch_blog_gists():
    # Preserve any static pages (e.g. search page) and static folder
    pages_backup = None
    static_backup = None
    if os.path.exists(PAGES_DIR):
        pages_backup = TEMP_PAGES
        shutil.copytree(PAGES_DIR, pages_backup)
    if os.path.exists(STATIC_DIR):
        static_backup = TEMP_STATIC
        shutil.copytree(STATIC_DIR, static_backup)

    if os.path.exists(CONTENT_DIR):
        shutil.rmtree(CONTENT_DIR)
    os.makedirs(CONTENT_DIR)

    # Restore pages and static
    if pages_backup and os.path.exists(pages_backup):
        os.makedirs(PAGES_DIR, exist_ok=True)
        shutil.copytree(pages_backup, PAGES_DIR, dirs_exist_ok=True)
        shutil.rmtree(pages_backup)
    if static_backup and os.path.exists(static_backup):
        os.makedirs(STATIC_DIR, exist_ok=True)
        shutil.copytree(static_backup, STATIC_DIR, dirs_exist_ok=True)
        shutil.rmtree(static_backup)

    # Use token if available (prevents rate limits)
    headers = {}
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers = {"Authorization": f"token {github_token}"}

    res = requests.get(GIST_API, headers=headers)
    res.raise_for_status()

    for gist in res.json():
        desc = gist.get("description") or ""
        if desc.startswith("blog: "):
            file_meta = list(gist["files"].values())[0]
            raw_url = file_meta["raw_url"]
            content = requests.get(raw_url, headers=headers).text

            filepath = os.path.join(CONTENT_DIR, f"{gist['id']}.rst")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Synced: {desc}")


if __name__ == "__main__":
    fetch_blog_gists()
