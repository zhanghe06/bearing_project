# KubeDB

[https://github.com/kubedb](https://github.com/kubedb)

[https://github.com/kubedb/installer/tree/0.12.0/chart/kubedb](https://github.com/kubedb/installer/tree/0.12.0/chart/kubedb)

Install KubeDB via Helm 
```
$ helm repo add appscode https://charts.appscode.com/stable/
$ helm repo update
$ helm search appscode/kubedb
NAME                   	CHART VERSION	APP VERSION 	DESCRIPTION
appscode/kubedb        	0.12.0 	0.12.0	KubeDB by AppsCode - Production ready databases on Kubern...
appscode/kubedb-catalog	0.12.0 	0.12.0	KubeDB Catalog by AppsCode - Catalog for database versions

# Step 1: Install kubedb operator chart
$ helm install appscode/kubedb --name kubedb-operator --version 0.12.0 \
  --namespace kube-system

# Step 2: wait until crds are registered
$ kubectl get crds -l app=kubedb -w
NAME                               AGE
dormantdatabases.kubedb.com        6s
elasticsearches.kubedb.com         12s
elasticsearchversions.kubedb.com   8s
etcds.kubedb.com                   8s
etcdversions.kubedb.com            8s
memcacheds.kubedb.com              6s
memcachedversions.kubedb.com       6s
mongodbs.kubedb.com                7s
mongodbversions.kubedb.com         6s
mysqls.kubedb.com                  7s
mysqlversions.kubedb.com           7s
postgreses.kubedb.com              8s
postgresversions.kubedb.com        7s
redises.kubedb.com                 6s
redisversions.kubedb.com           6s
snapshots.kubedb.com               6s

# Step 3(a): Install KubeDB catalog of database versions
$ helm install appscode/kubedb-catalog --name kubedb-catalog --version 0.12.0 \
  --namespace kube-system

# Step 3(b): Or, if previously installed, upgrade KubeDB catalog of database versions
$ helm upgrade kubedb-catalog appscode/kubedb-catalog --version 0.12.0 \
  --namespace kube-system
```


```
NAME:   kubedb-operator
LAST DEPLOYED: Tue Jun 11 09:56:48 2019
NAMESPACE: kube-system
STATUS: DEPLOYED

RESOURCES:
==> v1/ClusterRole
NAME             AGE
kubedb-operator  9s

==> v1/ClusterRoleBinding
NAME                                      AGE
kubedb-operator                           9s
kubedb-operator-apiserver-auth-delegator  9s

==> v1/Deployment
NAME             READY  UP-TO-DATE  AVAILABLE  AGE
kubedb-operator  0/1    1           0          9s

==> v1/Pod(related)
NAME                              READY  STATUS             RESTARTS  AGE
kubedb-operator-588fff969f-c665w  0/1    ContainerCreating  0         9s

==> v1/RoleBinding
NAME                                                              AGE
kubedb-operator-apiserver-extension-server-authentication-reader  9s

==> v1/Secret
NAME                            TYPE    DATA  AGE
kubedb-operator-apiserver-cert  Opaque  2     9s

==> v1/Service
NAME             TYPE       CLUSTER-IP     EXTERNAL-IP  PORT(S)  AGE
kubedb-operator  ClusterIP  10.108.12.143  <none>       443/TCP  9s

==> v1/ServiceAccount
NAME             SECRETS  AGE
kubedb-operator  1        9s

==> v1beta1/APIService
NAME                            AGE
v1alpha1.mutators.kubedb.com    1s
v1alpha1.validators.kubedb.com  5s

==> v1beta1/PodSecurityPolicy
NAME             PRIV  CAPS                   SELINUX   RUNASUSER  FSGROUP   SUPGROUP  READONLYROOTFS  VOLUMES
kubedb-operator  true  IPC_LOCK,SYS_RESOURCE  RunAsAny  RunAsAny   RunAsAny  RunAsAny  false           *


NOTES:
To verify that KubeDB has started, run:

  kubectl --namespace=kube-system get deployments -l "release=kubedb-operator, app=kubedb"

Now install/upgrade appscode/kubedb-catalog chart.

To install, run:

  helm install appscode/kubedb-catalog --name kubedb-catalog --version 0.12.0 --namespace kube-system

To upgrade, run:

  helm upgrade kubedb-catalog appscode/kubedb-catalog --version 0.12.0 --namespace kube-system
```

Install KubeDB CLI
```
# Linux amd 64-bit
wget -O kubedb https://github.com/kubedb/cli/releases/download/0.12.0/kubedb-linux-amd64 \
  && chmod +x kubedb \
  && sudo mv kubedb /usr/local/bin/

# Mac 64-bit
wget -O kubedb https://github.com/kubedb/cli/releases/download/0.12.0/kubedb-darwin-amd64 \
  && chmod +x kubedb \
  && sudo mv kubedb /usr/local/bin/
```
