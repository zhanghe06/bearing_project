# BlueKing

急速体验

- PAAS
```
docker run -d --name="bk-paas" -p 8000-8003:8000-8003 ccr.ccs.tencentyun.com/bk.io/paas-standalone:latest
```

- CMDB
```
docker run -d --name="bk-cmdb" -p 8090:8090 ccr.ccs.tencentyun.com/bk.io/cmdb-standalone:latest
```

[http://127.0.0.1:8090](http://127.0.0.1:8090)

## PaaS

[https://github.com/Tencent/bk-PaaS](https://github.com/Tencent/bk-PaaS)

```
brew cask install docker
docker pull ccr.ccs.tencentyun.com/bk.io/paas-standalone:latest
docker run -d --name="bk-paas" -p 8000-8003:8000-8003 ccr.ccs.tencentyun.com/bk.io/paas-standalone:latest
```

appengine 8000
paas 8001
esb 8002
login 8003

/etc/hosts
```
127.0.0.1 www.bking.com
```

pass [http://www.bking.com:8001](http://www.bking.com:8001)

初次访问，跳转登录 [http://www.bking.com:8003](http://www.bking.com:8003)

admin/admin


## CMDB - MacOS K8S环境部署

[https://github.com/Tencent/bk-cmdb](https://github.com/Tencent/bk-cmdb)

[https://github.com/Tencent/bk-cmdb/blob/master/helm/README.md](https://github.com/Tencent/bk-cmdb/blob/master/helm/README.md)

需要更新helm到v3版本
```bash
brew upgrade helm
```

准备镜像
```bash
docker pull hoffermei/bk-cmdb:v3.6.3
docker images | grep bk-cmdb
docker tag hoffermei/bk-cmdb:v3.6.3 bk-cmdb:v3.6.3
```
说明：
bk-cmdb镜像使用的是`bk-cmdb:v3.6.3`，拉取之后需要重新打标签，否则报错镜像不存在，`kubectl get pods`显示错误`ImagePullBackOff`
查看详细日志`kubectl describe pod bk-cmdb-bk-cmdb-coreservice-766f9d65c5-npr5f`，显示错误`Failed to pull image "bk-cmdb:v3.6.3": rpc error: code = Unknown desc = Error response from daemon: pull access denied for bk-cmdb, repository does not exist or may require 'docker login': denied: requested access to the resource is denied`

```bash
git clone https://github.com/Tencent/bk-cmdb.git
cd bk-cmdb
git co -b v3.6.x origin/v3.6.x
cd helm/bk-cmdb
helm install bk-cmdb ./
kubectl get pods -o wide | 
kubectl get svc
```

查看bk-cmdb-webserver pod详情
```
➜  ~ kubectl get pods -o wide | grep -E "bk-cmdb-bk-cmdb-webserver|NAME"
NAME                                               READY   STATUS      RESTARTS   AGE    IP          NODE             NOMINATED NODE   READINESS GATES
bk-cmdb-bk-cmdb-webserver-976dc47fd-h5rnj          1/1     Running     4          154m   10.1.0.59   docker-desktop   <none>           <none>
```

查看bk-cmdb-webserver svc详情
```
➜  ~ kubectl get svc | grep -E "bk-cmdb-bk-cmdb-webserver|NAME"
NAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
bk-cmdb-bk-cmdb-webserver         NodePort    10.110.180.187   <none>        80:32033/TCP                 178m
```

登录pod对应的容器，访问对应服务
```
➜  ~ kubectl exec bk-cmdb-bk-cmdb-webserver-976dc47fd-h5rnj -it -- /bin/bash
[root@bk-cmdb-bk-cmdb-webserver-976dc47fd-h5rnj cmdb_webserver]# curl 10.1.0.59
<!DOCTYPE html><html><head><meta charset=utf-8><title>配置平台 | 蓝鲸智云企业版</title><link rel="shortcut icon" href=/static/favicon.ico type=image/x-icon><link href=/static/css/app.cbd7c02f44089f1f9cea9c87eb8d10ed.css rel=stylesheet></head><body><div id=app></div><script type=text/javascript>window.Site = {
            url: "http://bk-cmdb.blueking.domain/",
            version: "v3",
            login: "%!(EXTRA string=cc, string=http://bk-cmdb.blueking.domain/)",
            agent: "http://127.0.0.1:8088/console/?app=bk_agent_setup",
            authscheme: "internal" || 'internal',
            authCenter: {"appCode":"","url":""},
            buildVersion: 'v3.6.3',
            fullTextSearch: "off" || 'off',
        }
        window.User = {
            admin: "1",
            name: "admin"
        }
        window.Supplier = {
            account: '0'
        }
        window.API_HOST = Site.buildVersion.indexOf('dev') !== -1 ? Site.url : (window.location.origin + '/')
        window.API_PREFIX = API_HOST + 'api/' + Site.version</script><script type=text/javascript src=/static/js/manifest.4917acb03eb8d559da63.js></script><script type=text/javascript src=/static/js/vendor.999eb6929642d212565d.js></script><script type=text/javascript src=/static/js/app.7951fa56bd2dfb6d4b84.js></script></body></html>
[root@bk-cmdb-bk-cmdb-webserver-976dc47fd-h5rnj cmdb_webserver]#
```

```
curl http://localhost:32033
```

访问[http://localhost:32033](http://localhost:32033)
