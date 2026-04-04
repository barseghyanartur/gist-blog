VERSION := 0.1
SHELL := /bin/bash
# Makefile for project
VENV := .venv/bin/activate
UNAME_S := $(shell uname -s)

# Makefile for Gist2Pelican – Serverless Headless CMS
# Run "make help" to see all commands

.PHONY: help install fetch build clean serve dev

PYTHON := python3
PELICAN := pelican
PIP := pip3
CONFFILE := pelicanconf.py

help:
	@echo "Gist2Pelican Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make install   → Install all Python dependencies"
	@echo "  make fetch     → Pull latest blog Gists + regenerate search index"
	@echo "  make build     → Fetch + build static site (output/)"
	@echo "  make serve     → Build + serve statically on http://localhost:8000"
	@echo "  make dev       → Fetch + LIVE RELOAD + auto-serve (best for local editing)"
	@echo "  make clean     → Remove generated output/"
	@echo ""
	@echo "After 'make dev' open → http://localhost:8000"

create-venv:
	uv venv

install: create-venv
	uv pip install -r requirements.txt

fetch:
	@echo "Fetching Gists and generating search index..."
	uv run python fetch_gists.py
	uv run python generate_search_index.py

build: fetch
	@echo "Building site with Pelican..."
	uv run env SITEURL='' $(PELICAN) -s $(CONFFILE)

clean:
	rm -rf output/
	@echo "✅ Cleaned. content/ (including static pages) was preserved."

serve: build
	@echo "🚀 Serving built site at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	uv run env SITEURL='' python -m http.server 8000 --directory output

only-serve:
	@echo "🚀 Serving built site at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	uv run env SITEURL='' python -m http.server 8000 --directory output

dev: fetch
	@echo "🚀 Starting DEV mode with live reload"
	@echo "→ Changes to any .rst file in content/ will auto-rebuild"
	@echo "→ Server running at http://localhost:8000"
	@echo ""
	@echo "Tip: In another terminal run 'make fetch' to pull new Gists while dev server is running."
	uv run env SITEURL='' $(PELICAN) -s $(CONFFILE) --autoreload --listen
