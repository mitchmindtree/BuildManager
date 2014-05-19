" 
" BuildManager.vim
"
" An assistant script to help automate the C++ compilation process in Vim.
"

function ManageBuild(dir, ...)
    if a:0 == 1
        if match(a:1, "-r") != -1
            let a:dir = "-r " . a:dir
        endif
    endif
    execute "!python ~/.vim/plugin/BuildManager/BuildManager.py " . " " . a:dir
endfunction

com -nargs=* Build call ManageBuild(getcwd(), <f-args>)
    
