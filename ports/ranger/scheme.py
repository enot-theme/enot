# enot -- earthy scheme, dichromacy-resistant
# generated from colors.json by the enot build, do not edit by hand
# colors are ANSI indices 0-15, the actual values come from the
# terminal palette (wezterm/enot-*.toml): one file for dark and light
# requires ranger >= 1.9.3

from __future__ import (absolute_import, division, print_function)

from ranger.gui.colorscheme import ColorScheme
from ranger.gui.color import (
    black, blue, cyan, green, magenta, red, white, yellow, default,
    normal, bold, reverse, dim, BRIGHT, default_colors,
)


class Scheme(ColorScheme):
    progress_bar_color = blue

    def use(self, context):  # pylint: disable=too-many-branches
        fg, bg, attr = default_colors

        if context.reset:
            return default_colors

        elif context.in_browser:
            attr = reverse if context.selected else normal
            if context.empty or context.error:
                bg = red
            if context.border:
                fg = default
            if context.media:
                fg = yellow if context.image else magenta
            if context.container:
                fg = red
            if context.directory:
                attr |= bold
                fg = blue + BRIGHT
            elif context.executable and not \
                    any((context.media, context.container,
                         context.fifo, context.socket)):
                attr |= bold
                fg = green + BRIGHT
            if context.socket:
                attr |= bold
                fg = magenta + BRIGHT
            if context.fifo or context.device:
                fg = yellow
                if context.device:
                    attr |= bold
                    fg += BRIGHT
            if context.link:
                fg = cyan if context.good else magenta
            if context.tag_marker and not context.selected:
                attr |= bold
                fg = white + BRIGHT if fg in (red, magenta) else red + BRIGHT
            # line_number appeared after 1.9.3: absent on the release
            if getattr(context, "line_number", False) and \
                    not context.selected:
                fg = default
                attr &= ~bold
            if not context.selected and (context.cut or context.copied):
                # cut/copied in grey (br_black); on an 8-color terminal
                # BRIGHT == 0 and black is replaced with dim white
                attr |= bold
                fg = black + BRIGHT
                if BRIGHT == 0:
                    attr |= dim
                    fg = white
            if context.main_column:
                if context.selected:
                    attr |= bold
                if context.marked:
                    attr |= bold
                    fg = yellow
            if context.badinfo:
                if attr & reverse:
                    bg = magenta
                else:
                    fg = magenta
            if context.inactive_pane:
                fg = cyan

        elif context.in_titlebar:
            attr |= bold
            if context.hostname:
                fg = red if context.bad else green
            elif context.directory:
                fg = blue
            elif context.tab and context.good:
                # active tab: reverse instead of upstream's green bg; a
                # green bg fails contrast under the terminal text color
                attr |= reverse
            elif context.link:
                fg = cyan

        elif context.in_statusbar:
            if context.permissions:
                if context.good:
                    fg = cyan
                elif context.bad:
                    fg = magenta
            if context.marked:
                attr |= bold | reverse
                fg = yellow + BRIGHT
            if context.frozen:
                attr |= bold | reverse
                fg = cyan + BRIGHT
            if context.message and context.bad:
                attr |= bold
                fg = red + BRIGHT
            if context.loaded:
                bg = self.progress_bar_color
            if context.vcsinfo:
                fg = blue
                attr &= ~bold
            if context.vcscommit:
                fg = yellow
                attr &= ~bold
            if context.vcsdate:
                fg = cyan
                attr &= ~bold

        if context.text and context.highlight:
            attr |= reverse

        if context.in_taskview:
            if context.title:
                fg = blue
            if context.selected:
                attr |= reverse
            if context.loaded:
                if context.selected:
                    fg = self.progress_bar_color
                else:
                    bg = self.progress_bar_color

        if context.vcsfile and not context.selected:
            attr &= ~bold
            # aligned with the vim scheme: changed is blue, conflict purple
            if context.vcsconflict:
                fg = magenta
            elif context.vcsuntracked:
                fg = cyan
            elif context.vcschanged:
                fg = blue
            elif context.vcsunknown:
                fg = red
            elif context.vcsstaged or context.vcssync:
                fg = green
            elif context.vcsignored:
                fg = default

        elif context.vcsremote and not context.selected:
            attr &= ~bold
            if context.vcssync or context.vcsnone:
                fg = green
            elif context.vcsbehind:
                fg = red
            elif context.vcsahead:
                fg = blue
            elif context.vcsdiverged:
                fg = magenta
            elif context.vcsunknown:
                fg = red

        return fg, bg, attr
