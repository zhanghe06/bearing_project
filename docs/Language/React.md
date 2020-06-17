# React

[https://react.docschina.org](https://react.docschina.org)

- 声明式
- 组件化

## node版本

升级Node LTS版本 [https://nodejs.org/en/](https://nodejs.org/en/)

否则通过create-react-app创建项目会报错
```
error @typescript-eslint/eslint-plugin@2.24.0: The engine "node" is incompatible with this module. Expected version "^8.10.0 || ^10.13.0 || >=11.10.1".
```

## yarn版本

如果遇到因yarn版本报错
```
error fork-ts-checker-webpack-plugin@3.1.1: The engine "yarn" is incompatible with this module. Expected version ">=1.0.0".
```
安装或升级yarn
```
npm install -g npm
npm install -g yarn
```

## 创建项目

```
npm install -g create-react-app
create-react-app react_project
cd react_project
npm start
```

访问：[http://localhost:3000](http://localhost:3000)
