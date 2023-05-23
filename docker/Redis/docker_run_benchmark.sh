#!/usr/bin/env bash

# 性能测试
docker exec -it redis redis-benchmark -h localhost -p 6379 -c 50 -n 10000
