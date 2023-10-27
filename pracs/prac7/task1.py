import dis


def foo(n):
    r = 1
    while n > 1:
        r = n * r
        n -= 1

    return r



print(dis.dis(foo))
