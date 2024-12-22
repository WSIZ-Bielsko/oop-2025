from datetime import datetime
from random import randint

ts = lambda: datetime.now().timestamp()

if __name__ == '__main__':
    print('---')
    w = [0] * 100 * 10 ** 6
    print('started')
    st = ts()
    for _ in range(1000):
        idx = randint(0, len(w) - 1)
        # w.pop(idx)
        # w = w[:-1]
        w.pop()
    en = ts()
    print(f'elapsed: {en-st:.3f}s')
    print(len(w))
