# Flask-Cors

跨域测试

[https://yq.aliyun.com/articles/688172](https://yq.aliyun.com/articles/688172)
```
var token= "Bearer eyJhbGciOiJIUzUxMiIsImV4cCI6MTU4Nzk5NTcyOCwiaWF0IjoxNTg3OTk0NTI4fQ.eyJ0b2tlbl9pZCI6MX0.3Tb1lsGKdEAHepuIxeSCJ9ZOyO3pMIbL6sfRbxHv8Vt0C2_syBEF9BsCA7MzqUfRIqubFKX3IIYaxO8MuxNuxg";
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://127.0.0.1:8000/task?page=1&size=20');
xhr.setRequestHeader("Authorization",token);
xhr.send(null);
xhr.onload = function(e) {
    var xhr = e.target;
    console.log(xhr.responseText);
}
```
