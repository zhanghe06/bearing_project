# ChartMuseum

[https://github.com/helm/chartmuseum](https://github.com/helm/chartmuseum)

[chartmuseum api 源码](https://github.com/helm/chartmuseum/blob/master/pkg/chartmuseum/server/multitenant/routes.go)

Chart 仓库

查找
```bash
helm search chartmuseum
helm inspect stable/chartmuseum
helm inspect values stable/chartmuseum
```

安装（推荐方式）
```bash
helm install stable/chartmuseum --name my-chartmuseum --set env.open.DISABLE_API=false --set persistence.enabled=true
```

```
NOTES:
** Please be patient while the chart is being deployed **

Get the ChartMuseum URL by running:

  export POD_NAME=$(kubectl get pods --namespace default -l "app=chartmuseum" -l "release=my-chartmuseum" -o jsonpath="{.items[0].metadata.name}")
  echo http://127.0.0.1:8080/
  kubectl port-forward $POD_NAME 8080:8080 --namespace default
```

[不推荐]安装（下载 chartmuseum cli 工具）
```bash
curl -LO https://s3.amazonaws.com/chartmuseum/release/latest/bin/darwin/amd64/chartmuseum
chartmuseum --version
chartmuseum --help
```

[不推荐]启动
```bash
chartmuseum --debug --port=8180 \
  --storage="local" \
  --storage-local-rootdir="./chartstorage"
```

删除
```bash
helm delete --purge my-chartmuseum
```

```bash
POD_NAME=$(kubectl get pods --namespace default -l "app=chartmuseum" -l "release=my-chartmuseum" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward ${POD_NAME} 8180:8080 --namespace default
```

访问: [http://127.0.0.1:8180](http://127.0.0.1:8180)

```bash
helm repo add chartmuseum http://127.0.0.1:8180
helm repo list
```

[http://127.0.0.1:8180/health](http://127.0.0.1:8180/health)

[http://127.0.0.1:8180/api/charts](http://127.0.0.1:8180/api/charts)


更换仓库端口
```bash
helm repo remove chartmuseum
helm repo add chartmuseum http://127.0.0.1:8180
helm repo list

POD_NAME=$(kubectl get pods --namespace default -l "app=chartmuseum" -l "release=my-chartmuseum" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward ${POD_NAME} 8180:8080 --namespace default
```

测试数据
```bash
git clone https://github.com/helm/chartmuseum.git
cd chartmuseum/testdata/charts/mychart/
helm package .

curl --data-binary "@mychart-0.1.0.tgz" http://127.0.0.1:8180/api/charts
```
