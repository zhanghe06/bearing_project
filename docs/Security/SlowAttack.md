# 慢速攻击

https://www.cnblogs.com/wpjamer/p/9030259.html

CC攻击的变异品种

这个攻击的基本原理如下：
对任何一个开放了HTTP访问的服务器HTTP服务器，先建立了一个连接，指定一个比较大的content-length，然后以非常低的速度发包，比如1-10s发一个字节，然后维持住这个连接不断开。
如果客户端持续建立这样的连接，那么服务器上可用的连接将一点一点被占满，从而导致拒绝服务。

慢速攻击的分类

- Slow headers
- Slow body
- Slow read


使用较多的慢速攻击工具有：Slowhttptest和Slowloris。

https://blog.csdn.net/Bul1et/article/details/83651010
