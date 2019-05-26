# Monocular

[https://github.com/helm/monocular](https://github.com/helm/monocular)

The backend is a small Go REST API service, chartsvc, and background CronJobs to run the chart-repo sync command.


```bash
helm repo add monocular https://helm.github.io/monocular
helm install monocular/monocular --name my-monocular
```

```
NOTES:
The Monocular chart sets up an Ingress to serve the API and UI on the same
domain. You can get the address to access Monocular from this Ingress endpoint:

  $ kubectl --namespace default get ingress my-monocular-monocular

Point your Ingress hosts to the address from the output of the above command:
  - null

Visit https://github.com/helm/monocular for more information.
```

```
➜  Helm git:(master) ✗ kubectl --namespace default get ingress
NAME                     HOSTS   ADDRESS   PORTS   AGE
my-monocular-monocular   *                 80      62s
```

访问: [https://localhost/](https://localhost/) 进入 Monocular 界面
