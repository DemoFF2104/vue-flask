from tkinter import *
from tkinter import scrolledtext
import random
import math


def bin_pow(a, x, p):
    bin_x = bin(x)[2:]
    result = a
    for i in range(1, len(bin_x)):
        result = ((result * result) * pow(a, int(bin_x[i]))) % p
    return result


def gen_p_q_g():
    l = 0
    while l == 0:
        k = 0
        while k == 0:
            p = random.randint(1000000, 10000000)
            flag = 0
            if p % 2 == 1:
                for i in range(3, math.ceil(math.sqrt(p)) + 1, 2):
                    if p % i == 0:
                        flag = 1
                        break
                if flag == 0:
                    k = 1
        q = int((p - 1) / 2)
        flag = 0
        if q % 2 == 1:
            for i in range(3, math.ceil(math.sqrt(q)) + 1, 2):
                if q % i == 0:
                    flag = 1
                    break
            if flag == 0:
                l = 1

    flag = 0
    while flag == 0:
        g = random.randint(2, p - 2)
        if bin_pow(g, q, p) != 1:
            flag = 1

    return p, q, g


def gen_Y(flag, q, p):
    y = random.randint(1000000, 10000000)
    q = q
    p = p
    if flag == 0:

        Xa = y
        Ya = bin_pow(q, y, p)
        return Xa, Ya

    elif flag == 1:
        Yb = bin_pow(q, y, p)
        Xb = y
        return Yb, Xb


def gen_key(Xa, Ya, Yb, Xb, p):
    X1 = int(Xa)
    X2 = int(Xb)

    Y1 = int(Ya)
    Y2 = int(Yb)

    p = int(p)

    answ1 = bin_pow(Y2, X1, p)
    answ2 = bin_pow(Y1, X2, p)
    return answ1, answ2


def gen_result():
    p, q, g = gen_p_q_g()
    Xa, Ya = gen_Y(0, q, p)
    Yb, Xb = gen_Y(1, q, p)
    answ1, answ2 = gen_key(Xa, Ya, Yb, Xb, p)
    return p, q, g, Xa, Ya, Yb, Xb, answ1, answ2
