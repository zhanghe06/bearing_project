# Mac

- ssh LC_CTYPE 警告
```
warning: setlocale: LC_CTYPE: cannot change locale (UTF-8): No such file or directory
```

解决方案
```
sudo vim /etc/ssh/ssh_config
注释掉   SendEnv LANG LC_*
```

## iterm & oh-my-zsh

oh-my-zsh 插件
```
cd ~/.oh-my-zsh/custom/plugins/
git clone https://github.com/zsh-users/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting
```

vim ~/.zshrc
```
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
)
```
