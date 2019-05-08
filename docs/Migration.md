# Migration

项目数据迁移方案


```
项目A          项目M            项目B
A.id    ->     M.id       <-   B.id
A.data  ->     M.data     ->   B.data
```

主键同步
```graph
graph TB
    A.id-->M.id
    subgraph 项目A
    A.id---A.data
    end

    subgraph 项目M
    M.id
    end

    B.id-->M.id
    subgraph 项目B
    B.id---B.data
    end
```

数据同步
```graph
graph TB
    A.data-->M.data
    subgraph 项目A
    A.data
    end

    subgraph 项目M
    M.data
    end

    M.data-->B.data
    subgraph 项目B
    B.data
    end
```

