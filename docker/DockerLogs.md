## Docker Logs

### Nginx

nginx 官方镜像，使用了一种方式，让日志输出到 STDOUT，也就是 创建一个符号链接 /var/log/nginx/access.log 到 /dev/stdout

`/etc/logrotate.d/nginx`
```
root@nginx:/# cat /etc/logrotate.d/nginx
/var/log/nginx/*.log {
        daily
        missingok
        rotate 52
        compress
        delaycompress
        notifempty
        create 640 nginx adm
        sharedscripts
        postrotate
                if [ -f /var/run/nginx.pid ]; then
                        kill -USR1 `cat /var/run/nginx.pid`
                fi
        endscript
}
```

### Httpd

httpd 使用的是 让其输出到指定文件 ，正常日志输出到 /proc/self/fd/1 (STDOUT) ，错误日志输出到 /proc/self/fd/2 (STDERR)

