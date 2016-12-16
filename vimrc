" Search for plugins: http://vimawesome.com

" vim != vi
set nocompatible

" Load all plugins
execute pathogen#infect()
filetype plugin indent on
syntax on

" Use smart autocompletion
set omnifunc=syntaxcomplete#Complete

" Add italic escape support
let &t_ZH="\e[3m"
let &t_ZR="\e[23m"

" Set escapesequence timeout
set timeoutlen=1000
set ttimeoutlen=10

set hidden
set ttyfast
set number
set fileformat=unix
set encoding=utf-8
set colorcolumn=80
set cursorline

set backup
set writebackup

set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab

set wildmenu
set showmatch
set incsearch
" set hlsearch
" nnoremap <esc> :nohlsearch<CR>
set foldenable
set nowrap
set laststatus=2
set history=1024
set updatetime=250

" The status line already has the mode info
set noshowmode

" Strip trailing whitespaces
autocmd BufWritePre * %s/\s\+$//e

" Customise look and feel
" if horizontal fillchar can be changed, it should be the \u2500
let &fillchars .= ",vert:\u2502"

highlight LineNr       ctermbg=black ctermfg=darkgray
highlight ColorColumn  ctermbg=black
highlight CursorLineNr ctermbg=darkgray ctermfg=white cterm=bold
highlight CursorLine   ctermbg=black cterm=bold
highlight Comment      ctermfg=darkgray cterm=italic
highlight Constant     ctermfg=darkred
highlight Normal       ctermfg=lightgray
highlight Visual       cterm=reverse
highlight VertSplit    cterm=none ctermfg=darkgray
highlight EndOfBuffer  ctermfg=darkgray
highlight Pmenu        ctermbg=black ctermfg=lightgray
highlight PmenuSel     ctermbg=darkgray ctermfg=white cterm=bold
highlight PmenuSbar    ctermbg=darkgray
highlight PmenuThumb   ctermbg=lightgray
highlight SignColumn   ctermbg=none

" plugin: nerdtree
let NERDTreeShowHidden = 1

" plugin: buftabline
highlight BufTabLineCurrent ctermbg=lightgray ctermfg=black
highlight BufTabLineActive  ctermbg=darkgray ctermfg=white
highlight BufTabLineHidden  ctermbg=darkgray ctermfg=lightgray
highlight BufTabLineFill    ctermbg=darkgray

" plugin: gitgutter
let g:gitgutter_override_sign_column_highlight = 0

" plugin: indentLine
let g:indentLine_color_term   = 0
let g:indentLine_char         = "\u2502"
let g:indentLine_enabled      = 1
let g:vim_json_syntax_conceal = 0

" plugin: undotree
set undodir=~/.vim/undodir
set undofile
set undolevels=8192
let g:undotree_WindowLayout         = 4
let g:undotree_SplitWidth           = 32
let g:undotree_DiffPanelHeight      = 8
let g:undotree_HighlightChangedText = 0
let g:undotree_SetFocusWhenToggle   = 1

" plugin: lightline
" More on predefined components :help g:lightline.component
let g:lightline = {
    \ 'enable': {
        \ 'statusline': 1,
        \ 'tabline': 0
    \ },
    \ 'colorscheme': 'space16',
    \ 'active': {
        \ 'left': [
            \ ['mode'],
            \ ['paste'],
            \ ['relativepath', 'modified']
        \ ],
        \ 'right': [
            \ ['percent'],
            \ ['lineinfo'],
            \ ['fileformat', 'fileencoding', 'filetype']
        \ ]
    \ },
    \ 'inactive': {
        \ 'left'  : [
            \ ['mode'],
            \ ['relativepath', 'modified']
        \ ],
        \ 'right' : [
            \ ['percent'],
            \ ['lineinfo'],
            \ ['fileformat', 'fileencoding', 'filetype']
        \ ]
    \ },
    \ 'subseparator': {
        \ 'left': '',
        \ 'right': ''
    \ }
\ }

" Keybindings
"let &<F1>="\e[11~"
set <F1>=[11~
set <F2>=[12~
set <F3>=[13~
set <F4>=[14~

set pastetoggle=<F4>
nnoremap <F1>  :CtrlPMixed<CR>
nnoremap <F2>  :NERDTreeToggle<CR>
nnoremap <F3>  :UndotreeToggle<CR>
nnoremap <CR>  i<CR><ESC>

