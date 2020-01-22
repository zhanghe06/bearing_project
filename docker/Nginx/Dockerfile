FROM nginx:1.13.0

# logrotate安装会附带crontab，并生成/etc/cron.daily/logrotate，但是cron服务并未启动
# service cron status
# [FAIL] cron is not running ... failed!

# 安装logrotate，并清理缓存（182MB >> 166MB）
RUN apt-get update && apt-get -y install logrotate; apt-get autoclean; rm -rf /var/lib/apt/lists/*

COPY logrotate.d/nginx /etc/logrotate.d/

# Start nginx and cron as a service
CMD service cron start && nginx -g 'daemon off;'
