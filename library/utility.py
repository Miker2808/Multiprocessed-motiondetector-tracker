import numpy as np
import timeit

def non_sys_sleep(sleep_time):
    start_time = timeit.default_timer()
    counter_time = timeit.default_timer()
    while True:
        counter_time = timeit.default_timer()
        delta_time = counter_time - start_time
        if delta_time >= sleep_time:
            break


def cv_to_cartesian(cv_point, resolution = (1240,720)):
    cartesian_x = cv_point[0] - resolution[0]/2
    cartesian_y = resolution[1]/2 - cv_point[1]
    return int(cartesian_x), int(cartesian_y)
