# Лабораторна робота №2.2
# Серебряков Роман, ІО-71
# Варіант №22
# Число гармонік в сигналі n = 10
# Гранична частота, w_max = 1200
# Кількість дискретних відліків, N = 64

# Додаткое завдання:
# порівняти час виконання ффт вашої реалізації та numpy

import random as r
import math
import matplotlib.pyplot as plt
from datetime import datetime
from numpy import fft

n = 10
w_max = 1200
N = 64


x = [0] * N

def generate_x(N: int):
    x = [0] * N
    for i in range(n):
        A = r.randrange(2)
        W = r.randrange(w_max)
        f = r.randrange(1000000)
        for t in range(N):
            x[t] += A * math.sin(W * t + f)


generate_x(N)


def fast_fourier_trans(x: list):
    N = len(x)
    fft = [[0] * 2 for i in range(N)]
    for i in range(N // 2):
        array1 = [0] * 2
        array2 = [0] * 2
        for j in range(N // 2):
            cos = math.cos(4 * math.pi * i * j / N)
            sin = math.sin(4 * math.pi * i * j / N)
            array1[0] += x[2 * j + 1] * cos # real
            array1[1] += x[2 * j + 1] * sin # imag
            array2[0] += x[2 * j] * cos # real
            array2[1] += x[2 * j] * sin # imag
        cos = math.cos(2 * math.pi * i / N)
        sin = math.sin(2 * math.pi * i / N)
        fft[i][0] = array2[0] + array1[0] * cos - array1[1] * sin # real
        fft[i][1] = array2[1] + array1[0] * sin + array1[1] * cos # imag
        fft[i + N // 2][0] = array2[0] - (array1[0] * cos - array1[1] * sin) # real
        fft[i + N // 2][1] = array2[1] - (array1[0] * sin + array1[1] * cos) # imag
    return fft


# Виконання додаткового завдання


for x_size in range(N * 20, N * 80, N // 8):
    generate_x(x_size)
    first = datetime.now()
    # Моя реалізація ФФТ
    fast_fourier_trans(x)
    second = datetime.now()
    # Реалізація із numpy: fft(a)
    fft.fft(x)
    third = datetime.now()
    first = first.second * 1e6 + first.microsecond
    second = second.second * 1e6 + second.microsecond
    third = third.second * 1e6 + third.microsecond
    print('X length: {}, default fft: {}, numpy fft {}'.format(x_size, second - first, third - second))


exit(0)



fft = fast_fourier_trans(x)

data_fft = [math.sqrt(fft[i][0] ** 2 + fft[i][1] ** 2) for i in range(N)]

plt.plot([i for i in range(N)], x)
plt.show()
plt.plot([i for i in range(N)], data_fft)
plt.show()