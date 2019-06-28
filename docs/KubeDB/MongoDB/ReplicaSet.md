# ReplicaSet

[https://kubedb.com/docs/0.12.0/guides/mongodb/clustering/replicaset/](https://kubedb.com/docs/0.12.0/guides/mongodb/clustering/replicaset/)


```
kubectl create ns demo
kubedb create -f demo-mg-clustering.yaml
```

```
kubedb describe mg -n demo mgo-replicaset
```


```
✗ kubectl get secrets -n demo mgo-replicaset-auth -o jsonpath='{.data.\username}' | base64 -D
root%
✗ kubectl get secrets -n demo mgo-replicaset-auth -o jsonpath='{.data.\password}' | base64 -D
Acl4mXoZ6H75NEni%
```

primary member
```
✗ kubectl exec -it mgo-replicaset-0 -n demo bash
mongodb@mgo-replicaset-0:/$ mongo admin -u root -p Acl4mXoZ6H75NEni
MongoDB shell version v3.6.12
connecting to: mongodb://127.0.0.1:27017/admin?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("807b11c9-134d-4bf2-bf9d-d1806856f463") }
MongoDB server version: 3.6.12
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
2019-06-20T12:01:54.147+0000 I STORAGE  [main] In File::open(), ::open for '/home/mongodb/.mongorc.js' failed with No such file or directory
rs0:PRIMARY> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
rs0:PRIMARY> show users
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
rs0:PRIMARY> use newdb
switched to db newdb
rs0:PRIMARY> db.movie.insert({"name":"batman"});
WriteResult({ "nInserted" : 1 })
rs0:PRIMARY> db.movie.find().pretty()
{ "_id" : ObjectId("5d0b75c9a5e9aaaa2222e87b"), "name" : "batman" }
rs0:PRIMARY> exit
bye
2019-06-20T12:02:27.731+0000 E -        [main] Error saving history file: FileOpenFailed: Unable to open() file /home/mongodb/.dbshell: No such file or directory
mongodb@mgo-replicaset-0:/$
```

secondary members
```
✗ kubectl exec -it mgo-replicaset-1 -n demo bash
mongodb@mgo-replicaset-1:/$ mongo admin -u root -p Acl4mXoZ6H75NEni
MongoDB shell version v3.6.12
connecting to: mongodb://127.0.0.1:27017/admin?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("2d799a45-9b7c-4bce-a937-8e8c4d92eda3") }
MongoDB server version: 3.6.12
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
2019-06-24T12:17:41.998+0000 I STORAGE  [main] In File::open(), ::open for '/home/mongodb/.mongorc.js' failed with No such file or directory
rs0:SECONDARY> show dbs
2019-06-24T12:17:57.855+0000 E QUERY    [thread1] Error: listDatabases failed:{
	"operationTime" : Timestamp(1561378669, 1),
	"ok" : 0,
	"errmsg" : "not master and slaveOk=false",
	"code" : 13435,
	"codeName" : "NotMasterNoSlaveOk",
	"$clusterTime" : {
		"clusterTime" : Timestamp(1561378669, 1),
		"signature" : {
			"hash" : BinData(0,"mkt9ixireXX0zBGBepSUB+otnH4="),
			"keyId" : NumberLong("6705986404955979777")
		}
	}
} :
_getErrorWithCode@src/mongo/shell/utils.js:25:13
Mongo.prototype.getDBs@src/mongo/shell/mongo.js:67:1
shellHelper.show@src/mongo/shell/utils.js:860:19
shellHelper@src/mongo/shell/utils.js:750:15
@(shellhelp2):1:1
rs0:SECONDARY> rs.slaveOk()
rs0:SECONDARY> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
newdb   0.000GB
rs0:SECONDARY> show users
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
rs0:SECONDARY> use newdb
switched to db newdb
rs0:SECONDARY> db.movie.find().pretty()
{ "_id" : ObjectId("5d107513eca518a5c48f7ab8"), "name" : "batman" }
rs0:SECONDARY> exit
bye
2019-06-24T12:18:47.971+0000 E -        [main] Error saving history file: FileOpenFailed: Unable to open() file /home/mongodb/.dbshell: No such file or directory
mongodb@mgo-replicaset-1:/$
```


Automatic Failover
```
✗ kubectl exec -it mgo-replicaset-1 -n demo bash
mongodb@mgo-replicaset-1:/$ mongo admin -u root -p Acl4mXoZ6H75NEni
MongoDB shell version v3.6.12
connecting to: mongodb://127.0.0.1:27017/admin?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("66ca9595-e68d-438c-86a4-5f215513525c") }
MongoDB server version: 3.6.12
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
2019-06-24T12:24:01.984+0000 I STORAGE  [main] In File::open(), ::open for '/home/mongodb/.mongorc.js' failed with No such file or directory
rs0:SECONDARY> rs.isMaster().primary
mgo-replicaset-2.mgo-replicaset-gvr.demo.svc.cluster.local:27017
rs0:SECONDARY> show dbs
2019-06-24T12:24:57.178+0000 E QUERY    [thread1] Error: listDatabases failed:{
	"operationTime" : Timestamp(1561379093, 1),
	"ok" : 0,
	"errmsg" : "not master and slaveOk=false",
	"code" : 13435,
	"codeName" : "NotMasterNoSlaveOk",
	"$clusterTime" : {
		"clusterTime" : Timestamp(1561379093, 1),
		"signature" : {
			"hash" : BinData(0,"FGUeTu0CTUjlt4dWPbcFG62z7iw="),
			"keyId" : NumberLong("6705986404955979777")
		}
	}
} :
_getErrorWithCode@src/mongo/shell/utils.js:25:13
Mongo.prototype.getDBs@src/mongo/shell/mongo.js:67:1
shellHelper.show@src/mongo/shell/utils.js:860:19
shellHelper@src/mongo/shell/utils.js:750:15
@(shellhelp2):1:1
rs0:SECONDARY> rs.slaveOk()
rs0:SECONDARY> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
newdb   0.000GB
rs0:SECONDARY> show users
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
rs0:SECONDARY> use newdb
switched to db newdb
rs0:SECONDARY> db.movie.find().pretty()
{ "_id" : ObjectId("5d107513eca518a5c48f7ab8"), "name" : "batman" }
rs0:SECONDARY>
```


Cleaning up
```
kubectl patch -n demo mg/mgo-replicaset -p '{"spec":{"terminationPolicy":"WipeOut"}}' --type="merge"
kubectl delete -n demo mg/mgo-replicaset

kubectl patch -n demo drmn/mgo-replicaset -p '{"spec":{"wipeOut":true}}' --type="merge"
kubectl delete -n demo drmn/mgo-replicaset

kubectl delete ns demo
```
