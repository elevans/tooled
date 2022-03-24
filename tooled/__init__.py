import tooled.plot


def obj_info(object):
    """
    Print out a readable list from dir of an object.
    """
    print(f"\nObject: {object}\nType: {type(object)}\n")

    obj_dir = dir(object)
    for at1, at2, at3 in zip(obj_dir[::3], obj_dir[1::3], obj_dir[2::3]):
        print("{:<30}{:<30}{:<}".format(at1, at2, at3))

    return