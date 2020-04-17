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
