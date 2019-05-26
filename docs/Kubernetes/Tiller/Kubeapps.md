# Kubeapps

https://github.com/kubeapps/kubeapps

https://github.com/kubeapps/kubeapps/blob/master/docs/user/getting-started.md

## Step 1: Install Kubeapps
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install --name kubeapps --namespace kubeapps bitnami/kubeapps
```

Tiller Proxy: [https://github.com/kubeapps/kubeapps/tree/master/cmd/tiller-proxy](https://github.com/kubeapps/kubeapps/tree/master/cmd/tiller-proxy)

```
NOTES:
** Please be patient while the chart is being deployed **

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace kubeapps

Kubeapps can be accessed via port 80 on the following DNS name from within your cluster:

   kubeapps.kubeapps.svc.cluster.local

To access Kubeapps from outside your K8s cluster, follow the steps below:

1. Get the Kubeapps URL by running these commands:
   echo "Kubeapps URL: http://127.0.0.1:8080"
   export POD_NAME=$(kubectl get pods --namespace kubeapps -l "app=kubeapps" -o jsonpath="{.items[0].metadata.name}")
   kubectl port-forward --namespace kubeapps $POD_NAME 8080:8080

2. Open a browser and access Kubeapps using the obtained URL.
```

## Step 2: Create a Kubernetes API token
```bash
kubectl create serviceaccount kubeapps-operator
kubectl create clusterrolebinding kubeapps-operator --clusterrole=cluster-admin --serviceaccount=default:kubeapps-operator
```

```
➜  ~ kubectl create serviceaccount kubeapps-operator
serviceaccount/kubeapps-operator created
➜  ~ kubectl get serviceaccount
NAME                     SECRETS   AGE
default                  1         96d
kubeapps-operator        1         3s
my-nginx-nginx-ingress   1         4d22h
my-rabbitmq
➜  ~ kubectl create clusterrolebinding kubeapps-operator --clusterrole=cluster-admin --serviceaccount=default:kubeapps-operator
clusterrolebinding.rbac.authorization.k8s.io/kubeapps-operator created
```

retrieve the token
```bash
kubectl get secret $(kubectl get serviceaccount kubeapps-operator -o jsonpath='{.secrets[].name}') -o jsonpath='{.data.token}' | base64 --decode
```


## Step 3: Start the Kubeapps Dashboard
```bash
export POD_NAME=$(kubectl get pods -n kubeapps -l "app=kubeapps,release=kubeapps" -o jsonpath="{.items[0].metadata.name}")
echo "Visit http://127.0.0.1:8080 in your browser to access the Kubeapps Dashboard"
kubectl port-forward -n kubeapps ${POD_NAME} 8080:8080
```

[http://127.0.0.1:8080](http://127.0.0.1:8080)

type the token


## Step 4: Deploy WordPress


## Using a Private Repository with Kubeapps

[https://github.com/kubeapps/kubeapps/blob/master/docs/user/private-app-repository.md](https://github.com/kubeapps/kubeapps/blob/master/docs/user/private-app-repository.md)

Configure the repository in Kubeapps
```
Configuration > App Repositories
Name: <release_name>
URL: http://<release_name>-chartmuseum.<namespace>:8080
```

例如：
```
Name: my-chartmuseum
URL: http://my-chartmuseum-chartmuseum.default:8080
```
