# 微服务

## 微服务的发展

- 单体应用

- 模块化、组件化

- 前后端分离

- SOA

- 微服务

- 服务治理

架构形式随着业务的发展和技术的发展共同演进

## 认证鉴权

- 分布式会话（耗空间），客户端每次访问更新会话过期时间
- JWT（耗CPU），客户端每次访问需要验证签名，增加CPU资源损耗，中途需要重新验证用户体验不好

分布式会话的好处: 支持多终端会话管理
