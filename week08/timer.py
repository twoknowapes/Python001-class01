import time
from functools import wraps


def timer(func):
    @wraps(func)
    def time_this_func(*args, **kwargs):
        print('timer of decorator...')

        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(f'@timer: {func.__name__} took {end_time - start_time: .5f} s')
        return res

    return time_this_func


@timer
def time_test_func(n):
    while n > 0:
        time.sleep(0.1)
        n -= 1


time_test_func(100)
