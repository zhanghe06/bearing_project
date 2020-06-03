# Vue

```
npm install cnpm -g
cnpm install vue
cnpm install webpack -g
```

## [Element](https://element.eleme.cn/#/zh-CN)

第一步：安装项目模板
npm install -g webpack
npm install -g vue-cli
vue init webpack element_project

cd element_project      //进入项目目录
npm install             //安装项目依赖（新建项目省略此步）
npm run dev             //运行项目

[http://localhost:8080](http://localhost:8080)

第二步：安装主题框架
cd element_project
npm i element-ui -S
npm i vuex -S

第三步：打包
npm run build


颜色
- primary
- success
- warning
- danger
- info

## 插值表达式

插值表达式`{{  }}`默认已文本形式显示

## 指令

指令 | 解释 | 缩写
--- | --- | ---
v-once | 渲染一次 | -
v-html | HTML | -
v-bind | HTML属性 | :<属性名称>
v-model | 表单双向绑定 | -
v-on | 事件 | @<事件名称>
v-if | 条件 | -
v-for | 循环 | -

## 事件处理器

事件修饰符

按键修饰符

## 组件（Vue的核心）

- 父组件，包含子组件
- 子组件，被父组件引用

方式 | 数据流 | 说明
--- | --- | ---
props | 父组件 -> 子组件 | 不应该在一个子组件内部改变 prop
$emit | 子组件 -> 父组件 | v-on:input="$emit('input', $event.target.value)"; 或者定义在子组件的方法内


$emit，仅kebab-case命名
$event

$refs dom节点、组件节点
$store 子组件可通过this.$store访问

## 插槽

插槽显不显示、怎样显示是由父组件来控制的，而插槽在哪里显示就由子组件来进行控制

## 学习路径

1. VUE基础
2. 组件化
3. 工程化
4. Element（页面布局，导航，表格，表单...）


## 语法

日期格式化
`yyyy-MM-dd HH:mm:SS`

## Router


## Axios

```
npm i axios -S
```

main.js
```ecmascript 6
import Vue from 'vue'

import axios from 'axios'

Vue.prototype.$http = axios
```

发送示例
```ecmascript 6
const fromData = {
  age: this.ruleForm.age,
  pass: this.ruleForm.pass
}
// 发送数据
this.$http.post('/api.json', fromData)
  .then(res => {
    // 数据发送成功回调
    console.log("数据发送成功")
    console.log(res.data)
  })
  .catch((error) => {
    // 数据发送失败回调
    console.log(error)
  })
```

请求示例 - 不含参数
```ecmascript 6
this.$http.get('/api.json')
  .then(res => {
    // 数据请求成功回调
    console.log(res.data)
  })
  .catch((error) => {
    // 数据请求失败回调
    console.log(error)
  })
```

请求示例 - 含有参数
```ecmascript 6
let params = {
  name: 12345
}
this.$http.get('/api.json', {params})
  .then(res => {
    // 数据请求成功回调
    console.log(res.data)
  })
  .catch((error) => {
    // 数据请求失败回调
    console.log(error)
  })
```
注意 params 外层需要花括号再包一层
