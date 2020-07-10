# Tencent

[https://cloud.tencent.com](https://cloud.tencent.com)

关闭云盾

为什么要关闭？
```
  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
13946 root      20   0 1009216  69912   4152 S  0.7  3.7 113:10.82 YDService
```
看吧，能不关么

方式一（控制台）
在[主机安全（云镜）-资产管理-主机列表](https://console.cloud.tencent.com/cwp/asset/machine)里找到自己的机器，点击卸载即可。
约1分钟同步状态，实测没有卸载成功，这就有点扯了。

方式二（终端）
```
/usr/local/qcloud/YunJing/uninst.sh
```
