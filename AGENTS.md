# AGENTS.md - gist-blog

**Repository**: https://github.com/barseghyanartur/gist-blog
**Maintainer**: Artur Barseghyan <artur.barseghyan@gmail.com>

---

## 1. Project mission (never deviate)

> Zero-friction serverless blogging where **public GitHub Gists** are the single source of truth and Pelican builds a clean, fast, fully static site with search.

- Write posts as reStructuredText inside public Gists (description must start with `blog: `).
- Metadata lives in reST field lists (`:date:`, `:category:`, `:tags:`, `:summary:`, `:image:`).
- Automatic periodic sync → Pelican build → GitHub Pages deployment.
- Full-text search (Lunr.js) and beautiful post-list previews are built-in.
- Local development with `make dev` must always work exactly like production.

**Scope note**: The system must stay extremely simple — no database, no backend, no extra services. Everything is driven by Gists + Pelican + GitHub Actions.

---

## 2. Architecture

### Core pipeline

1. **fetch_gists.py** — scans public Gists, keeps only those with `blog: ` prefix, preserves `/content/pages/` static pages, writes `.rst` files using Gist ID as filename.
2. **generate_search_index.py** — scans all `.rst` files and creates a client-side Lunr.js index (`static/search_index.json`).
3. **pelicanconf.py** — Pelican configuration + `article_generator_finalized` signal that:
   - Injects `:image:` preview at the top of list summaries
   - Uses `:summary:` (if present) or falls back to Pelican default
   - Appends “Originally published as GitHub Gist #xxxxxx” link to full post content
4. **GitHub Actions** (`.github/workflows/deploy.yml`) — runs every 4 hours + manual trigger → fetch → build → deploy to `gh-pages`.

### Key files

| File                        | Purpose |
|-----------------------------|-------|
| `fetch_gists.py`            | Gist → content/ sync (preserves pages/) |
| `pelicanconf.py`            | Pelican config + metadata processing signal |
| `generate_search_index.py`  | Builds Lunr.js search index |
| `content/pages/search.rst`  | Static search page (preserved on every sync) |
| `Makefile`                  | Local dev commands (`make dev`, `make fetch`, etc.) |
| `.github/workflows/deploy.yml` | CI/CD cron + deploy |
| `requirements.txt`          | Python dependencies |

---

## 3. How to publish a post

Create a **public** GitHub Gist with:

```rst
================
Post Title Goes Here
================
:date: 2026-04-03 14:30
:category: Tech
:tags: python, pelican, automation
:summary: This text appears **only** in post listings (homepage, archives, tags, categories).
:image: https://picsum.photos/id/1015/800/450   # optional

Full post body starts here...
```

The site updates automatically on the next GitHub Action run (or trigger manually).

---

## 4. Local development

```bash
make install          # one-time
make fetch            # pull latest Gists
make dev              # live reload server at http://localhost:8000
make serve            # static preview only
make clean            # remove output/
```

``uv`` is used behind the scenes.

```bash
uv pip install -r requirements.txt
uv run python fetch_gists.py
uv run python generate_search_index.py
```

All features (preview images, summaries, Gist links, search) work identically locally and in production.

---

## 5. Agent workflow: adding features or fixing bugs

1. **Check the mission** — any change must preserve zero-friction Gist-based authoring and full static output.
2. **Identify the correct location**:
   - Gist fetching / syncing → `fetch_gists.py`
   - Metadata processing (image, summary, Gist link) → `pelicanconf.py` signal
   - Search index → `generate_search_index.py`
   - Pelican config / URLs / menu → `pelicanconf.py`
   - Local commands → `Makefile`
   - Deployment → `.github/workflows/deploy.yml`
3. **Test locally** first with `make clean && make fetch && make dev`.
4. **Update AGENTS.md** if the architecture or workflow changes.
5. **Commit** with clear message and push — GitHub Actions will deploy.

---

## 6. Coding conventions

- Keep the entire system **under 10 files** whenever possible.
- No external runtime dependencies beyond `pelican`, `docutils`, `requests`.
- Use `article._content` (not `article.content`) when modifying rendered output.
- Prefer inline HTML for previews/links inside the Pelican signal (no custom templates).
- All Python code must run cleanly with `python 3.11+`.
- Line length: ≤ 100 characters.
- Always preserve backward compatibility for existing Gists.

Run locally:
```bash
make fetch
make dev
```

---

## 7. Forbidden

- Adding any backend, database, or external service.
- Requiring users to clone/commit/push anything (Gists must remain the only authoring surface).
- Removing or breaking the `:image:`, `:summary:`, or Gist-link features.
- Modifying the `content/pages/` preservation logic in `fetch_gists.py`.
- Changing the reST field-list metadata contract (`:date:`, `:category:`, `:tags:`, `:summary:`, `:image:`).

---

**This file is the single source of truth for any AI agent (or human) working on this blog.**  
Never deviate from the mission. Keep it simple, static, and Gist-driven.
