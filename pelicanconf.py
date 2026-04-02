AUTHOR = "Artur Barseghyan"
SITENAME = "Dev Notes"
SITEURL = "/gist-blog"

PATH = "content"
# THEME = 'simple'                    # clean & responsive

TIMEZONE = "UTC"
DEFAULT_LANG = "en"

 # reST field lists (:date:, :category:, :tags:) are parsed automatically
DEFAULT_DATE = "fs"

ARTICLE_URL = "/gist-blog/posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "/gist-blog/posts/{date:%Y}/{date:%m}/{slug}/index.html"

PAGE_URL = "/gist-blog/pages/{slug}/"
PAGE_SAVE_AS = "/gist-blog/pages/{slug}/index.html"

STATIC_PATHS = ["static"]

MENUITEMS = (
    ("Home", "/gist-blog/"),
    ("Search", "/gist-blog/pages/search/"),
)

SUMMARY_MAX_LENGTH = 50
