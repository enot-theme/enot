" enot -- earthy scheme, CIELAB, dichromacy-resistant
" generated from colors.json by the enot build, do not edit by hand
hi clear
if exists('syntax_on')
  syntax reset
endif
let g:colors_name = 'enot'

if &background ==# 'dark'
  hi Normal guifg=#e2d7b5 ctermfg=187 guibg=#292826 ctermbg=235 gui=NONE cterm=NONE
  hi NormalFloat guifg=#e2d7b5 ctermfg=187 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi FloatBorder guifg=#4e4d4c ctermfg=239 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi Cursor guifg=#292826 ctermfg=235 guibg=#e2d7b5 ctermbg=187 gui=NONE cterm=NONE
  hi CursorLine guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi CursorColumn guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi ColorColumn guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi CursorLineNr guifg=#beb69c ctermfg=144 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi LineNr guifg=#5f5e5c ctermfg=59 gui=NONE cterm=NONE
  hi SignColumn guifg=#5f5e5c ctermfg=59 gui=NONE cterm=NONE
  hi FoldColumn guifg=#5f5e5c ctermfg=59 gui=NONE cterm=NONE
  hi Folded guifg=#83817e ctermfg=244 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi VertSplit guifg=#4e4d4c ctermfg=239 gui=NONE cterm=NONE
  hi WinSeparator guifg=#4e4d4c ctermfg=239 gui=NONE cterm=NONE
  hi StatusLine guifg=#beb69c ctermfg=144 guibg=#3e3d3c ctermbg=237 gui=NONE cterm=NONE
  hi StatusLineNC guifg=#83817e ctermfg=244 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi TabLine guifg=#beb69c ctermfg=144 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi TabLineSel guifg=#e2d7b5 ctermfg=187 guibg=#292826 ctermbg=235 gui=NONE cterm=NONE
  hi TabLineFill guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi Pmenu guifg=#e2d7b5 ctermfg=187 guibg=#323130 ctermbg=236 gui=NONE cterm=NONE
  hi PmenuSel guifg=#e2d7b5 ctermfg=187 guibg=#4e4d4c ctermbg=239 gui=NONE cterm=NONE
  hi PmenuSbar guibg=#3e3d3c ctermbg=237 gui=NONE cterm=NONE
  hi PmenuThumb guibg=#4e4d4c ctermbg=239 gui=NONE cterm=NONE
  hi WildMenu guifg=#292826 ctermfg=235 guibg=#fde494 ctermbg=222 gui=NONE cterm=NONE
  hi Visual guibg=#3e3d3c ctermbg=237 gui=NONE cterm=NONE
  hi Search guifg=#292826 ctermfg=235 guibg=#fde494 ctermbg=222 gui=NONE cterm=NONE
  hi IncSearch guifg=#292826 ctermfg=235 guibg=#ad8764 ctermbg=137 gui=NONE cterm=NONE
  hi QuickFixLine guibg=#3e3d3c ctermbg=237 gui=NONE cterm=NONE
  hi MatchParen guibg=#4e4d4c ctermbg=239 gui=bold cterm=bold
  hi Conceal guifg=#83817e ctermfg=244 gui=NONE cterm=NONE
  hi Directory guifg=#79cad9 ctermfg=81 gui=NONE cterm=NONE
  hi Title guifg=#fde494 ctermfg=222 gui=bold cterm=bold
  hi ErrorMsg guifg=#d7a0a1 ctermfg=174 gui=bold cterm=bold
  hi WarningMsg guifg=#fde494 ctermfg=222 gui=NONE cterm=NONE
  hi MoreMsg guifg=#bab04d ctermfg=143 gui=NONE cterm=NONE
  hi ModeMsg guifg=#beb69c ctermfg=144 gui=NONE cterm=NONE
  hi Question guifg=#bab04d ctermfg=143 gui=NONE cterm=NONE
  hi NonText guifg=#4e4d4c ctermfg=239 gui=NONE cterm=NONE
  hi SpecialKey guifg=#4e4d4c ctermfg=239 gui=NONE cterm=NONE
  hi Whitespace guifg=#4e4d4c ctermfg=239 gui=NONE cterm=NONE
  hi Comment guifg=#83817e ctermfg=244 gui=italic cterm=italic
  hi Constant guifg=#c37fa1 ctermfg=175 gui=NONE cterm=NONE
  hi Number guifg=#c37fa1 ctermfg=175 gui=NONE cterm=NONE
  hi String guifg=#9ff5e3 ctermfg=158 gui=NONE cterm=NONE
  hi Identifier guifg=#79cad9 ctermfg=81 gui=NONE cterm=NONE
  hi Function guifg=#bab04d ctermfg=143 gui=NONE cterm=NONE
  hi Statement guifg=#d7a0a1 ctermfg=174 gui=NONE cterm=NONE
  hi Operator guifg=#e2d7b5 ctermfg=187 gui=NONE cterm=NONE
  hi PreProc guifg=#ad8764 ctermfg=137 gui=NONE cterm=NONE
  hi Type guifg=#fde494 ctermfg=222 gui=NONE cterm=NONE
  hi Special guifg=#ad8764 ctermfg=137 gui=NONE cterm=NONE
  hi SpecialChar guifg=#ad8764 ctermfg=137 gui=NONE cterm=NONE
  hi Tag guifg=#bab04d ctermfg=143 gui=NONE cterm=NONE
  hi Delimiter guifg=#beb69c ctermfg=144 gui=NONE cterm=NONE
  hi SpecialComment guifg=#83817e ctermfg=244 gui=bold cterm=bold
  hi Debug guifg=#ad8764 ctermfg=137 gui=NONE cterm=NONE
  hi Underlined guifg=#79cad9 ctermfg=81 gui=underline cterm=underline
  hi Error guifg=#d7a0a1 ctermfg=174 gui=bold cterm=bold
  hi Todo guifg=#292826 ctermfg=235 guibg=#fde494 ctermbg=222 gui=bold cterm=bold
  hi DiffAdd guibg=#413e2f ctermbg=58 gui=NONE cterm=NONE
  hi DiffDelete guifg=#d7a0a1 ctermfg=174 guibg=#3f2b2c ctermbg=52 gui=NONE cterm=NONE
  hi DiffChange guibg=#2e4144 ctermbg=24 gui=NONE cterm=NONE
  hi DiffText guibg=#2b5158 ctermbg=23 gui=NONE cterm=NONE
  hi diffAdded guifg=#bab04d ctermfg=143 gui=NONE cterm=NONE
  hi diffRemoved guifg=#d7a0a1 ctermfg=174 gui=NONE cterm=NONE
  hi diffChanged guifg=#79cad9 ctermfg=81 gui=NONE cterm=NONE
  hi DiagnosticError guifg=#d7a0a1 ctermfg=174 gui=NONE cterm=NONE
  hi DiagnosticWarn guifg=#fde494 ctermfg=222 gui=NONE cterm=NONE
  hi DiagnosticInfo guifg=#79cad9 ctermfg=81 gui=NONE cterm=NONE
  hi DiagnosticHint guifg=#9ff5e3 ctermfg=158 gui=NONE cterm=NONE
  hi DiagnosticUnderlineError gui=undercurl cterm=underline guisp=#d7a0a1
  hi DiagnosticUnderlineWarn gui=undercurl cterm=underline guisp=#fde494
  hi DiagnosticUnderlineInfo gui=undercurl cterm=underline guisp=#79cad9
  hi DiagnosticUnderlineHint gui=undercurl cterm=underline guisp=#9ff5e3
  hi SpellBad gui=undercurl cterm=underline guisp=#d7a0a1
  hi SpellCap gui=undercurl cterm=underline guisp=#79cad9
  hi SpellRare gui=undercurl cterm=underline guisp=#c37fa1
  hi SpellLocal gui=undercurl cterm=underline guisp=#9ff5e3
  let g:terminal_ansi_colors = ['#45423c', '#cb938b', '#b0a76c', '#a38e6a', '#4eb3c7', '#d18da8', '#4caaa2', '#d7d1c6', '#6f6d6a', '#e0b1a5', '#c6c487', '#fcdfa5', '#75e1f4', '#f0b7cd', '#7ce2dc', '#f8f3ec']
  let g:terminal_color_0 = '#45423c'
  let g:terminal_color_1 = '#cb938b'
  let g:terminal_color_2 = '#b0a76c'
  let g:terminal_color_3 = '#a38e6a'
  let g:terminal_color_4 = '#4eb3c7'
  let g:terminal_color_5 = '#d18da8'
  let g:terminal_color_6 = '#4caaa2'
  let g:terminal_color_7 = '#d7d1c6'
  let g:terminal_color_8 = '#6f6d6a'
  let g:terminal_color_9 = '#e0b1a5'
  let g:terminal_color_10 = '#c6c487'
  let g:terminal_color_11 = '#fcdfa5'
  let g:terminal_color_12 = '#75e1f4'
  let g:terminal_color_13 = '#f0b7cd'
  let g:terminal_color_14 = '#7ce2dc'
  let g:terminal_color_15 = '#f8f3ec'
