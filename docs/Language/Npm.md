# Npm

安装Node，自动安装Npm (Node.js 的包管理工具)

下载 [node-v14.15.4](https://nodejs.org/dist/v14.15.4/node-v14.15.4.pkg) 并安装
```
This package will install:
	•	Node.js v14.15.4 to /usr/local/bin/node
	•	npm v6.14.10 to /usr/local/bin/npm
Make sure that /usr/local/bin is in your $PATH.
```

Mac环境查找根目录
```
npm root -g
```

WIndows在`C:\Users(your username)\AppData\Roaming`


排错

TypeError: cb.apply is not a function
```
# /usr/local/lib/node_modules/gitbook-cli/node_modules/npm/node_modules/graceful-fs/polyfills.js
# 注释以下3行
 62 //  fs.stat = statFix(fs.stat)
 63 //  fs.fstat = statFix(fs.fstat)
 64 //  fs.lstat = statFix(fs.lstat)
```

npm WARN checkPermissions Missing write access to /usr/local/lib/node_modules
```
sudo chown -R $USER /usr/local/lib/node_modules
```
