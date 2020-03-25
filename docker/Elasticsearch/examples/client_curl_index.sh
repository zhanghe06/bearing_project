#!/usr/bin/env bash

# https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
# https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html#query-dsl-term-query

#ES_HOSTNAME="elasticsearch"
ES_HOSTNAME='127.0.0.1'
ES_PORT=9200
ES_USERNAME='elastic'
ES_PASSWORD='changeme'

ES_INDEX="robot-"$(date "+%Y%m%d")
ES_TYPE='_doc'

# 查看索引配置
# curl -u elastic:changeme -X GET "localhost:9200/robot-20200319?pretty"
# 删除全部索引
# curl -u elastic:changeme -X DELETE "localhost:9200/robot-20200319?pretty"

# 新建索引
# curl -u elastic:changeme -X POST "localhost:9200/robot-20200319/_doc?pretty" -H 'Content-Type: application/json' -d'
curl -u ${ES_USERNAME}:${ES_PASSWORD} -X POST "${ES_HOSTNAME}:${ES_PORT}/${ES_INDEX}/${ES_TYPE}?pretty" -H 'Content-Type: application/json' -d'
{
  "host_name": "container_01",
  "line_name": "line_03",
  "q_name": "g.icall.q.appkey",
  "q_name_delay": "g.icall.delayq.appkey",
  "qty": 50,
  "qty_delay": 20,
  "time": "2020-03-20 03:05:00"
}
'