else
  hi Normal guifg=#48443e ctermfg=238 guibg=#f4f2ee ctermbg=255 gui=NONE cterm=NONE
  hi NormalFloat guifg=#48443e ctermfg=238 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi FloatBorder guifg=#c4c2be ctermfg=251 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi Cursor guifg=#f4f2ee ctermfg=255 guibg=#48443e ctermbg=238 gui=NONE cterm=NONE
  hi CursorLine guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi CursorColumn guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi ColorColumn guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi CursorLineNr guifg=#64605c ctermfg=241 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi LineNr guifg=#b3b0ab ctermfg=145 gui=NONE cterm=NONE
  hi SignColumn guifg=#b3b0ab ctermfg=145 gui=NONE cterm=NONE
  hi FoldColumn guifg=#b3b0ab ctermfg=145 gui=NONE cterm=NONE
  hi Folded guifg=#9b9893 ctermfg=246 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi VertSplit guifg=#c4c2be ctermfg=251 gui=NONE cterm=NONE
  hi WinSeparator guifg=#c4c2be ctermfg=251 gui=NONE cterm=NONE
  hi StatusLine guifg=#64605c ctermfg=241 guibg=#d7d6d2 ctermbg=188 gui=NONE cterm=NONE
  hi StatusLineNC guifg=#9b9893 ctermfg=246 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi TabLine guifg=#64605c ctermfg=241 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi TabLineSel guifg=#48443e ctermfg=238 guibg=#f4f2ee ctermbg=255 gui=NONE cterm=NONE
  hi TabLineFill guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi Pmenu guifg=#48443e ctermfg=238 guibg=#e7e5e1 ctermbg=254 gui=NONE cterm=NONE
  hi PmenuSel guifg=#48443e ctermfg=238 guibg=#c4c2be ctermbg=251 gui=NONE cterm=NONE
  hi PmenuSbar guibg=#d7d6d2 ctermbg=188 gui=NONE cterm=NONE
  hi PmenuThumb guibg=#c4c2be ctermbg=251 gui=NONE cterm=NONE
  hi WildMenu guifg=#f4f2ee ctermfg=255 guibg=#876923 ctermbg=94 gui=NONE cterm=NONE
  hi Visual guibg=#d7d6d2 ctermbg=188 gui=NONE cterm=NONE
  hi Search guifg=#f4f2ee ctermfg=255 guibg=#876923 ctermbg=94 gui=NONE cterm=NONE
  hi IncSearch guifg=#f4f2ee ctermfg=255 guibg=#632f05 ctermbg=160 gui=NONE cterm=NONE
  hi QuickFixLine guibg=#d7d6d2 ctermbg=188 gui=NONE cterm=NONE
  hi MatchParen guibg=#c4c2be ctermbg=251 gui=bold cterm=bold
  hi Conceal guifg=#9b9893 ctermfg=246 gui=NONE cterm=NONE
  hi Directory guifg=#0c6a96 ctermfg=24 gui=NONE cterm=NONE
  hi Title guifg=#876923 ctermfg=94 gui=bold cterm=bold
  hi ErrorMsg guifg=#9d5a5d ctermfg=124 gui=bold cterm=bold
  hi WarningMsg guifg=#876923 ctermfg=94 gui=NONE cterm=NONE
  hi MoreMsg guifg=#495a38 ctermfg=22 gui=NONE cterm=NONE
  hi ModeMsg guifg=#64605c ctermfg=241 gui=NONE cterm=NONE
  hi Question guifg=#495a38 ctermfg=22 gui=NONE cterm=NONE
  hi NonText guifg=#c4c2be ctermfg=251 gui=NONE cterm=NONE
  hi SpecialKey guifg=#c4c2be ctermfg=251 gui=NONE cterm=NONE
  hi Whitespace guifg=#c4c2be ctermfg=251 gui=NONE cterm=NONE
  hi Comment guifg=#9b9893 ctermfg=246 gui=italic cterm=italic
  hi Constant guifg=#974164 ctermfg=125 gui=NONE cterm=NONE
  hi Number guifg=#974164 ctermfg=125 gui=NONE cterm=NONE
  hi String guifg=#09797c ctermfg=23 gui=NONE cterm=NONE
  hi Identifier guifg=#0c6a96 ctermfg=24 gui=NONE cterm=NONE
  hi Function guifg=#495a38 ctermfg=22 gui=NONE cterm=NONE
  hi Statement guifg=#9d5a5d ctermfg=124 gui=NONE cterm=NONE
  hi Operator guifg=#48443e ctermfg=238 gui=NONE cterm=NONE
  hi PreProc guifg=#632f05 ctermfg=160 gui=NONE cterm=NONE
  hi Type guifg=#876923 ctermfg=94 gui=NONE cterm=NONE
  hi Special guifg=#632f05 ctermfg=160 gui=NONE cterm=NONE
  hi SpecialChar guifg=#632f05 ctermfg=160 gui=NONE cterm=NONE
  hi Tag guifg=#495a38 ctermfg=22 gui=NONE cterm=NONE
  hi Delimiter guifg=#64605c ctermfg=241 gui=NONE cterm=NONE
  hi SpecialComment guifg=#9b9893 ctermfg=246 gui=bold cterm=bold
  hi Debug guifg=#632f05 ctermfg=160 gui=NONE cterm=NONE
  hi Underlined guifg=#0c6a96 ctermfg=24 gui=underline cterm=underline
  hi Error guifg=#9d5a5d ctermfg=124 gui=bold cterm=bold
  hi Todo guifg=#f4f2ee ctermfg=255 guibg=#876923 ctermbg=94 gui=bold cterm=bold
  hi DiffAdd guibg=#dde5d3 ctermbg=187 gui=NONE cterm=NONE
  hi DiffDelete guifg=#9d5a5d ctermfg=124 guibg=#e6cbcb ctermbg=181 gui=NONE cterm=NONE
  hi DiffChange guibg=#d7e4f1 ctermbg=153 gui=NONE cterm=NONE
  hi DiffText guibg=#bcd5eb ctermbg=146 gui=NONE cterm=NONE
  hi diffAdded guifg=#495a38 ctermfg=22 gui=NONE cterm=NONE
  hi diffRemoved guifg=#9d5a5d ctermfg=124 gui=NONE cterm=NONE
  hi diffChanged guifg=#0c6a96 ctermfg=24 gui=NONE cterm=NONE
  hi DiagnosticError guifg=#9d5a5d ctermfg=124 gui=NONE cterm=NONE
  hi DiagnosticWarn guifg=#876923 ctermfg=94 gui=NONE cterm=NONE
  hi DiagnosticInfo guifg=#0c6a96 ctermfg=24 gui=NONE cterm=NONE
  hi DiagnosticHint guifg=#09797c ctermfg=23 gui=NONE cterm=NONE
  hi DiagnosticUnderlineError gui=undercurl cterm=underline guisp=#9d5a5d
  hi DiagnosticUnderlineWarn gui=undercurl cterm=underline guisp=#876923
  hi DiagnosticUnderlineInfo gui=undercurl cterm=underline guisp=#0c6a96
  hi DiagnosticUnderlineHint gui=undercurl cterm=underline guisp=#09797c
  hi SpellBad gui=undercurl cterm=underline guisp=#9d5a5d
  hi SpellCap gui=undercurl cterm=underline guisp=#0c6a96
  hi SpellRare gui=undercurl cterm=underline guisp=#974164
  hi SpellLocal gui=undercurl cterm=underline guisp=#09797c
  let g:terminal_ansi_colors = ['#4a4641', '#a25756', '#5c5b37', '#836933', '#0d7381', '#944c6b', '#2c7552', '#cac6bf', '#7b7670', '#632e28', '#50530f', '#493603', '#06444d', '#5d1c3e', '#105958', '#eeeeee']
  let g:terminal_color_0 = '#4a4641'
  let g:terminal_color_1 = '#a25756'
  let g:terminal_color_2 = '#5c5b37'
  let g:terminal_color_3 = '#836933'
  let g:terminal_color_4 = '#0d7381'
  let g:terminal_color_5 = '#944c6b'
  let g:terminal_color_6 = '#2c7552'
  let g:terminal_color_7 = '#cac6bf'
  let g:terminal_color_8 = '#7b7670'
  let g:terminal_color_9 = '#632e28'
  let g:terminal_color_10 = '#50530f'
  let g:terminal_color_11 = '#493603'
  let g:terminal_color_12 = '#06444d'
  let g:terminal_color_13 = '#5d1c3e'
  let g:terminal_color_14 = '#105958'
  let g:terminal_color_15 = '#eeeeee'
endif

hi! link Character String
hi! link Boolean Number
hi! link Float Number
hi! link Conditional Statement
hi! link Repeat Statement
hi! link Label Statement
hi! link Keyword Statement
hi! link Exception Statement
hi! link Include PreProc
hi! link Define PreProc
hi! link Macro PreProc
hi! link PreCondit PreProc
hi! link StorageClass Type
hi! link Structure Type
hi! link Typedef Type
hi! link EndOfBuffer NonText
hi! link CurSearch IncSearch
hi! link Added diffAdded
hi! link Removed diffRemoved
hi! link Changed diffChanged
hi! link GitSignsAdd diffAdded
hi! link GitSignsChange diffChanged
hi! link GitSignsDelete diffRemoved
hi! link GitGutterAdd diffAdded
hi! link GitGutterChange diffChanged
hi! link GitGutterDelete diffRemoved
