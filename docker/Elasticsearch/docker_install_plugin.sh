#!/usr/bin/env bash

docker exec elasticsearch \
    sh -c "elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.2.3/elasticsearch-analysis-ik-6.2.3.zip"

docker restart elasticsearch
