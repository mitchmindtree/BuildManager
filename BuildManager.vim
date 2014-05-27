" 
" BuildManager.vim
"
" An assistant script to help automate the C++ compilation process in Vim.
"

function ManageBuild(dir, ...)
    let string = a:dir
    if a:0 > 0
        if match(a:1, "-r") != -1
            let string = "-r " . string
        endif
        if match(a:2, "rust") != -1
            let string = "--lang=rust " . string
        endif
    endif
    execute "!python ~/.vim/plugin/BuildManager/BuildManager.py " . string
endfunction

com -nargs=* Build call ManageBuild(getcwd(), <f-args>)
    
" Map call to '\r'
autocmd FileType cpp nnoremap <Leader>r :Build -r<CR>
autocmd FileType h nnoremap <Leader>r :Build -r<CR>
autocmd FileType rust nnoremap <Leader>r :Build -r rust<CR>
