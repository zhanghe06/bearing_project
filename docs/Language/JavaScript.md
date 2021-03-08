# JavaScript

- ECMAScript
- BOM（Browser Object Model）是指浏览器对象模型，它使 JavaScript 有能力与浏览器进行“对话”。
- DOM（Document Object Model）是指文档对象模型，通过它，可以访问HTML文档的所有元素。

## BOM


1、window对象
一些常用的Window方法：

window.innerHeight - 浏览器窗口的内部高度
window.innerWidth - 浏览器窗口的内部宽度
window.open() - 打开新窗口
window.close() - 关闭当前窗口

2、window的子对象

navigator对象
```
navigator.appName　　// Web浏览器全称
navigator.appVersion　　// Web浏览器厂商和版本的详细字符串
navigator.userAgent　　// 客户端绝大部分信息
navigator.platform　　　// 浏览器运行所在的操作系统
```

screen对象
```
screen.availWidth - 可用的屏幕宽度
screen.availHeight - 可用的屏幕高度　
```

history对象
```
history.forward()  // 前进一页
history.back()  // 后退一页
```

location对象
```
location.href  获取URL
location.href="URL" // 跳转到指定页面
location.reload() 重新加载页面
```

弹出框
```
alert("你看到了吗？");  // 警告框
confirm("你确定吗？")  // 确认框
prompt("请在下方输入","你的答案")  // 提示框
```

延时
```
// 在指定时间之后执行一次相应函数
var timer = setTimeout(function(){alert(123);}, 3000)
// 取消setTimeout设置
clearTimeout(timer);
```

周期
```
// 每隔一段时间就执行一次相应函数
var timer = setInterval(function(){console.log(123);}, 3000)
// 取消setInterval设置
clearInterval(timer);　
```

## DOM

一些常用的 HTML DOM 方法：

getElementById(id) - 获取带有指定 id 的节点（元素）
appendChild(node) - 插入新的子节点（元素）
removeChild(node) - 删除子节点（元素）
一些常用的 HTML DOM 属性：

innerHTML - 节点（元素）的文本值
parentNode - 节点（元素）的父节点
childNodes - 节点（元素）的子节点
attributes - 节点（元素）的属性节点

事件
```
onclick        当用户点击某个对象时调用的事件句柄。
ondblclick     当用户双击某个对象时调用的事件句柄。
 
onfocus        元素获得焦点。               // 练习：输入框
onblur         元素失去焦点。               应用场景：用于表单验证,用户离开某个输入框时,代表已经输入完了,我们可以对它进行验证.
onchange       域的内容被改变。             应用场景：通常用于表单元素,当元素内容被改变时触发.（select联动）
 
onkeydown      某个键盘按键被按下。          应用场景: 当用户在最后一个输入框按下回车按键时,表单提交.
onkeypress     某个键盘按键被按下并松开。
onkeyup        某个键盘按键被松开。
onload         一张页面或一幅图像完成加载。
onmousedown    鼠标按钮被按下。
onmousemove    鼠标被移动。
onmouseout     鼠标从某元素移开。
onmouseover    鼠标移到某元素之上。
 
onselect      在文本框中的文本被选中时发生。
onsubmit      确认按钮被点击，使用的对象是form。
```

## JavaScript Array 对象

Array 对象方法

方法 | 描述
--- | ---
concat()	|   连接两个或更多的数组，并返回结果。
join()	    |   把数组的所有元素放入一个字符串。元素通过指定的分隔符进行分隔。
pop()	    |   删除并返回数组的最后一个元素
push()	    |   向数组的末尾添加一个或更多元素，并返回新的长度。
reverse()	|   颠倒数组中元素的顺序。
shift()	    |   删除并返回数组的第一个元素
slice()	    |   从某个已有的数组返回选定的元素
sort()	    |   对数组的元素进行排序
splice()	|   删除元素，并向数组添加新元素。
toSource()	|   返回该对象的源代码。
toString()	|   把数组转换为字符串，并返回结果。
toLocaleString()	|   把数组转换为本地数组，并返回结果。
unshift()	|   向数组的开头添加一个或更多元素，并返回新的长度。
valueOf()	|   返回数组对象的原始值

包含
```
['1', '2'].includes('1')
```

删除

