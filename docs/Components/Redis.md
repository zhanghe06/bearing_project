# Redis

默认情况下，每个redis实例都会维护自己的连接池
可以直接建立一个连接池，实例化对象的时候使用连接池作为参数，这样可以实现多个redis实例共享连接池


## 极端业务场景

- 新闻应用中的热点新闻内容；
- 活动系统中某个用户疯狂参与的活动的活动配置；
- 商城秒杀系统中，最吸引用户眼球，性价比最高的商品信息；
- 论坛中的大型持久盖楼活动；
- 聊天室系统中热门聊天室的消息列表；


## 优化方向

- Hot Key 集群请求倾斜
    - 本地缓存（占用业务资源）
    - 分片打散（推荐，需要业务支持）
- Big Key 集群内存倾斜
    - 对 big key 存储的数据 （big value）进行拆分
        - big value 是个大 json: 使用 mget、mset 将内容打散（取 mget key1, key2 ... keyN；存 mset key1, key2 ... keyN）
        - big value 是个大 list: 变成value1，value2… valueN
- Die Key 死键
    - 已过期未清理
    - 没有业务使用
- 缓存雪崩
    - 坡度过期
- 缓存穿透
    - 缓存空数据
- keys 模糊匹配
    - 禁用keys，用set替代

非字符串的 BigKey, 不要使用del删除（会block实例）, 使用hscan、sscan、zscan等迭代方式渐进删除，同时注意防止BigKey过期时间自动删除问题


参考：

[https://juejin.im/post/5c19be51f265da615c593351](https://juejin.im/post/5c19be51f265da615c593351)


## 读取数据类型

默认读取的是字节，如需字符串，需要设置`decode_responses=True`

```
import redis

redis_client = redis.Redis(host='localhost', port=6379,
                 db=0, password=None,
                 decode_responses=True)
```
