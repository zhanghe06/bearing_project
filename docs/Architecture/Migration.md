# 迁移系统（Migration System）

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
graph LR
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


数据同步 - 表结构

字段 | 备注
--- | ---
id | 主键
resource_type | 资源类型
pk_source | 来源主键
pk_target | 目标主键
latest_time_source | 来源最后更新时间
latest_time_target | 目标最后更新时间
status_delete | 删除状态
delete_time | 删除时间
create_time | 创建时间
update_time | 更新时间
