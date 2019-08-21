import asyncio
import time

"""
await: 对耗时的操作进行挂起，loop遇到await会执行别的协程，直到其他的协程也挂起或者执行完毕
https://www.cnblogs.com/zhaof/p/8490045.html
"""

async def hello(x):
    print("say hello")
    print(asyncio.sleep(x))
    return "say {}".format(x)


def callback(future):
    print("callback", future.result())  # 回调里获取返回值


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    start_time = time.time()
    coroutine = hello(2)
    print(coroutine)
    task = asyncio.ensure_future(coroutine)
    print(task)
    task.add_done_callback(callback)  # 绑定回调
    print(task)
    loop.run_until_complete(task)
    print(time.time() - start_time)
