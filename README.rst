===================================
gist-blog – Serverless headless CMS
===================================

**Zero Git friction.** Write in reStructuredText → Public Gist → auto-deployed Pelican blog with full-text search.

How to publish a post
=====================
1. Create a **public** Gist on GitHub.
2. Description must start with: `blog: Your Post Title`
3. File must be valid reST with field-list metadata (see example in the original prompt).
4. Save. The site updates automatically every 4 hours (or manually trigger the GitHub Action).

.. code-block:: rst

    ================
    The Post Title
    ================
    :date: 2026-04-02 14:00
    :category: Tech
    :tags: python, automation
    :summary: This text appears **only** in the post listings (homepage, archives, etc.).
    :image: https://picsum.photos/id/1015/800/450

    Post body starts here...


Search page lives at `/pages/search/`.

**Important:** Change `USERNAME = "barseghyanartur"` in `fetch_gists.py` to **your own GitHub username** before the first run.

Local development
=================
1. Clone the repo
-----------------

::

    git clone https://github.com/YOURUSERNAME/YOUR-REPO.git
    cd YOUR-REPO

2. Install dependencies
-----------------------

::

    make install

3. Pull your latest Gists
-------------------------

::

    make fetch

4. One-time build + static preview
----------------------------------
::

    make serve

# → http://localhost:8000

5. LIVE development mode (recommended)
--------------------------------------
::

    make dev

# → Auto-rebuilds on any change + live server at http://localhost:8000
