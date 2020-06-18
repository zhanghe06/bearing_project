# Vue

```
npm install cnpm -g
cnpm install vue
cnpm install webpack -g
```

## [Element](https://element.eleme.cn/#/zh-CN)

第一步：安装项目模板
```
npm install -g webpack
npm install -g vue-cli
vue init webpack element_project

cd element_project      //进入项目目录
npm install             //安装项目依赖（新建项目省略此步）
npm run dev             //运行项目
```

访问：[http://localhost:8080](http://localhost:8080)

第二步：安装主题框架
```
cd element_project
npm i element-ui -S
npm i vuex -S
```
第三步：打包
```
npm run build
```

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

### 模板循环

循环 - 列表
```
<p v-for="(item, i) in list" :key="item.id">索引: {{i}}, 值: {{item.name}}</p>
```

循环 - 对象
```
<p v-for="(val, key, i) in list">索引: {{i}}, 键: {{key}}, 值: {{val}}</p>
```

循环 - 数字
```
<p v-for="count in 5">第{{count}}次</p>
```
以上数字从1开始

### 脚本循环
```
for(let item of response.data.result) {
    // 用item操作每一条数据。
}
```
注意：这里是 of 不是 in，of和in是有区别的

```
response.data.result.forEach((item, index) => {
    // 用item操作每一条数据。
})
```


总结：

`for in` 总是得到对像的key、数组或字符串的下标

`for of` 和`forEach`一样, 是直接得到值, 但是`for of`不能用于对象


列表操作
```
this.list.push({})
this.list.unshift({})
```

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

## 生命周期

```
mounted() {
  // 定时刷新
  if (this.timer) {
    clearInterval(this.timer)
  } else {
    this.timer = setInterval(() => {
      this.getMigrateDetail()
    }, 1000)
  }
}
```

```
destroyed() {
  // 清除定时
  clearInterval(this.timer)
}
```

循环执行（setInterval）
```
export default {
  data() {
    return {
      timer: '',
      value: 0
    }
  },
  methods: {
    get() {
      this.value ++
      console.log(this.value)
    }
  },
  mounted() {
    this.timer = setInterval(this.get, 1000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  }
}
```
以上循环多次执行

定时执行（setTimeout）
```
export default {
  data() {
    return {
      timer: '',
      value: 0
    }
  },
  methods: {
    get() {
      this.value ++;
      console.log(this.value)
    }
  },
  mounted() {
    this.timer = setTimeout(this.get, 1000)
  },
  beforeDestroy() {
    clearTimeout(this.timer)
  }
}
```
以上仅仅执行一次


## 使用element-ui的分页组件刷新后保留在当前页

```
<div class="pagination">
  <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :page-sizes="[10, 20, 50, 100]"
    :page-size="pageSize"
    :current-page.sync="currentPage"
    layout="total, sizes, prev, pager, next" background
    :total="count">
  </el-pagination>
</div>
```

```
//每页大小变化
handleSizeChange(val) {
  this.$router.replace({
    path: this.$route.path,
    query: {
      page: this.$route.query.page ? this.$route.query.page : 1,
      pageSize: val,
    }
  });
  this.getData();
},
//分页页码变化
handleCurrentChange(val) {
  this.$router.replace({
    path: this.$route.path,
    query: {
      page: val,
      pageSize: this.$route.query.pageSize ? this.$route.query.pageSize : 10,
    }
  });
  this.getData();
},
//获取数据
getData(){
  axios.post({
    page: this.$route.query.page ? this.$route.query.page : 1,
    pageSize: this.$route.query.pageSize ? this.$route.query.pageSize : 10,
  }).then((res) => {
    console.log(res)
  }).catch((err) => {
    console.error('获取列表出错');
    console.error(err);
  });
},
```


## props
```
demo: {
  type: Array,
  default: function () {
    return []
  }
}

demo: {
  type: Array,
  default: function () {
    return {}
  }
}

demoArray: {
  type: Array,
  default: () => []
}

demoObject: {
  type: Object,
  default: () => ({})
}
```

## 参考

[https://github.com/lin-xin/vue-manage-system](https://github.com/lin-xin/vue-manage-system)

## 文件上传

CHROME 异常`net::ERR_UPLOAD_FILE_CHANGED`

复现步骤：
```
1、点击上传（上传失败、表单未重置）
2、修改文件，再次上传
```

## array转map
```
arrayToMap (array, k, v) {
  const map = new Map()
  for (let item of array) {
    map.set(item[k], item[v])
  }
  return map
}
```

## Array 中的高阶函数 map, filter, reduce

```
var array1 = [1,4,9,16];
const map1 = array1.map(x => x *2);
console.log(array1);  // [1,4,9,16]
console.log(map1);  // [2,8,18,32]
```

```
var arr = [20,30,50,96,50]
var newArr = arr.filter(item => item>40) 
console.log(arr)  // [20,30,50, 96,50]
console.log(newArr)  // [50, 96, 50]
```

```
// 高频用途：去掉数组中的 空字符串、0、undefined、null；
var arr = ['1', '2', null, '3.jpg', null, 0]
var newArr = arr.filter(item => item)
// 也可以写成
// var newArr = arr.filter(Boolean);
console.log(newArr) // ["1", "2", "3.jpg"]
```

```
// 统计字符串中每个字符出现的次数
const str = '9kFZTQLbUWOjurz9IKRdeg28rYxULHWDUrIHxCY6tnHleoJ'
const obj = {}
Array.from(str).reduce((accumulator, current) => {
  current in accumulator ? accumulator[current]++ : accumulator[current] = 1
  return accumulator;
}, obj)
```
