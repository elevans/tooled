import sys
import time
from typing import List

def obj_info(obj):
    """
    Print out a readable list from dir of a desired object. Also returns
    the type of object.
    """
    # TODO: Add more python dianostic options (i.e. object size in memory etc...)
    print(f"Object: {obj}\nType: {type(obj)}\nSize: {sys.getsizeof(obj)} bytes")
    obj_dir = dir(obj)
    # slice obj dir list into 3s
    col_a = obj_dir[::3]
    col_b = obj_dir[1::3]
    col_c = obj_dir[2::3]

    # get max col size and padd out other columns
    max_size = max(len(col_a), len(col_b), len(col_c))
    if len(col_a) < max_size:
        col_a = _pad_list(col_a, max_size)
    if len(col_b) < max_size:
        col_b = _pad_list(col_b, max_size)
    if len(col_c) < max_size:
        col_c = _pad_list(col_c, max_size)

    print("Functions:")
    for at1, at2, at3 in zip(col_a, col_b, col_c):
        print("{:<30}{:<30}{:<}".format(at1, at2, at3))

def timed_function(f, *args, **kwargs):
    """
    Time a method/function by applying the @timed_function decorator to
    the desired method.
    """
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        delta = time.time() - start
        print('Function {} Time = {:6.3f}ms'.format(myname, delta*1000))
        return result

    return new_func


def _pad_list(l: List[str], size: int):
    while len(l) < size:
        l.append("")

    return l