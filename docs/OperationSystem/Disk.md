# Disk

```
# 查看磁盘
sudo fdisk -l | grep Disk
# 挂载磁盘
mount <磁盘> <挂载点>
# 卸载磁盘
umount <挂载点>
```

dd 命令模拟高密集 I/O 任务
```
dd if=/dev/sda of=/dev/null bs=1MB
```

iostat
```
# 需要安装
sudo apt install -y sysstat     # Ubuntu
yum install -y sysstat          # CentOS
```
