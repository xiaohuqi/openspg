# from cachetools import TTLCache
#
#
# class LinkCache:
#
#     def __init__(self):
# # 创建一个TTLCache对象，设置缓存的最大容量为100，过期时间为60秒
# cache = TTLCache(maxsize=500, ttl=60)
#
# # 写入缓存
# cache['key1'] = 'value1'
# cache['key2'] = 'value2'
#
# # 查询缓存
# print(cache['key1'])  # 输出: value1
# print(cache['key2'])  # 输出: value2
# print(cache.get('key3'))  # 输出: None，因为key3未被写入缓存
