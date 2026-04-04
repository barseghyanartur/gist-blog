import os
from pelican import signals
from docutils.core import publish_parts

AUTHOR = "Artur Barseghyan"
SITENAME = "Dev Notes"
SITEURL = os.environ.get("SITEURL", "/gist-blog")

PATH = "content"
THEME = os.path.join(os.path.dirname(__file__), "themes", "custom")

TIMEZONE = "UTC"
DEFAULT_LANG = "en"

DEFAULT_DATE = "fs"

ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"

PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"

STATIC_PATHS = ["static"]

MENUITEMS = (
    ("Home", f"{SITEURL}"),
    ("Search", f"{SITEURL}/pages/search/"),
)

SUMMARY_MAX_LENGTH = 50

USERNAME = "barseghyanartur"  # <- MUST match the USERNAME in fetch_gists.py


def process_article_metadata(generator):
    """Attach optional :image: preview + :summary: to listings + add Gist link to full posts."""
    articles = generator.context.get("articles", [])

    for article in articles:
        # 1. Preview image (optional :image: field)
        image = article.metadata.get("image")

        # 2. Original Gist URL
        gist_id = None
        if hasattr(article, "source_path") and article.source_path:
            gist_id = os.path.basename(article.source_path).replace(".rst", "")
            article.gist_url = f"https://gist.github.com/{USERNAME}/{gist_id}"
        else:
            article.gist_url = None

        # 3. Preview HTML for listings only
        preview_html = ""
        if image:
            preview_html = (
                f'<img src="{image}" alt="Preview" class="preview-image" '
                f'style="max-width:100%; height:auto; border-radius:8px; '
                f'margin-bottom:1.5rem; display:block;">'
            )

        # 4. Use :summary: if provided, otherwise fall back to default + prepend image
        # get_summary returns functools.partial wrapping a memoized decorator
        # The memoized cache key is (self, siteurl) since the signature is get_summary(self, siteurl)
        has_custom_summary = (
            "summary" in article.metadata and article.metadata["summary"].strip()
        )

        get_summary_method = article.get_summary
        memoized_obj = get_summary_method.func.__self__
        cache_key = (article, article.get_siteurl())

        if has_custom_summary:
            new_summary = preview_html + article.metadata["summary"].strip()
            memoized_obj.cache[cache_key] = new_summary
        elif preview_html:
            from pelican.utils import truncate_html_words

            content = article.content
            max_len = article.settings.get("SUMMARY_MAX_LENGTH")
            if max_len is not None:
                suffix = article.settings.get("SUMMARY_END_SUFFIX", "...")
                new_summary = preview_html + truncate_html_words(
                    content, max_len, suffix
                )
            else:
                new_summary = preview_html + content
            memoized_obj.cache[cache_key] = new_summary

        # 5. Append Gist link ONLY to the full rendered post (not listings)
        if article.gist_url:
            gist_html = (
                f'<p style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #ddd; '
                f'font-size: 0.9rem; color: #555; text-align: right;">'
                f'Originally published as <a href="{article.gist_url}" '
                f'target="_blank" rel="noopener">GitHub Gist #{gist_id}</a></p>'
            )
            article._content += gist_html


signals.article_generator_finalized.connect(process_article_metadata)
