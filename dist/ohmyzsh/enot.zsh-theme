# enot -- earthy prompt, robust to dichromacy
# static port: colors are ANSI slots 0-15 taken from the terminal
# palette (see the wezterm port); one file serves the dark and light
# themes. Single-line prompt in the habamax-pikachu lineage:
# identity, venv, cwd, git, status char.
#
# roles: cwd blue (4), git branch magenta (5), dirty/staged star and
# ssh identity yellow (3), venv bright magenta (13), root identity
# red (1) bold; the status char is green (2) on a zero exit and
# red (1) otherwise -- enot guarantees red and green stay
# distinguishable under protanopia and deuteranopia.
#
# install: copy to ~/.oh-my-zsh/custom/themes/enot.zsh-theme and set
# ZSH_THEME="enot" in ~/.zshrc

setopt PROMPT_SUBST

# the venv plaque is drawn by the theme alone; otherwise the activate
# script (in zsh PS1==PROMPT) prepends its own uncolored "(name) " --
# a duplicate that breaks the style.
export VIRTUAL_ENV_DISABLE_PROMPT=1

autoload -Uz vcs_info
zstyle ':vcs_info:*' check-for-changes true
zstyle ':vcs_info:*' unstagedstr '%F{3}*%f'
zstyle ':vcs_info:*' stagedstr '%F{3}*%f'
zstyle ':vcs_info:git*' formats '%F{5}(%b%c%u)%f'
zstyle ':vcs_info:git*' actionformats '%F{5}(%b|%a%c%u)%f'
zstyle ':vcs_info:*' enable git

enot_precmd() {
  enot_status=$?
  vcs_info
}
autoload -U add-zsh-hook
add-zsh-hook precmd enot_precmd

# root -- a persistent root@host plaque (visible even without ssh,
# including after `sudo su`); otherwise user@host, ssh sessions only.
enot_identity_segment() {
  if [[ "$EUID" -eq 0 ]]; then
    print -n '%F{1}%B%n@%m%b%f '
  elif [[ -n "$SSH_CONNECTION" || -n "$SSH_TTY" ]]; then
    print -n '%F{3}%n@%m%f '
  fi
}

enot_venv_segment() {
  if [[ -n "$VIRTUAL_ENV" ]]; then
    # project name from VIRTUAL_ENV_PROMPT (set by uv/venv); fallback --
    # the path basename, and for the ".venv"/"venv" convention at the
    # project root -- the parent directory name.
    local name="$VIRTUAL_ENV_PROMPT"
    if [[ -z "$name" ]]; then
      name="${VIRTUAL_ENV:t}"
      [[ "$name" == ".venv" || "$name" == "venv" ]] && name="${VIRTUAL_ENV:h:t}"
    fi
    print -n "%F{13}(${name})%f "
  elif [[ -n "$CONDA_DEFAULT_ENV" && "$CONDA_DEFAULT_ENV" != "base" ]]; then
    print -n "%F{13}(${CONDA_DEFAULT_ENV})%f "
  fi
}

# the char (# for root, $ for a user) is a signal independent from the
# color: the color follows only the last exit code, same for both.
enot_prompt_char() {
  local char='$'
  [[ "$EUID" -eq 0 ]] && char='#'
  if [[ "$enot_status" -eq 0 ]]; then
    print -n "%F{2}${char}%f "
  else
    print -n "%F{1}${char}%f "
  fi
}

PROMPT='$(enot_identity_segment)$(enot_venv_segment)%F{4}%~%f ${vcs_info_msg_0_} $(enot_prompt_char)'
