#!/usr/bin/env bash

# 安装插件
docker exec elasticsearch \
    sh -c "elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.6.0/elasticsearch-analysis-ik-7.6.0.zip"

docker restart elasticsearch

## 配置热词
#docker exec -it elasticsearch sh -c 'cat << EOF > config/analysis-ik/IKAnalyzer.cfg.xml
#<?xml version="1.0" encoding="UTF-8"?>
#<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
#<properties>
#	<comment>IK Analyzer Settings</comment>
#	<entry key="ext_dict"></entry>
#	<entry key="ext_stopwords"></entry>
#	<entry key="remote_ext_dict">http://192.168.4.1:8160/static/ik/extra_word.dic</entry>
#	<entry key="remote_ext_stopwords">http://192.168.4.1:8160/static/ik/stop_word.dic</entry>
#</properties>
#EOF'
#
#docker restart elasticsearch
#
## 检查热词
#docker exec -it elasticsearch sh -c 'curl -I http://192.168.4.1:8160/static/ik/extra_word.dic'
#docker exec -it elasticsearch sh -c 'curl -I http://192.168.4.1:8160/static/ik/stop_word.dic'
#
## 校验配置
#docker exec -it elasticsearch sh -c 'cat config/analysis-ik/IKAnalyzer.cfg.xml'

# 远程字典配置失败，貌似需要修改 es 服务器 配置
