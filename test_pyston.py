from pyston import PystonClient, File
import asyncio


async def main():
    client = PystonClient(base_url="http://172.17.0.1:2000/api/v2")
    output = await client.execute("python", [File("print('Hello world')")])
    print(output)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())