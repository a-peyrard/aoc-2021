from functools import reduce


def compose2(f, g):
    return lambda *args, **kwargs: f(g(*args, **kwargs))


def compose(*fs):
    if fs:
        return reduce(compose2, fs)

    return lambda x: x
