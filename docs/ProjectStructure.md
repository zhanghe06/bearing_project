## Project Structure

```
➜  bearing_project git:(master) ✗ tree -L 2 -I '*.pyc|bearing.env|app_frontend|app_weixingh|download|logs'
.
├── LICENSE
├── README.md
├── app_backend
│   ├── README.md
│   ├── __init__.py
│   ├── api
│   ├── clients
│   ├── filters.py
│   ├── forms
│   ├── login.py
│   ├── messages.pot
│   ├── models
│   ├── permissions.py
│   ├── signals
│   ├── static
│   ├── tasks
│   ├── templates
│   ├── tests
│   ├── tools
│   ├── translations
│   ├── validators
│   └── views
├── app_common
│   ├── __init__.py
│   ├── codes
│   ├── libs
│   ├── maps
│   └── tools
├── babel.cfg
├── babel_compile.sh
├── babel_init.sh
├── babel_update.sh
├── config
│   ├── __init__.py
│   ├── default.py
│   └── develop.py
├── db
│   ├── backup
│   ├── data
│   └── schema
├── docker
│   ├── Beats
│   ├── Elasticsearch
│   ├── Grafana
│   ├── InfluxDB
│   ├── Kibana
│   ├── Kubernetes
│   ├── Logstash
│   ├── MariaDB
│   ├── Nginx
│   ├── Prometheus
│   └── Redis
├── docs
│   ├── Bilingual.md
│   ├── Compatibility.md
│   ├── Docker.md
│   ├── Elasticsearch.md
│   ├── Git.md
│   ├── OperatingSystem
│   ├── OperationManual.md
│   ├── ProjectStructure.md
│   ├── README.md
│   └── SUMMARY.md
├── env_default.sh
├── env_develop.sh
├── etc
│   ├── app_backend.ini
│   └── supervisord.conf
├── gen.py
├── requirements.txt
├── run_backend.py
├── run_frontend.py
└── tests
    ├── __init__.py
    └── test_compatibility.py

40 directories, 35 files
```
