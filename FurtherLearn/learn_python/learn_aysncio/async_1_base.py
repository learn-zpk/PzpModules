import asyncio
import time

"""
 loop.run_until_complete(hello()) # 运行事件循环，直到future运行结束，这里面的hello()会自动变成一个future
 
 
 async声明了一个协程，不能直接运
 获取一个事件循环loop: asyncio.get_event_loop()
 协程加入到事件循环中，并启动协程:loop.run_until_complete(hello())，这里会将协程方法包装成一个task对象，保存协程运行后的状态，用于未来获取协程的结果
 创建一个task: loop.create_task(hello())
"""


async def hello():
    print("say hello")
    asyncio.sleep(1)


def run():
    for i in range(2):
        loop.run_until_complete(hello())


def run2():
    task1 = loop.create_task(hello())  # pending
    print(task1)
    loop.run_until_complete(task1)  # done
    print(task1)


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    start_time = time.time()
    run2()
    print(time.time() - start_time)  # 5.01750087738
