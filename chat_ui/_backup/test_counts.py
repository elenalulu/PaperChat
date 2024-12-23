
from collections import Counter
 
# 假设我们有以下列表，列表中包含字典，字典有一个键'field'
data = [
    {'field': 'value1', 'other_key': 'other_value1'},
    {'field': 'value2', 'other_key': 'other_value2'},
    {'field': 'value1', 'other_key': 'other_value3'},
    {'field': 'value3', 'other_key': 'other_value4'},
    {'field': 'value2', 'other_key': 'other_value5'},
]
 
# 使用Counter对field的值进行计数
counts = Counter([item['field'] for item in data])
 
print(counts)
most_title = counts.most_common(1)
most_title = most_title[0]
most_title = str(most_title).split("',")
most_title = most_title[0]
most_title = most_title.replace("('",'')
print (most_title)