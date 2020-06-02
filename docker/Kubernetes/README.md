## Kubernetes

https://kubernetes.io/cn/

https://kubernetes.io/cn/docs/tutorials/kubernetes-basics/


指定命名空间和服务名称进入容器
```bash
kubectl -n namespace get po | grep node_name | awk '{print $1;}' | xargs -o -t -I{} kubectl -n namespace exec -it {} bash
```
替换上面命令中的namespace、node_name

### `Kubernetes`的三种外部访问方式：`NodePort`、`LoadBalancer`和`Ingress`

参考[http://dockone.io/article/4884](http://dockone.io/article/4884)
