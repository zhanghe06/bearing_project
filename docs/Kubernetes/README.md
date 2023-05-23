# Kubernetes

[http://docs.kubernetes.org.cn](http://docs.kubernetes.org.cn)


```bash
helm install stable/redis --name my-redis
helm install stable/mariadb --name my-mariadb
helm install stable/rabbitmq --name my-rabbitmq
helm install stable/prometheus --name my-prometheus
helm install stable/nginx-ingress --name my-nginx --set rbac.create=true
helm list my
kubectl get po -o wide
```

~~安装Dashboard~~
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
```

安装新版Dashboard

[https://github.com/kubernetes/dashboard](https://github.com/kubernetes/dashboard)
```bash
# 下载需要翻墙
wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
# 安装不要翻墙
kubectl apply -f recommended.yaml
```

或者通过Helm方式
```
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard
```

获取Token
```bash
kubectl -n kube-system describe secret default| awk '$1=="token:"{print $2}'
```

开启代理（允许本地访问Dashboard）
```
➜  ~ kubectl proxy
Starting to serve on 127.0.0.1:8001
```

开启代理（允许远程访问Dashboard）
```
➜  ~ kubectl proxy --address='0.0.0.0' --port=8001 --accept-hosts='^*$'
Starting to serve on [::]:8001
```

登录

[~~K8s Dashboard~~](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/overview?namespace=default)

[K8s Dashboard 新版](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/)

输入令牌


ingress 安装

自 Kubernetes 1.6版本开始，API Server启用了RBAC授权

RBAC: 基于角色的权限访问控制（Role-Based Access Control）

https://kubernetes.github.io/ingress-nginx/deploy/#docker-for-mac

```
helm search repo ingress-nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install [RELEASE_NAME] ingress-nginx/ingress-nginx
helm uninstall [RELEASE_NAME]                       # 卸载
helm upgrade [RELEASE_NAME] [CHART] --install       # 更新
```
