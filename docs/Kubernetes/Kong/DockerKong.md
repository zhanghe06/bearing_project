# Docker Kong

The Cloud-Native API Gateway

[https://github.com/kong/kong](https://github.com/kong/kong)


```bash
helm install stable/kong --name my-kong --set ingressController.enabled=true
```

```
NAME:   my-kong
LAST DEPLOYED: Tue Apr 23 18:38:31 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Job
NAME                          COMPLETIONS  DURATION  AGE
my-kong-kong-init-migrations  0/1          0s        0s

==> v1/Pod(related)
NAME                                      READY  STATUS    RESTARTS  AGE
my-kong-kong-57f7957f6c-qqq45             0/1    Init:0/1  0         0s
my-kong-kong-controller-7cf6bc6b94-7jn9l  0/2    Init:0/1  0         0s
my-kong-kong-init-migrations-rdpk8        0/1    Pending   0         0s
my-kong-postgresql-0                      0/1    Init:0/1  0         0s

==> v1/Secret
NAME                TYPE    DATA  AGE
my-kong-postgresql  Opaque  1     9s

==> v1/Service
NAME                         TYPE       CLUSTER-IP      EXTERNAL-IP  PORT(S)                     AGE
my-kong-kong-admin           NodePort   10.97.195.10    <none>       8444:30847/TCP              1s
my-kong-kong-proxy           NodePort   10.106.15.30    <none>       80:31016/TCP,443:31778/TCP  1s
my-kong-postgresql           ClusterIP  10.100.208.197  <none>       5432/TCP                    1s
my-kong-postgresql-headless  ClusterIP  None            <none>       5432/TCP                    1s

==> v1/ServiceAccount
NAME          SECRETS  AGE
my-kong-kong  1        9s

==> v1beta1/ClusterRole
NAME          AGE
my-kong-kong  1s

==> v1beta1/ClusterRoleBinding
NAME          AGE
my-kong-kong  1s

==> v1beta1/CustomResourceDefinition
NAME                                      AGE
kongconsumers.configuration.konghq.com    5s
kongcredentials.configuration.konghq.com  1s
kongingresses.configuration.konghq.com    1s
kongplugins.configuration.konghq.com      1s

==> v1beta1/Role
NAME          AGE
my-kong-kong  1s

==> v1beta1/RoleBinding
NAME          AGE
my-kong-kong  1s

==> v1beta2/Deployment
NAME                     READY  UP-TO-DATE  AVAILABLE  AGE
my-kong-kong             0/1    1           0          0s
my-kong-kong-controller  0/1    1           0          1s

==> v1beta2/StatefulSet
NAME                READY  AGE
my-kong-postgresql  0/1    0s


NOTES:
1. Kong Admin can be accessed inside the cluster using:
     DNS=my-kong-kong-admin.default.svc.cluster.local
     PORT=8444

To connect from outside the K8s cluster:
     HOST=$(kubectl get nodes --namespace default -o jsonpath='{.items[0].status.addresses[0].address}')
     PORT=$(kubectl get svc --namespace default my-kong-kong-admin -o jsonpath='{.spec.ports[0].nodePort}')


2. Kong Proxy can be accessed inside the cluster using:
     DNS=my-kong-kong-proxy.default.svc.cluster.localPORT=443To connect from outside the K8s cluster:
     HOST=$(kubectl get nodes --namespace default -o jsonpath='{.items[0].status.addresses[0].address}')
     PORT=$(kubectl get svc --namespace default my-kong-kong-proxy -o jsonpath='{.spec.ports[0].nodePort}')
```
