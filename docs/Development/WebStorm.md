# WebStorm

修改缩进为2个空格
```
WebStorm -> Preferences... -> Editor -> Code Style -> Other File Types -> Tab size: 2; Indent: 2
```

关闭脚本结尾分号提醒
```
WebStorm -> Preferences... -> Editor -> Code Style -> JavaScript -> Punctuation -> Don't use semicolon to terminate statements
```

识别@路径别名

```
npm i @vue/cli-service -S
```

```
WebStorm -> Preferences... -> Languages & Frameworks -> JavaScript -> Webpack -> 选择node_modules/@vue/cli-service/webpack.config.js即可
```

取消起始位置缩进（支持eslint）
```
WebStorm -> Preferences... -> Editer -> Code Style -> HTML -> Other Do not indent children of: -> 点开，换行，添加script
```
