from pyston import PystonClient, File
import asyncio


# special cases 
# order of execution 
# benchmark it time and bad cases 
async def main():
    client = PystonClient(base_url="http://172.17.0.1:2000/api/v2/")
    codes = ["print('Hello world')"] * 1000
    outputs = await asyncio.gather(*[asyncio.create_task(client.execute("python", [File(code)])) for code in codes])
    print(len(outputs))
    for output in outputs:
        print("output: ", output)

# async def main():
#     client = PystonClient(base_url="http://172.17.0.1:2000/api/v2/")
#     codes = ["print('Hello world')"] * 1000
#     count = 0
#     outputs = []
#     for code in codes:
#         output = await client.execute("python", [File(code)])
#         if "fork: retry" in str(output):
#             print("output: ", output)
#             count += 1
#         outputs.append(output)
#     print(count)
#     print(len(outputs))


if __name__ == "__main__":
    asyncio.run(main())
