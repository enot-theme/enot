.DEFAULT_GOAL := help
# the site is the sibling Astro repo (symlink site -> ../site); the
# pipeline feeds it a data bundle, the site repo's CI builds and deploys
.PHONY: help optimize resolve render assets check build sitedata all deploy

help: ## show this help
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

optimize: ## recompute the theme accents and ANSI slots (enot.json)
	python3 pipeline/optimize.py

resolve: ## color spec at three depths (colors.json)
	python3 pipeline/resolve.py

render: ## render every port from colors.json (ports/*)
	python3 pipeline/build.py

assets: ## README design reference SVGs (docs/assets/*)
	python3 pipeline/assets.py

check: ## regression: invariants of colors.json and artifacts
	python3 pipeline/check.py

build: optimize resolve render assets check ## full pipeline (CI gate)

sitedata: ## emit the site data bundle into build/site (needs build)
	python3 pipeline/sitedata.py

all: build ## full pipeline; the site is a separate Astro repo

deploy: build sitedata ## sync the data bundle into the Astro site and push (site CI deploys)
	cp build/site/site.json site/src/data/site.json
	cp build/site/llms.txt build/site/llms-full.txt site/public/
	cp -R build/site/downloads/* site/public/
	cd site && git add -A && (git diff --cached --quiet \
		|| (git commit -s -m "chore: sync theme data" && git push))
