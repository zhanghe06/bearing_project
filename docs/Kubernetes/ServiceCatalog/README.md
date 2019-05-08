# Service Catalog

Service Catalog（服务目录)是Kubernetes社区的孵化项目[Kubernetes Service Catalog Project](https://github.com/kubernetes-incubator/service-catalog)，旨在接入和管理第三方提供的Service Broker，使kubernetes上托管的应用可以使用service broker所代理的外部服务。

Service Catalog项目是基于k8s的OSB API实现，为k8s提供了如下功能:
- 注册第三方提供的Service Broker到k8s
- 将Service Broker所代理的服务(或者服务的变体)，提供给k8s的用户
- k8s用户可以发现可用的服务
- k8s用户可以请求创建新的服务实例
- k8s用户可以将服务实例绑定到一组pod上面
