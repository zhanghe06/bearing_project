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

安装Dashboard
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
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

登录 [K8s Dashboard](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/overview?namespace=default)
输入令牌


ingress 安装

自 Kubernetes 1.6版本开始，API Server启用了RBAC授权

RBAC: 基于角色的权限访问控制（Role-Based Access Control）

https://kubernetes.github.io/ingress-nginx/deploy/#docker-for-mac
