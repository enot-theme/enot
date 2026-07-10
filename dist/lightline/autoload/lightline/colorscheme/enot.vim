" enot -- earthy scheme, CIELAB, dichromacy-resistant
" generated from colors.json by the enot build, do not edit by hand
" both themes in one file: the palette follows &background at load;
" after switching background call lightline#init(), then
" lightline#colorscheme() and lightline#update()

if &background ==# 'light'
  let s:bg0 = [ '#f4f2ee', 255 ]
  let s:bg1 = [ '#e7e5e1', 254 ]
  let s:bg2 = [ '#d7d6d2', 188 ]
  let s:fg0 = [ '#48443e', 238 ]
  let s:fg1 = [ '#64605c', 241 ]
  let s:comment = [ '#9b9893', 246 ]
  let s:red = [ '#9d5a5d', 124 ]
  let s:green = [ '#495a38', 22 ]
  let s:yellow = [ '#876923', 94 ]
  let s:blue = [ '#0c6a96', 24 ]
  let s:purple = [ '#974164', 125 ]
else
  let s:bg0 = [ '#292826', 235 ]
  let s:bg1 = [ '#323130', 236 ]
  let s:bg2 = [ '#3e3d3c', 237 ]
  let s:fg0 = [ '#e2d7b5', 187 ]
  let s:fg1 = [ '#beb69c', 144 ]
  let s:comment = [ '#83817e', 244 ]
  let s:red = [ '#d7a0a1', 174 ]
  let s:green = [ '#bab04d', 143 ]
  let s:yellow = [ '#fde494', 222 ]
  let s:blue = [ '#79cad9', 81 ]
  let s:purple = [ '#c37fa1', 175 ]
endif

let s:p = {'normal': {}, 'inactive': {}, 'insert': {}, 'replace': {}, 'visual': {}, 'tabline': {}}

" mode chips on accent fills, text is bg0: contrast held by the spec
let s:p.normal.left = [ [ s:bg0, s:blue ], [ s:fg0, s:bg2 ] ]
let s:p.normal.middle = [ [ s:comment, s:bg1 ] ]
let s:p.normal.right = [ [ s:fg0, s:bg2 ], [ s:fg1, s:bg1 ] ]
let s:p.normal.error = [ [ s:bg0, s:red ] ]
let s:p.normal.warning = [ [ s:bg0, s:yellow ] ]
let s:p.insert.left = [ [ s:bg0, s:green ], [ s:fg0, s:bg2 ] ]
let s:p.replace.left = [ [ s:bg0, s:red ], [ s:fg0, s:bg2 ] ]
let s:p.visual.left = [ [ s:bg0, s:purple ], [ s:fg0, s:bg2 ] ]
let s:p.inactive.left = [ [ s:comment, s:bg1 ], [ s:comment, s:bg1 ] ]
let s:p.inactive.middle = [ [ s:comment, s:bg1 ] ]
let s:p.inactive.right = [ [ s:comment, s:bg1 ], [ s:comment, s:bg1 ] ]
let s:p.tabline.left = [ [ s:fg1, s:bg1 ] ]
let s:p.tabline.tabsel = [ [ s:bg0, s:blue ] ]
let s:p.tabline.middle = [ [ s:comment, s:bg1 ] ]
let s:p.tabline.right = [ [ s:fg1, s:bg1 ] ]

let g:lightline#colorscheme#enot#palette = lightline#colorscheme#flatten(s:p)
