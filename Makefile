.DEFAULT_GOAL := help
# site matches the directory name; ports render from ports/*/port.json
.PHONY: help optimize palettes resolve report render check build site all deploy

help: ## show this help
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

optimize: ## recompute accents of the "enot" variant (enot.json)
	python3 optimize.py

palettes: ## rebuild palettes.json and preview.html
	python3 palette.py

resolve: ## color spec at three depths (colors.json)
	python3 resolve.py

report: ## dichromacy report cvd.html
	python3 cvd.py

render: ## render every port from colors.json (ports/*)
	python3 build.py

check: ## regression: invariants of colors.json and artifacts
	python3 check.py

build: optimize palettes resolve report render check ## full pipeline without the site (CI gate)

site: ## theme site (site/*.html + scheme files)
	python3 site.py

all: build site ## full cycle including the site

deploy: site ## rebuild the site and publish to GitHub Pages
	cd site && git add -A && (git diff --cached --quiet \
		|| (git commit -s -m "chore: rebuild site" && git push))
