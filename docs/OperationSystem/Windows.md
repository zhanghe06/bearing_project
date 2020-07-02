# Windows

## 查看端口

```
netstat -ano | findstr "8000"
```


## Vmware 快照

注意，快照需要虚机关机或挂起状态，才能使用克隆。否则只能给自己使用

## Vmware Tools
Vmware Tool 安装，对虚机系统有要求

系统补丁

OS | VER
--- | ---
Windows | Windows Server 2016
Windows | Windows 10
Windows | Windows Server 2012 R2 with Microsoft update KB2919355
Windows | Windows 8.1 with Microsoft update KB2919355
Windows | Windows Server 2012
Windows | Windows 8
Windows | [Windows Server 2008 R2 Service Pack 1 (SP1)](https://www.microsoft.com/zh-CN/download/details.aspx?id=5842)
Windows | [Windows 7 SP1](https://www.microsoft.com/zh-CN/download/details.aspx?id=5842)
Windows | Windows Server 2008 Service Pack 2 (SP2)
Windows | Windows Vista SP2

更新补丁需要先更新系统

[Update for Universal C Runtime in Windows](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows)

如果 "安装 Vmware Tool" 按钮灰色，需要关闭虚机，勾选连接 CD/DVD，并选自动检测

关闭防火墙
控制面板 - 高级安全Windows防火墙

Windows Server 2012 禁用IE增强安全
管理工具 - 服务器管理 - 本地服务器 - IE增强的安全配置（禁用）

python 安装

[python-2.7.17.amd64.msi](https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi)

注意安装过程，添加PATH



默认已经安装 pip
更换源
%APPDATA%\pip\pip.ini
```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```

修复 windows 环境下报错 UnicodeDecodeError

给 C:\Python27 加写权限

C:\Python27\Lib\mimetypes.py
```
if sys.getdefaultencoding() != 'gbk': 
 reload(sys) 
 sys.setdefaultencoding('gbk')
```


[https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)

mysqlclient
下载 mysqlclient‑1.4.5‑cp27‑cp27m‑win_amd64.whl
虚拟环境下安装
pip install mysqlclient‑1.4.5‑cp27‑cp27m‑win_amd64.whl

[https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Visual C++

下载 [VCForPython27.msi](https://aka.ms/vcpython27)

挪到C盘，管理员权限启动cmd，命令安装（双击会提示系统策略禁止）
msiexec.exe /i "C:\VCForPython27.msi"

下载 [Visual C++ Tools](https://aka.ms/vs/16/release/RemoteTools.amd64ret.chs.exe)


```
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
```

pip install -r requirements.txt

git 安装

virtualenv 安装


SET PROJ_HOME=%USERPROFILE%/proj/111
SET PROJECT_BASEDIR=%PROJ_HOME%/exercises/ex1
mkdir "%PROJ_HOME%"

## 打包

```
pip install pyinstaller
pip install pywin32
pyinstaller -n lims -D run_apps.py  # 进入项目入口文件夹
修改 lims.spec，删除build dist
pyinstaller lims.spec

会生成 dist, build 目录
```

## NPM

## Host切换
1、hosts文件赋予修改权限
2、switchhost工具修改hosts


## 排错

python3安装库时关于 ImportError: cannot import name 'Feature' from 'setuptools'报错解决

```
pip install --upgrade pip setuptools==45.2.0
```

## Windows系统目录环境变量

环境变量 | 说明 | 路径
--- | --- | ---
%systemdrive% | Windows系统所在磁盘分区 | 通常就是C盘的根目录
%systemroot%,%windir% | Windows系统所在的目录 | 通常是C:\Winows
%programfiles% | 应用程序所在的目录 | 通常情况下是C:\program files
%commonprogramfiles% | 公用文件目录 | 通常是C:\program files\common files
%userprofile% | 当前账户的用户目录 | 通常是C:\documents and settings\当前用户名
%alluserprofile% | 所有用户的用户目录 | 通常是C:\documents and settings\all user
%temp%,%tmp% | 当前用户的临时文件目录 | 通常是C:\documents and settings\当前用户名\local settings\temp


## .Net Framework

错误一、.Net Framework 安装失败 提示一般信任关系失败

1. 进入系统后按下`Win + R`快捷键打开运行，输入`gpedit.msc`并点击确定打开组策略
2. 在本地组策略编辑器依次展开到`计算机配置--管理模板--Windows 组件--Windows Installer`，在右侧窗口找到并双击打开`允许用户对安装进行控制`策略
3. 将其设置为`已启动`，点击确定，如已经是`已启动`，可先设置为`未配置`，确定退出后，再重新设置为`已启动`
4. 重启

错误二、已处理证书链，但是在不受信任提供程序信任的根证书中终止

1. 点击链接下载微软证书：[MicrosoftRootCertificateAuthority2011.cer](http://download.microsoft.com/download/2/4/8/248D8A62-FCCD-475C-85E7-6ED59520FC0F/MicrosoftRootCertificateAuthority2011.cer)
2. 按 Windows徽标键+R 打开运行，输入MMC
3. 打开控制台，文件→添加/删除管理单元 (Ctrl+M)
4. 选择证书 → 添加 → 计算机账户（其他的保持默认，一直下一步）
5. 回到控制台主窗口，依次展开：证书 → 受信任的根证书颁发机构 → 证书，单击更多操作的小箭头，选择所有任务 → 导入；接下来选择步骤1中下载好的cer证书文件，然后一直点击下一步，导入成功即可。
6. 此时重新安装 .Net Framework 则不会提示问题了。


## .NET Core SDK

[https://dotnet.microsoft.com/download](https://dotnet.microsoft.com/download)

## Visual Studio

[https://go.microsoft.com/fwlink/?LinkId=615448&clcid=0x409](https://go.microsoft.com/fwlink/?LinkId=615448&clcid=0x409)

## VS Code

打开终端（Terminal -> New Terminal），进入项目，编译
```
dotnet build
```

目前Visual Studio Code里官方C#插件只支持.NET Core编译调试。暂不支持Mono和传统.NET Framework
