# Shell

整站抓取
```
wget -c -m -k https://ip.cn
```

-H 允许外链递归，针对某些静态cdn资源是外链的情况
-D 指定 域名列表
-U 指定 AGENT

去除?及后缀的2种方法
```
echo 'www.baidu.com?a=b' | sed 's/\?[^?]*$//'
echo 'www.baidu.com?a=b' | awk -F "\?" '{print $1}'
```

去除当前目录下所有文件名的?及后缀
```
find . -name "*\?*" | xargs -I ls | awk -F "\?" '{print "mv "$0" "$1}' | sh
```
