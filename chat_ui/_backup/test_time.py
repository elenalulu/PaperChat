import time

# 获取当前时间的时间戳
current_timestamp = time.time()
current_timestamp = str(current_timestamp).split('.')[0]

print(current_timestamp)