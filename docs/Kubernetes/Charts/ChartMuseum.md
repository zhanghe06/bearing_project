# ChartMuseum

[https://github.com/helm/chartmuseum](https://github.com/helm/chartmuseum)

Chart 仓库

```bash
helm install stable/chartmuseum --name my-repo
```

```
NOTES:
** Please be patient while the chart is being deployed **

Get the ChartMuseum URL by running:

  export POD_NAME=$(kubectl get pods --namespace default -l "app=chartmuseum" -l "release=my-repo" -o jsonpath="{.items[0].metadata.name}")
  echo http://127.0.0.1:8080/
  kubectl port-forward $POD_NAME 8080:8080 --namespace default
```


```bash
POD_NAME=$(kubectl get pods --namespace default -l "app=chartmuseum" -l "release=my-repo" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward ${POD_NAME} 8080:8080 --namespace default
```

访问: [http://127.0.0.1:8080](http://127.0.0.1:8080)

```bash
helm repo add chartmuseum http://localhost:8080
helm repo list
```

[http://127.0.0.1:8080/health](http://127.0.0.1:8080/health)

[http://127.0.0.1:8080/api/charts](http://127.0.0.1:8080/api/charts)
