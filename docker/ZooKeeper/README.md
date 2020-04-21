# ZooKeeper

ZK属于CP的中间件

[https://zookeeper.apache.org](https://zookeeper.apache.org)

而到底是用AP还是CP，是由业务决定的。

比如你是一个文件上传的服务器，用户可能上传几个g的文件，那么如果用一个AP的系统，拿到的可能是不可用的节点，这样返回给客户端重试，客户端肯定得疯掉，这时候就需要用CP。

而像 rpc 调用，调用失败了重试就好，成本代价都不大，这时候，用AP可能会更合适。
