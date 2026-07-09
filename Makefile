.DEFAULT_GOAL := help
# vim, wezterm, mc, ranger and site match the directory names
.PHONY: help optimize palettes resolve report check wezterm vim mc ranger site all deploy

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

check: ## regression: invariants of colors.json and artifacts
	python3 check.py

wezterm: ## wezterm schemes from colors.json (wezterm/*.toml)
	python3 wezterm.py

vim: ## vim colorscheme from colors.json (vim/colors/*.vim)
	python3 vim.py

mc: ## mc skins from colors.json (mc/*.ini)
	python3 mc.py

ranger: ## ranger scheme on the terminal palette (ranger/colorschemes/*.py)
	python3 ranger.py

site: ## theme site (site/*.html + scheme files)
	python3 site.py

all: optimize palettes resolve report wezterm vim mc ranger site check ## full cycle

deploy: site ## rebuild the site and publish to GitHub Pages
	cd site && git add -A && (git diff --cached --quiet \
		|| (git commit -s -m "chore: rebuild site" && git push))
