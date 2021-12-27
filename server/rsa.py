from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import numpy as np
import random
import math
import sys


def bin_pow(a, x, p):
    bin_x = bin(x)[2:]
    result = a
    for i in range(1, len(bin_x)):
        result = ((result * result) * pow(a, int(bin_x[i]))) % p
    return result


def gen_primal_number():
    flag = 0
    while flag == 0:
        k = random.randint(2, 10000000)
        range_chisla = pow(10, 100)
        d = 2 * k + 1
        number = 2 * d
        s = 1
        while number // range_chisla < 1:
            number = 2 * number
            s += 1

        number += 1
        if bin_pow(5, d, number) == 1:
            flag = 1
        a = 5
        for r in range(s):
            if bin_pow(a, pow(2, r) * d, number) == number - 1:
                flag = 1

    return number


def gen_primal_e(start, stop):
    flag = 0
    while flag == 0:
        k = random.randint(start, 10000000)
        range_chisla = pow(10, 100)
        d = 2 * k + 1
        number = 2 * d
        s = 1
        while number // range_chisla < 1:
            number = 2 * number
            s += 1

        number += 1
        if bin_pow(5, d, number) == 1:
            flag = 1
        a = 5
        for r in range(s):
            if bin_pow(a, pow(2, r) * d, number) == number - 1:
                flag = 1

    return number


def gcd(a, b):
    a = int(a)
    b = int(b)
    U = [a, 1, 0]
    V = [b, 0, 1]
    T = [0, 0, 0]
    while V[0] != 0:

        q = U[0] // V[0]

        T[0] = U[0] % V[0]
        T[1] = U[1] - (q * V[1])
        T[2] = U[2] - (q * V[2])

        U = V
        V = [T[0], T[1], T[2]]
    return U[0]


def gen_e(p, q):
    fi = (p - 1) * (q - 1)
    flag = 0
    while flag == 0:
        e = gen_primal_e(3, fi)
        if gcd(e, fi) == 1:
            break
    return e


def inversion(a, b):
    U = [a, 1, 0]
    V = [b, 0, 1]
    T = [0, 0, 0]
    while V[0] != 0:
        q = U[0] // V[0]
        T[0] = U[0] % V[0]
        T[1] = U[1] - (q * V[1])
        T[2] = U[2] - (q * V[2])

        U = V
        V = [T[0], T[1], T[2]]

    if U[1] < 0:
        U[1] = U[1] + b

    return U[1]


def code_message(text):
    samiy_vajniy_flag = 0
    result = ''
    while samiy_vajniy_flag == 0:
        p = gen_primal_number()
        q = gen_primal_number()
        while p == q:
            q = gen_primal_number()

        e = gen_e(p, q)
        d = inversion(e, (p - 1) * (q - 1))
        while e == d:
            d = inversion(e, (p - 1) * (q - 1))

        n = p * q

        input_message = text
        for i in input_message:
            shifr = bin_pow(ord(i), e, n)
            result = result + ' ' + str(shifr)
        samiy_vajniy_flag = 1
    return result, str(d), str(n)


def decode_message(text, d, n):
    result = ''
    input_message = text.split()
    d = int(d)
    n = int(n)
    for i in input_message:
        answer = bin_pow(int(i), d, n)
        result += chr(answer)
    return result