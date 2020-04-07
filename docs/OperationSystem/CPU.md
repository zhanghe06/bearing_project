# CPU

- 用户态
- 内核态

idle CPU 的状态
iowait 任务的状态

iowait 只是 CPU 空闲（idle）时间的一个子集，也就是说 iowait 其实可以归类到 idle 状态，
本质上表示 CPU 是空闲的，只不过 iowait 表示任务中有等待 I/O 操作完成的时间

使用 Linux 中的 dd 命令模拟高密集 I/O 任务
```
sudo dd if=/dev/sda1 of=/dev/null bs=1MB
```

模拟IO/CPU密集场景, 通过 top 查看效果
```
# 正常空闲状态
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

# IO 密集
sudo taskset 1 dd if=/dev/sda1 of=/dev/null bs=1MB
%Cpu(s):  0.3 us, 83.9 sy,  0.0 ni,  0.0 id,  1.0 wa,  0.0 hi, 14.7 si,  0.0 st

# CPU 密集
sudo taskset 1 sh -c "while true; do true; done"
%Cpu(s):100.0 us,  0.0 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
```
