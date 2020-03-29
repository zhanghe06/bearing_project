#!/usr/bin/env bash

# Create Docker Volume
VOLUME_NAME="grafana-vol"

# docker volume rm grafana-vol

docker volume ls | grep -wq "${VOLUME_NAME}" && echo "The volume: ${VOLUME_NAME} already exists" ||
  docker volume create "${VOLUME_NAME}" && echo "The volume: ${VOLUME_NAME} has been created"

docker run \
  -h grafana \
  --name grafana \
  --restart always \
  --cpus ".25" \
  --memory "1g" \
  --memory-swap "1g" \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -e TZ=Asia/Shanghai \
  -e GF_SECURITY_ADMIN_USER='admin' \
  -e GF_SECURITY_ADMIN_PASSWORD='123456' \
  -e GF_USERS_ALLOW_SIGN_UP=false \
  -e "GF_SERVER_DOMAIN=192.168.4.1" \
  -e "GF_SMTP_ENABLED=true" \
  -e "GF_SMTP_HOST=smtp.partner.outlook.cn:587" \
  -e "GF_SMTP_USER=data-noreply@xxxxxx.com" \
  -e "GF_SMTP_PASSWORD=xxxxxx" \
  -e "GF_SMTP_SKIP_VERIFY=true" \
  -e "GF_SMTP_FROM_ADDRESS=data-noreply@xxxxxx.com" \
  -e "GF_SMTP_FROM_NAME=AlertingRobot" \
  -v "${VOLUME_NAME}":/var/lib/grafana \
  -p 3000:3000 \
  -d \
  grafana/grafana:6.6.2

# http://0.0.0.0:3000
# 如果密码含有#和; 需要加3个双引号, 例如（"""pass#word"""）
# GF_SERVER_DOMAIN 需要设置, 不然邮件报警, 链接为localhost
