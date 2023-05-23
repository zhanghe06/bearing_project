# Flask-Excel

中文乱码

Django:
```
import codecs
response.content = codecs.BOM_UTF8 + response.content
```
可在中间件统一处理

Flask:
```
import codecs
response.data = codecs.BOM_UTF8 + response.data
```

## 使用案例

模型导出
```
column_names = Answer.__table__.columns.keys()
query_sets = get_answer_rows(*search_condition)

return excel.make_response_from_query_sets(
    query_sets=query_sets,
    column_names=column_names,
    file_type='csv',
    file_name='download.csv'
)
```

列表导出
```
@app.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")
```

记录导出
```
records = [
    {'name': 'lucy', 'age': 20},
    {'name': 'lily', 'age': 22},
]
return excel.make_response_from_records(
    records=records,
    file_type='csv',
    file_name='download.csv'
)
```

自定义排序
```
# 定义排序
def custom_sort_hot(item):
    return item['hit'] >=100


# 执行排序
res_list = sorted(res_list, key=custom_sort_hot, reverse=True)
res_list = sorted(res_list, key=lambda item: item['hit'] >=100, reverse=True)
```
