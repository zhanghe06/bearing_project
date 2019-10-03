#  任务系统（Task System）

序列图

```graph
sequenceDiagram
    participant Task API
    participant Task Queue
    Note over Task Queue,Task Scheduler: Task Broker
    Task API->>Task Queue: Create Task
    Task Queue-->>Task API: Create Success
    loop Task Check
        Task Scheduler->>Task Scheduler: Check Task Status
        Task Scheduler->>Task Queue: Fetch Task
        Task Queue-->>Task Scheduler: Fetch Success
    end
    Task Scheduler->>Task Worker: Send Task
    Task Worker-->>Task Scheduler: Send Success
    Task Worker->>Task Backend: Save Task Result
    Task Backend-->>Task Worker: Save Success
```

- 限速
- 重试
- 回滚
- 分布式
- 高可用
- 高并发

到底解决了什么问题，又会引入什么新的问题？

问题思考：

1. 分布式任务，冲突怎么解决，包括手动任务与自动任务冲突
2. 多进程模式，任务消费需要关心顺序么
3. 如果不是幂等操作，任务不能重试
4. 是否需要考虑任务编排（即包含子任务时，子任务执行顺序，回滚顺序），还是说每个任务都是整体

