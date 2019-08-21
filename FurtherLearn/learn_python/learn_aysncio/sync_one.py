import time


def hello():
    time.sleep(1)


def run():
    for i in range(5):
        hello()


if __name__ == '__main__':
    start_time = time.time()
    run()
    print(time.time() - start_time) # 5.01750087738
