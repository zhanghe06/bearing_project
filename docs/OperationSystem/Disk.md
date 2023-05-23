# Disk

查看文件系统及挂载点
```
zhanghe@ubuntu:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            974M     0  974M   0% /dev
tmpfs           199M   14M  185M   7% /run
/dev/sda1        18G  1.5G   16G   9% /
tmpfs           992M     0  992M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           992M     0  992M   0% /sys/fs/cgroup
tmpfs           199M     0  199M   0% /run/user/1000
```

查看块设备
```
zhanghe@ubuntu:~$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk
sda      8:0    0   20G  0 disk
|-sda1   8:1    0   18G  0 part /
|-sda2   8:2    0    1K  0 part
`-sda5   8:5    0    2G  0 part [SWAP]
sr0     11:0    1 1024M  0 rom
sr1     11:1    1 1024M  0 rom
```

查看磁盘
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
