# Helm（Docker for Mac）

Helm把Kubernetes资源(比如deployments、services或 ingress等) 打包到一个chart中，而chart被保存到chart仓库。通过chart仓库可用来存储和分享chart。

Helm使发布可配置，支持发布应用配置的版本管理，简化了Kubernetes部署应用的版本控制、打包、发布、删除、更新等操作。

https://github.com/helm/helm

https://helm.sh/

https://hub.helm.sh/



## 基本概念

- Helm          Kubernetes 的包管理工具
- Chart         一个 Helm 包
- Release       在 Kubernetes 集群上运行的 Chart 的一个实例
- Repository    用于发布和存储 Chart 的仓库
- Helm CLI      Helm 客户端组件
- Tiller        Helm 服务端组件


## 安装 Helm 并通过 Helm 安装示例
```
# 用 homebrew 安装 Helm
➜  ~ brew install kubernetes-helm

# 初始化本地 CLI 并 将 Tiller 安装到 Kubernetes cluster
➜  ~ helm init

# 查看当前的helme Charts包仓库
➜  ~ helm repo list 

# 更新本地 charts repo
➜  ~ helm repo update

# 在stable仓库搜索 redis应用
➜  ~ helm search stable/redis

# 安装 redis chart
➜  ~ helm install --name my-redis stable/redis

# helm查看部署的应用
➜  ~ helm list my

# 删除 redis
➜  ~ helm delete my-redis

# 删除 redis 并释放该名字以便后续使用
➜  ~ helm delete --purge my-redis
```

## 访问服务

开启代理（允许本地访问Dashboard）
```
➜  ~ kubectl proxy
Starting to serve on 127.0.0.1:8001
```

等待片刻，访问[K8S Dashboard UI](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/)


## Troubleshooting

helm install 报错
```
Error: could not find a ready tiller pod
```

查看pod状态
```
➜  ~ kubectl get po -n kube-system
NAME                                     READY   STATUS             RESTARTS   AGE
coredns-86c58d9df4-6pglj                 1/1     Running            2          70d
coredns-86c58d9df4-lqzqx                 1/1     Running            2          70d
etcd-docker-desktop                      1/1     Running            3          70d
kube-apiserver-docker-desktop            1/1     Running            3          70d
kube-controller-manager-docker-desktop   1/1     Running            14         70d
kube-proxy-c9t5f                         1/1     Running            2          70d
kube-scheduler-docker-desktop            1/1     Running            12         70d
kubernetes-dashboard-57df4db6b-pqbpf     1/1     Running            4          27d
tiller-deploy-664d6bdc7b-4tr4g           0/1     ImagePullBackOff   0          27m
```
tiller容器没起来，状态是CrashLoopBackOff

查看原因发现是镜像没有拉取
```
➜  ~ kubectl describe pod tiller-deploy-664d6bdc7b-4tr4g -n kube-system | grep Warning
  Warning  Failed     28m (x4 over 30m)    kubelet, docker-desktop  Failed to pull image "gcr.io/kubernetes-helm/tiller:v2.13.1": rpc error: code = Unknown desc = Error response from daemon: Get https://gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
  Warning  Failed     28m (x4 over 30m)    kubelet, docker-desktop  Error: ErrImagePull
  Warning  Failed     20m (x36 over 30m)   kubelet, docker-desktop  Error: ImagePullBackOff
```

配置代理（FQ）后重装

```
➜  ~ brew reinstall kubernetes-helm
```

再次查看pod状态
```
➜  ~ kubectl get po -n kube-system
NAME                                     READY   STATUS    RESTARTS   AGE
coredns-86c58d9df4-6pglj                 1/1     Running   3          70d
coredns-86c58d9df4-lqzqx                 1/1     Running   3          70d
etcd-docker-desktop                      1/1     Running   4          70d
kube-apiserver-docker-desktop            1/1     Running   4          70d
kube-controller-manager-docker-desktop   1/1     Running   15         70d
kube-proxy-c9t5f                         1/1     Running   3          70d
kube-scheduler-docker-desktop            1/1     Running   13         70d
kubernetes-dashboard-57df4db6b-pqbpf     1/1     Running   6          27d
tiller-deploy-664d6bdc7b-4tr4g           1/1     Running   0          77m
```


## 启动本地repo仓库服务

```
➜  ~ helm serve --address 0.0.0.0:8879
Regenerating index. This may take a moment.
Now serving you on 0.0.0.0:8879
```
或
```bash
nohup helm serve --address 0.0.0.0:8879 --repo-path /dcos/appstore/local-repo &
```
访问 [http://127.0.0.1:8879](http://127.0.0.1:8879)

查看仓库列表
```
➜  ~ helm repo list
NAME  	URL
stable	https://kubernetes-charts.storage.googleapis.com
local 	http://127.0.0.1:8879/charts
```

更新
```bash
helm repo index --url=http://192.168.1.100:8879 .
helm repo update
```
