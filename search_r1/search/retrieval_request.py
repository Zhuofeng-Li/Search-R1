import requests

# URL for your local FastAPI server
url = "http://127.0.0.1:8093/retrieve"

# 测试用例1：正常返回 ans 变量
test_code1 = """
import math
ans = math.pi * 2
"""

# 测试用例2：只有打印输出，没有 ans 变量
test_code2 = """
print("Hello, World!")
print("This is a test")
"""

# 测试用例3：既有 ans 又有打印输出（应该返回 ans）
test_code3 = """
print("This will be ignored")
ans = 42
print("This will also be ignored")
"""

# 测试用例4：什么都没有
test_code4 = """
x = 1 + 1  # just calculation
"""

# 测试用例5：产生错误
test_code5 = """
ans = 1/0  # Division by zero error
"""

# 测试用例6：复杂计算
test_code6 = """
import math
x = [1, 2, 3, 4, 5]
ans = sum(x) * math.pi
print(ans)
"""


# Example payload
payload = {
    "queries": [test_code1],
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
