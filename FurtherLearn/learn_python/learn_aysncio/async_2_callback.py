import asyncio
import time


async def hello(x):
    print("say hello")
    return "say {}".format(x)


def callback(future):
    print("callback", future.result())  # 回调里获取返回值


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    start_time = time.time()
    coroutine = hello(2)
    task = asyncio.ensure_future(coroutine)
    print(task)
    task.add_done_callback(callback)  # 绑定回调
    print(task)
    loop.run_until_complete(task)
    print(time.time() - start_time)
