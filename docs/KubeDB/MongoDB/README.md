# MongoDB

[https://kubedb.com/docs/0.12.0/guides/mongodb/quickstart/quickstart](https://kubedb.com/docs/0.12.0/guides/mongodb/quickstart/quickstart)

[https://github.com/kubedb/cli/tree/0.12.0/docs/examples/mongodb](https://github.com/kubedb/cli/tree/0.12.0/docs/examples/mongodb)


```
✗ kubectl get storageclasses
NAME                 PROVISIONER          AGE
hostpath (default)   docker.io/hostpath   142d
✗ kubectl get ns
NAME              STATUS   AGE
default           Active   58m
docker            Active   57m
kube-node-lease   Active   58m
kube-public       Active   58m
kube-system       Active   58m
✗ kubectl create ns demo
namespace/demo created
```


Find Available MongoDBVersion
```
✗ kubectl get mongodbversions
NAME       VERSION   DB_IMAGE                DEPRECATED   AGE
3.4        3.4       kubedb/mongo:3.4        true         1d
3.4-v1     3.4       kubedb/mongo:3.4-v1     true         1d
3.4-v2     3.4       kubedb/mongo:3.4-v2     true         1d
3.4-v3     3.4       kubedb/mongo:3.4-v3                  1d
3.6        3.6       kubedb/mongo:3.6        true         1d
3.6-v1     3.6       kubedb/mongo:3.6-v1     true         1d
3.6-v2     3.6       kubedb/mongo:3.6-v2     true         1d
3.6-v3     3.6       kubedb/mongo:3.6-v3                  1d
4.0        4.0.5     kubedb/mongo:4.0        true         1d
4.0-v1     4.0.5     kubedb/mongo:4.0-v1                  1d
4.0.5      4.0.5     kubedb/mongo:4.0.5      true         1d
4.0.5-v1   4.0.5     kubedb/mongo:4.0.5-v1                1d
4.1.7      4.1.7     kubedb/mongo:4.1.7      true         1d
4.1.7-v1   4.1.7     kubedb/mongo:4.1.7-v1                1d
```

拉取镜像需要FQ

临时设置代理
```
export http_proxy=http://127.0.0.1:1087
export https_proxy=http://127.0.0.1:1087
```


```
✗ wget https://raw.githubusercontent.com/kubedb/cli/0.12.0/docs/examples/mongodb/quickstart/demo-1.yaml
✗ cp demo-1.yaml demo-mg-create.yaml
✗ sed -i "" "s/standard/hostpath/g" demo-mg-create.yaml
✗ kubedb create -f demo-mg-create.yaml
```


临时取消代理
```
unset http_proxy
unset https_proxy
```


```
✗ kubedb describe mg -n demo mgo-quickstart
Name:               mgo-quickstart
Namespace:          demo
CreationTimestamp:  Thu, 13 Jun 2019 02:39:27 +0800
Labels:             <none>
Annotations:        <none>
Replicas:           1  total
Status:             Running
  StorageType:      Durable
Volume:
  StorageClass:  hostpath
  Capacity:      1Gi
  Access Modes:  RWO

StatefulSet:
  Name:               mgo-quickstart
  CreationTimestamp:  Thu, 13 Jun 2019 02:39:27 +0800
  Labels:               app.kubernetes.io/component=database
                        app.kubernetes.io/instance=mgo-quickstart
                        app.kubernetes.io/managed-by=kubedb.com
                        app.kubernetes.io/name=mongodb
                        app.kubernetes.io/version=3.4-v3
                        kubedb.com/kind=MongoDB
                        kubedb.com/name=mgo-quickstart
  Annotations:        <none>
  Replicas:           824636919240 desired | 1 total
  Pods Status:        1 Running / 0 Waiting / 0 Succeeded / 0 Failed

Service:
  Name:         mgo-quickstart
  Labels:         app.kubernetes.io/component=database
                  app.kubernetes.io/instance=mgo-quickstart
                  app.kubernetes.io/managed-by=kubedb.com
                  app.kubernetes.io/name=mongodb
                  app.kubernetes.io/version=3.4-v3
                  kubedb.com/kind=MongoDB
                  kubedb.com/name=mgo-quickstart
  Annotations:  <none>
  Type:         ClusterIP
  IP:           10.105.143.125
  Port:         db  27017/TCP
  TargetPort:   db/TCP
  Endpoints:    10.1.4.134:27017

Service:
  Name:         mgo-quickstart-gvr
  Labels:         app.kubernetes.io/component=database
                  app.kubernetes.io/instance=mgo-quickstart
                  app.kubernetes.io/managed-by=kubedb.com
                  app.kubernetes.io/name=mongodb
                  app.kubernetes.io/version=3.4-v3
                  kubedb.com/kind=MongoDB
                  kubedb.com/name=mgo-quickstart
  Annotations:    service.alpha.kubernetes.io/tolerate-unready-endpoints=true
  Type:         ClusterIP
  IP:           None
  Port:         db  27017/TCP
  TargetPort:   27017/TCP
  Endpoints:    10.1.4.134:27017

Database Secret:
  Name:         mgo-quickstart-auth
  Labels:         kubedb.com/kind=MongoDB
                  kubedb.com/name=mgo-quickstart
  Annotations:  <none>

Type:  Opaque

Data
====
  password:  16 bytes
  username:  4 bytes

No Snapshots.

Events:
  Type    Reason      Age   From             Message
  ----    ------      ----  ----             -------
  Normal  Successful  3m    KubeDB operator  Successfully created stats service
  Normal  Successful  3m    KubeDB operator  Successfully created Service
  Normal  Successful  2m    KubeDB operator  Successfully created StatefulSet demo/mgo-quickstart
  Normal  Successful  2m    KubeDB operator  Successfully created MongoDB
  Normal  Successful  2m    KubeDB operator  Successfully created appbinding
  Normal  Successful  2m    KubeDB operator  Successfully patched stats service
  Normal  Successful  2m    KubeDB operator  Successfully patched StatefulSet demo/mgo-quickstart
  Normal  Successful  2m    KubeDB operator  Successfully patched MongoDB
```


```
✗ kubectl get po -n demo
NAME               READY   STATUS    RESTARTS   AGE
mgo-quickstart-0   1/1     Running   1          4m58s
✗ kubectl get statefulset -n demo
NAME             READY   AGE
mgo-quickstart   1/1     5m15s
✗ kubectl get pvc -n demo
NAME                       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
datadir-mgo-quickstart-0   Bound    pvc-684e2d4b-8d41-11e9-b190-025000000001   1Gi        RWO            hostpath       5m39s
✗ kubectl get pv -n demo
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                           STORAGECLASS   REASON   AGE
pvc-684e2d4b-8d41-11e9-b190-025000000001   1Gi        RWO            Delete           Bound    demo/datadir-mgo-quickstart-0   hostpath                6m2s
✗ kubectl get service -n demo
NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
mgo-quickstart       ClusterIP   10.105.143.125   <none>        27017/TCP   6m35s
mgo-quickstart-gvr   ClusterIP   None             <none>        27017/TCP   6m35s
```


```
✗ kubedb get mg -n demo mgo-quickstart -o yaml
apiVersion: kubedb.com/v1alpha1
kind: MongoDB
metadata:
  creationTimestamp: "2019-06-12T18:39:27Z"
  finalizers:
  - kubedb.com
  generation: 2
  name: mgo-quickstart
  namespace: demo
  resourceVersion: "5933"
  selfLink: /apis/kubedb.com/v1alpha1/namespaces/demo/mongodbs/mgo-quickstart
  uid: 681c508b-8d41-11e9-b190-025000000001
spec:
  databaseSecret:
    secretName: mgo-quickstart-auth
  podTemplate:
    controller: {}
    metadata: {}
    spec:
      livenessProbe:
        exec:
          command:
          - mongo
          - --eval
          - db.adminCommand('ping')
        failureThreshold: 3
        periodSeconds: 10
        successThreshold: 1
        timeoutSeconds: 5
      readinessProbe:
        exec:
          command:
          - mongo
          - --eval
          - db.adminCommand('ping')
        failureThreshold: 3
        periodSeconds: 10
        successThreshold: 1
        timeoutSeconds: 1
      resources: {}
      securityContext:
        fsGroup: 999
        runAsNonRoot: true
        runAsUser: 999
  replicas: 1
  serviceTemplate:
    metadata: {}
    spec: {}
  storage:
    accessModes:
    - ReadWriteOnce
    dataSource: null
    resources:
      requests:
        storage: 1Gi
    storageClassName: hostpath
  storageType: Durable
  terminationPolicy: DoNotTerminate
  updateStrategy:
    type: RollingUpdate
  version: 3.4-v3
status:
  observedGeneration: 2$4213139756412538772
  phase: Running
```

获取管理员账号密码
```
✗ kubectl get secrets -n demo mgo-quickstart-auth -o jsonpath='{.data.\username}' | base64 -D
root
✗ kubectl get secrets -n demo mgo-quickstart-auth -o jsonpath='{.data.\password}' | base64 -D
Acl4mXoZ6H75NEni
```

测试数据库连接操作
```
✗ kubectl exec -it mgo-quickstart-0 -n demo sh
$ mongo admin
MongoDB shell version v3.4.20
connecting to: mongodb://127.0.0.1:27017/admin
MongoDB server version: 3.4.20
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
2019-06-12T18:51:56.489+0000 I STORAGE  [main] In File::open(), ::open for '/home/mongodb/.mongorc.js' failed with No such file or directory
> db.auth("root","Acl4mXoZ6H75NEni")
1
> show dbs
admin  0.000GB
local  0.000GB
> show users
{
	"_id" : "admin.root",
	"user" : "root",
	"db" : "admin",
	"roles" : [
		{
			"role" : "root",
			"db" : "admin"
		}
	]
}
> use newdb
switched to db newdb
> db.movie.insert({"name":"batman"});
WriteResult({ "nInserted" : 1 })
> db.movie.find().pretty()
{ "_id" : ObjectId("5d014a236f72bab9c081cb75"), "name" : "batman" }
> exit
bye
```


```
✗ kubedb delete mg mgo-quickstart -n demo
✗ kubectl delete drmn mgo-quickstart -n demo
```

Resume
```
✗ kubedb create -f demo-mg-create.yaml
```

Cleaning up
```
✗ kubectl patch -n demo mg/mgo-quickstart -p '{"spec":{"terminationPolicy":"WipeOut"}}' --type="merge"
✗ kubectl delete -n demo mg/mgo-quickstart

✗ kubectl patch -n demo drmn/mgo-quickstart -p '{"spec":{"wipeOut":true}}' --type="merge"
✗ kubectl delete -n demo drmn/mgo-quickstart

✗ kubectl delete ns demo
```
