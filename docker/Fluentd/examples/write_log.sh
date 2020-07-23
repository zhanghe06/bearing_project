#!/usr/bin/env bash

# sh examples/write_log.sh

echo '2020-03-20T00:30:02.579794994Z [@basic.go.116][INF] recv body {"business": {"calls": [{"caller": "+9501359900088", "callee": "+639270322975", "type": "normal", "robotid": "122", "robot_name": "M0_Level3_PH_Jill", "prvdata": "{\"id\": 971816, \"taskid\": \"a28c3b6a7e4565befdaf49bf95c4527d\", \"sip_line\": \"TANGNIU_Line\"}", "template": {"due_dayofmonth": "Today", "due_days": "0", "dueday_remain": "TODAY", "borrower_name": "Cabonce_Sharon_Elevazo", "greetings": "Morning", "due_date": "0320", "platform": "PESOQ", "borrow_money": "3000", "borrow_date": "0314", "gender": "UNKNOWN"}, "callback": "aHR0cDovL25ldy1pbnRlcm5hbC1jYWxsaW5nLmFpcnVkZGVyLmNvbS9hcGkvY2FsbGJhY2s="}]}, "system": {"appkey": "119819371379", "charset": "UTF-8", "timestamp": 1584664202, "signtype": "MD5", "sign": "13whWlNxcACbZ_NezCugCg", "version": "1.0.0"}} 90b5816d93ca4621bd8d96afaaa1bb3a' >> log_tail/tail.log
echo '2020-03-20T00:30:05.271910258Z [@CrossMonkey.go.407][INF] post icall status notify http://172.31.16.51:8909/api/v1/call/90b5816d93ca4621bd8d96afaaa1bb3a/status {"time":"2020-03-20T00:30:05.271516581+07:00","status":"Ringing","maddress":"210.4.101.11:19066"} => {"callid":"90b5816d93ca4621bd8d96afaaa1bb3a","code":0,"msg":"OK"}' >> log_tail/tail.log
echo '2020-03-20T00:30:17.286950706Z [@CrossMonkey.go.407][INF] post icall status notify http://172.31.16.51:8909/api/v1/call/7734ad30c29b48a4a4a805f2916917df/status {"time":"2020-03-20T00:30:17.286465462+07:00","status":"Established","maddress":"210.4.101.11:19826"} => {"callid":"7734ad30c29b48a4a4a805f2916917df","code":0,"msg":"OK"}' >> log_tail/tail.log
echo '2020-03-20T00:30:32.583800387Z [@CrossMonkey.go.407][INF] post icall status notify http://172.31.16.51:8909/api/v1/call/90b5816d93ca4621bd8d96afaaa1bb3a/status {"time":"2020-03-20T00:30:32.583349015+07:00","status":"Closed"} => {"callid":"90b5816d93ca4621bd8d96afaaa1bb3a","code":0,"msg":"OK"}' >> log_tail/tail.log
echo '2020-03-20T00:30:32.593045912Z [@CallbackMonkey.go.261][INF] callback http://new-internal-calling.airudder.com/api/callback post {"business":{"billsec":0,"callee":"+639270322975","caller":"+9501359900088","callid":"90b5816d93ca4621bd8d96afaaa1bb3a","calltime":1584664202,"prvdata":"{\"id\": 971816, \"taskid\": \"a28c3b6a7e4565befdaf49bf95c4527d\", \"sip_line\": \"TANGNIU_Line\"}","reasoncode":180,"ringtime":1584664205,"talkbegtime":0,"talkendtime":0,"token":"90b5816d93ca4621bd8d96afaaa1bb3a"},"system":{"appkey":"119819371379","charset":"UTF-8","sign":"Qtj-ffNfDN7vvVkEpz3-Gg","signtype":"MD5","timestamp":1584664232,"version":"1.0.0"}} => {"system": {"appkey": "119819371379", "charset": "UTF-8", "signtype": "MD5", "timestamp": 1584664232, "errmessage": "success", "errcode": 0, "sign": "2L5MZSfI5DzjVzzyRlMASg"}}' >> log_tail/tail.log


#echo "" >> log/tail.log
#echo "" >> log/tail.log
#echo "" >> log/tail.log
#echo "" >> log/tail.log
#echo "" >> log/tail.log
