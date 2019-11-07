# Package Manager

- Dpkg
Debian Package Manager

- RPM
Redhat Linux Packet Manager

- PIP
Python Package Installer

参考: [https://www.linuxprobe.com/aptyum-dnfpkg-diff.html](https://www.linuxprobe.com/aptyum-dnfpkg-diff.html)


## 包管理系统

操作系统	| 格式 | 工具
--- | --- | ---
Debian | .deb | apt, apt-cache, apt-get, dpkg
Ubuntu | .deb | apt, apt-cache, apt-get, dpkg
CentOS | .rpm | yum
Fedora | .rpm | dnf
FreeBSD | Ports, .txz | make, pkg


## 更新包列表

系统 | 命令
--- | ---
Debian / Ubuntu	| sudo apt-get update
- | sudo apt update
CentOS | yum check-update
Fedora | dnf check-update
FreeBSD Packages | sudo pkg update
FreeBSD Ports | sudo portsnap fetch update


## 更新已安装的包

系统 | 命令 | 说明
--- | --- | ---
Debian / Ubuntu | sudo apt-get upgrade | 只更新已安装的包
- | sudo apt-get dist-upgrade | 可能会增加或删除包以满足新的依赖项
- | sudo apt upgrade | 和 apt-get upgrade 类似
- | sudo apt full-upgrade | 和 apt-get dist-upgrade 类似
CentOS | sudo yum update | -	
Fedora | sudo dnf upgrade | -
FreeBSD Packages | sudo pkg upgrade | -
FreeBSD Ports | less /usr/ports/UPDATING | 使用 less 来查看 ports 的更新提示（使用上下光标键滚动，按 q 退出）。
- | cd /usr/ports/ports-mgmt/portmaster && sudo make install && sudo portmaster -a | 安装 portmaster 然后使用它更新已安装的 ports


## 搜索某个包

