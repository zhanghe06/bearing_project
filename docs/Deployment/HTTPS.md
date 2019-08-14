# HTTPS

## 本地证书浏览器配置

### Chrome 浏览器

访问页面，会出现提示：该网站的安全证书不受信任！

仍然继续访问, https 标识为 X

三道杠（新版是三点） >> 设置 >> HTTPS/SSL >> 管理证书 >> 证书管理器 >> 授权中心 >> 导入 >> 选择证书 >> 勾选信任该证书，以标识网站的身份。

再次访问，图标变为绿色，心情瞬间变好了。

### IE 浏览器

```
Internet 选项 >> 内容 >> 证书 >> 受信任的根证书颁发机构 >> 导入 >> 下一步 >> 浏览 >> 选择 >> 弹出提示，选是 
```

附加：  
Windows 修改 hosts `C:\Windows\System32\drivers\etc\hosts`


## HSTS

[https://hstspreload.appspot.com/](https://hstspreload.appspot.com/)
