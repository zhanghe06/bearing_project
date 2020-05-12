# NIPAP

[https://nipap.readthedocs.io/en/latest](https://nipap.readthedocs.io/en/latest)

[https://hub.docker.com/r/nipap/nipapd](https://hub.docker.com/r/nipap/nipapd)
```
docker pull nipap/nipapd:v0.29.6
docker run -i -t --link nipap-db --name nipapd nipapd
```

```
#   LISTEN_ADDRESS      address on which nipapd should listen [0.0.0.0]
#   LISTEN_PORT         port on which nipapd should listen [1337]
#   SYSLOG              true / false enable syslog? [false]
#   DB_HOST             host where database is running
#   DB_PORT             port of database [5432]
#   DB_NAME             name of database
#   DB_USERNAME         username to authenticate to database
#   DB_PASSWORD         password to authenticate to database
#   DB_SSLMODE          require ssl? [disable]
#   NIPAP_USERNAME      name of account to create
#   NIPAP_PASSWORD      password of account to create
```

```
docker pull nipap/nipap-www:v0.29.6
docker run -i -t --link nipapd --name nipap-www nipap-www
```

```
#   NIPAPD_USERNAME     username to authenticate to nipapd
#   NIPAPD_PASSWORD     password to authenticate to nipapd
#   NIPAPD_HOST         host where nipapd is running [nipapd]
#   NIPAPD_PORT         port of nipapd [1337]
#   WWW_USERNAME        web UI username [guest]
#   WWW_PASSWORD        web UI password [guest]
```
