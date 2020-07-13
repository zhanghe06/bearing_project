# PIP

## CentOS

```
yum install -y python-pip
```

## 离线处理依赖

```
# 导出
pip download -d my_env_pkgs/ -r requirements.txt
# 加载（一定要使用绝对路径，所以有三个/）
pip install -r requirements.txt --no-index -f file:///home/user_name/my_env_pkgs
```

创建本地源
```
# 安装pip2pi模块
pip install pip2pi
# 建立索引（my_env_pkgs目录下会多出一个simple文件夹）
dir2pi ~/my_env_pkgs/
# 进入目标文件夹（就是对外发布的文件夹，因为开启HTTP Server是将当前文件夹发布）
cd ~/my_env_pkgs/simple/
# 开启HTTP Server - Python3
python -m http.server
# 开启HTTP Server - Python2
python -m SimpleHTTPServer
```

[http://127.0.0.1:8000](http://127.0.0.1:8000)

```
pip install -i http://127.0.0.1:8000 -r requirements.txt
```
