# MariaDB

```bash
helm install stable/mariadb --name my-mariadb
```

```
NOTES:

Please be patient while the chart is being deployed

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace default -l release=my-mariadb

Services:

  echo Master: my-mariadb.default.svc.cluster.local:3306
  echo Slave:  my-mariadb-slave.default.svc.cluster.local:3306

Administrator credentials:

  Username: root
  Password : $(kubectl get secret --namespace default my-mariadb -o jsonpath="{.data.mariadb-root-password}" | base64 --decode)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run my-mariadb-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mariadb:10.1.38 --namespace default --command -- bash

  2. To connect to master service (read/write):

      mysql -h my-mariadb.default.svc.cluster.local -uroot -p my_database

  3. To connect to slave service (read-only):

      mysql -h my-mariadb-slave.default.svc.cluster.local -uroot -p my_database

To upgrade this helm chart:

  1. Obtain the password as described on the 'Administrator credentials' section and set the 'rootUser.password' parameter as shown below:

      ROOT_PASSWORD=$(kubectl get secret --namespace default my-mariadb -o jsonpath="{.data.mariadb-root-password}" | base64 --decode)
      helm upgrade my-mariadb stable/mariadb --set rootUser.password=$ROOT_PASSWORD
```

开启外部访问
```bash
kubectl port-forward --namespace default svc/my-mariadb 3366:3306 &
```