方式一： 在Array原型对象上添加删除方法
```
// 查找指定的元素在数组中的位置
Array.prototype.indexOf = function(val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) {
            return i;
        }
    }
    return -1;
 };
// 通过索引删除数组元素
Array.prototype.remove = function(val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};
// demo使用
var arr = [1, 2, 3, 5, 6, 'abc', 'ert'];
arr.remove('abc');
/************** 打印输出 arr ***************/
    [1, 2, 3, 5, 6, "ert"]
/************** 打印输出  ***************/
```

方式二： ES6的简介写法
```
var arr = [
    {
        id: 1,
        name: 'Janche'
    },
    {
        id: 2,
        name: '老王'
    }
]
arr.splice(arr.findIndex(e => e.id === 1), 1) // 将删除id等于1的选项
/************** 打印输出 arr ***************/
{
    id: 2,
    name: '老王'
}
/************** 打印输出  ***************/
```

### array转map
```
arrayToMap (array, k, v) {
  const map = new Map()
  for (let item of array) {
    map.set(item[k], item[v])
  }
  return map
}
```

### Array 中的高阶函数 map, filter, reduce

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

```
// 列表分组
const data = [
    { source: 'test1', target: 'test7', value: 20 },
    { source: 'test5', target: 'test3', value: 50 },
    { source: 'test1', target: 'test4', value: 90 },
    { source: 'test6', target: 'test3', value: 10 }
]
const obj = {}
data.reduce((grouping, current) => {
  current['source'] in grouping ? grouping[current['source']].push(current) : grouping[current['source']] = [current]
  return grouping;
}, obj)
```

## JavaScript String 对象

方法 | 描述
--- | ---
anchor() | 创建 HTML 锚。
big() | 用大号字体显示字符串。
blink() | 显示闪动字符串。
bold() | 使用粗体显示字符串。
charAt() | 返回在指定位置的字符。
charCodeAt() | 返回在指定的位置的字符的 Unicode 编码。
concat() | 连接字符串。
fixed() | 以打字机文本显示字符串。
fontcolor() | 使用指定的颜色来显示字符串。
fontsize() | 使用指定的尺寸来显示字符串。
fromCharCode() | 从字符编码创建一个字符串。
indexOf() | 检索字符串。
italics() | 使用斜体显示字符串。
lastIndexOf() | 从后向前搜索字符串。
link() | 将字符串显示为链接。
localeCompare() | 用本地特定的顺序来比较两个字符串。
match() | 找到一个或多个正则表达式的匹配。
replace() | 替换与正则表达式匹配的子串。
search() | 检索与正则表达式相匹配的值。
slice() | 提取字符串的片断，并在新的字符串中返回被提取的部分。
small() | 使用小字号来显示字符串。
split() | 把字符串分割为字符串数组。
strike() | 使用删除线来显示字符串。
sub() | 把字符串显示为下标。
substr() | 从起始索引号提取字符串中指定数目的字符。
substring() | 提取字符串中两个指定的索引号之间的字符。
sup() | 把字符串显示为上标。
toLocaleLowerCase() | 把字符串转换为小写。
toLocaleUpperCase() | 把字符串转换为大写。
toLowerCase() | 把字符串转换为小写。
toUpperCase() | 把字符串转换为大写。
toSource() | 代表对象的源代码。
toString() | 返回字符串。
valueOf() | 返回某个字符串对象的原始值。


## 对象操作

动态创建对象：
Object.assign({a: 1, b: 2})
注意 Object.assign 与 Object.create 区别

给对象添加属性：
obj.属性=属性值;
obj={属性:属性值};
但是对于变量：
obj\[key\]=value;

检查属性是否存在：
const obj = {'a': 1}
'a' in obj // true
'toString' in obj // true
obj.hasOwnProperty('a') // true
obj.hasOwnProperty('b') // false
obj.hasOwnProperty('toString') // false


## JSON

​JSON.parse 将json字符串反序列化为json对象
```
// 定义一个字符串
var data='{"name":"tom"}'
// 解析对象​
​JSON.parse(data)
// 结果
{name: "tom"}

typeof(JSON.parse(data))
"object"
JSON.parse(data)["name"]
"tom"
JSON.parse(data).name
"tom"
```

JSON.stringify 将json对象序列化为json字符串
```
var data={name: 'tom'}
JSON.stringify(data)
'{"name":"tom"}'
```
