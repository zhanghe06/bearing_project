## Mac

- ssh LC_CTYPE 警告
```
warning: setlocale: LC_CTYPE: cannot change locale (UTF-8): No such file or directory
```

解决方案
```
sudo vim /etc/ssh/ssh_config
注释掉   SendEnv LANG LC_*
```
