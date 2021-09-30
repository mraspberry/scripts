import time


def proper():
    with open(__file__) as fd:
        return fd.read()


def read_self():
    return open(__file__).read()


def test_read_self():
    read_self()


def test_proper():
    proper()


if __name__ == "__main__":
    test_read_self()
    test_proper()
