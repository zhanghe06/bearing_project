# Kubernetes


```bash
helm install stable/redis --name my-redis
helm install stable/mariadb --name my-mariadb
helm install stable/rabbitmq --name my-rabbitmq
helm install stable/prometheus --name my-prometheus
helm install stable/nginx-ingress --name my-nginx --set rbac.create=true
helm list my
kubectl get po -o wide
```


获取Token
```bash
kubectl -n kube-system describe secret default| awk '$1=="token:"{print $2}'
```

登录 [K8s Dashboard](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/overview?namespace=default)
输入令牌


ingress 安装

自 Kubernetes 1.6版本开始，API Server启用了RBAC授权

https://kubernetes.github.io/ingress-nginx/deploy/#docker-for-mac
