import requests
import random

# URL for your local FastAPI server
url = "http://127.0.0.1:8091/retrieve"

# 测试用例1：正常返回 ans 变量并打印输出
test_code1 = """
import math
ans = math.pi * 2
print("Result:", ans)  # 输出结果
"""

# 测试用例2：只有计算，没有打印输出
test_code2 = """
import math
ans = math.pi * 2  # 计算结果，但不打印
"""

# 测试用例3：产生错误
test_code3 = """
ans = 1 / 0  # 除以零错误
"""

# 测试用例4：死循环
test_code4 = """
while True:
    pass  # 无限循环，不会有输出
"""

# time out bad case  



# Example payload
payload = {
    "queries": [test_code1, test_code2, test_code3, test_code4],
    "topk": 5,
    "return_scores": False
}

# Send POST request
response = requests.post(url, json=payload)

# Raise an exception if the request failed
response.raise_for_status()

# Get the JSON response
retrieved_data = response.json()

print("Response from server:")
print(retrieved_data)



