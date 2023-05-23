# Moment.js

[https://github.com/moment/moment](https://github.com/moment/moment)

[http://momentjs.com](http://momentjs.com)

JS
```
// 当前时间
$('#current_time').html(moment().format('dddd, YYYY-MM-DD, a hh:mm:ss'))
// 剩余时间 - 本地时间
$('#left_time').html(moment('{{ end_time }}', 'YYYY-MM-DD hh:mm:ss').fromNow(true))
// 剩余时间 - UTC时间
$('#left_time').html(moment.utc('{{ end_time }}', 'YYYY-MM-DD hh:mm:ss').fromNow(true));
```

HTML
```
<div id="left_time">-</div>
```

Python
```
end_time = (datetime.utcnow() + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
```
