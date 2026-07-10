# enot -- earthy prompt, robust to dichromacy
# static port: colors are ANSI slots 0-15 taken from the terminal
# palette (see the wezterm port); one file serves the dark and light
# themes. Minimal single-line prompt in the robbyrussell lineage.
#
# roles: cwd blue (4), git yellow (3), dirty red (1); the arrow is
# green (2) on a zero exit and red (1) otherwise -- enot guarantees
# red and green stay distinguishable under protanopia and deuteranopia.
#
# install: copy to ~/.oh-my-zsh/custom/themes/enot.zsh-theme and set
# ZSH_THEME="enot" in ~/.zshrc

PROMPT='%(?:%F{2}❯%f:%F{1}❯%f) %F{4}%c%f $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%F{3}git:("
ZSH_THEME_GIT_PROMPT_SUFFIX="%f "
ZSH_THEME_GIT_PROMPT_DIRTY="%F{3})%F{1}*"
ZSH_THEME_GIT_PROMPT_CLEAN="%F{3})"
