# Replay Attack 重放攻击

- 本地重放
- 中间人重放

本地重放, 接口签名
中间人重放, 通过HTTPS解决

应对策略:
1、时间戳 timestamp
2、随机数 nonce = MD5(timestamp+rand(0,1000))
3、参数签名 sign
4、然后 timestamp + nonce + sign

服务端处理:
1、验证签名
2、第一次接受请求，对请求的timestamp进行规定时间如60s检验，如果符合那就进行下一步操作。
3、对nonce的处理，针对nonce访问redis判断是否存在，如果不存在，表示第一次访问，并在redis中插入nonce和设置过期时间如60；如果存在表示重复提交。

举例:
客户端
?nonce=md5(时间戳 + 随机数 + 特定字符串)&time=时间戳&random=随机数&sign=签名

服务端
验证 md5(用客户端传入的时间戳 + 随机数 + 特定字符串) 与 nonce 对比 验证是否是客户端的请求, 然后将这个 nonce 存入缓存当中, 同一个 nonce 如果已经存在, 则为重放攻击
