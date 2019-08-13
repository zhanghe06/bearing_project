# OpenResty

[官网](http://openresty.org/en/)

[最佳实践](https://legacy.gitbook.com/book/moonbingbing/openresty-best-practices/details)


## 安装
```bash
brew update
brew install pcre openssl curl

brew install openresty/brew/openresty
```

```
==> openresty-openssl
openresty-openssl is keg-only, which means it was not symlinked into /usr/local,
because only for use with OpenResty.

If you need to have openresty-openssl first in your PATH run:
  echo 'export PATH="/usr/local/opt/openresty-openssl/bin:$PATH"' >> ~/.zshrc

For compilers to find openresty-openssl you may need to set:
  export LDFLAGS="-L/usr/local/opt/openresty-openssl/lib"
  export CPPFLAGS="-I/usr/local/opt/openresty-openssl/include"

For pkg-config to find openresty-openssl you may need to set:
  export PKG_CONFIG_PATH="/usr/local/opt/openresty-openssl/lib/pkgconfig"

==> openresty
To have launchd start openresty/brew/openresty now and restart at login:
  brew services start openresty/brew/openresty
Or, if you don't want/need a background service you can just run:
  openresty
```


```
➜  ~ /usr/local/Cellar/openresty/1.15.8.1/nginx/sbin/nginx -t
nginx: the configuration file /usr/local/etc/openresty/nginx.conf syntax is ok
nginx: configuration file /usr/local/etc/openresty/nginx.conf test is successful
```

## 创建目录
```
mkdir ~/work
cd ~/work
mkdir logs/ conf/
```

## 配置文件 conf/nginx.conf
```
worker_processes  1;
error_log logs/error.log;
events {
    worker_connections 1024;
}
http {
    server {
        listen 8080;
        location / {
            default_type text/html;
            content_by_lua_block {
                ngx.say("<p>hello, world</p>")
            }
        }
    }
}
```

## 启动
```
#PATH=/usr/local/openresty/nginx/sbin:$PATH
PATH=/usr/local/Cellar/openresty/1.15.8.1/nginx/sbin:$PATH
export PATH

nginx -p `pwd`/ -c conf/nginx.conf
```

## 验证

访问 [http://localhost:8080/](http://localhost:8080/)

浏览器出现 hello, world

## 关闭
```
#PATH=/usr/local/openresty/nginx/sbin:$PATH
PATH=/usr/local/Cellar/openresty/1.15.8.1/nginx/sbin:$PATH
export PATH

nginx -s stop
```
