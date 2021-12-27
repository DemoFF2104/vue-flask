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


def find_primal():
    k = 0
    while k == 0:
        flag = 0
        a = random.randint(2000, 10000)
        if a % 2 == 1:
            for i in range(3, math.ceil(math.sqrt(a)), 2):
                if a % i == 0:
                    flag = 1
                    break

            if flag == 0:
                k = 1
    return a


def inversion(c, m):
    U = [c, 1, 0]
    V = [m, 0, 1]
    T = [0, 0, 0]
    while V[0] != 0:
        q = U[0] // V[0]

        T[0] = U[0] % V[0]
        T[1] = U[1] - (q * V[1])
        T[2] = U[2] - (q * V[2])

        U = V
        V = [T[0], T[1], T[2]]

    if U[1] < 0:
        U[1] = U[1] + m

    return U[1]


def gen_secret_key(number_of_keys, p, abonent):
    count = 0
    resultKey = ''
    while count < number_of_keys:
        c = random.randint(3, p - 1)
        d = inversion(c, p - 1)
        if c * d % (p - 1) == 1:
            if abonent == 0:
                resultKey = resultKey + (f'{c} {d}\n')
            elif abonent == 1:
                resultKey = resultKey + (f'{c} {d}\n')
            count += 1
    return resultKey


def step_1(input_txt):
    step_2_txt = ''
    p = ''
    if p == '':
        p = find_primal()

    input_txt = input_txt

    secret_1 = ''
    if secret_1 == '':
        secret_1 = gen_secret_key(len(input_txt), p, 0)

    secret_1_splitn = secret_1.split('\n')
    # print(secret_1_splitn[0].split()[0])

    for i in range(len(input_txt)):
        message = bin_pow(ord(input_txt[i]),
                          int(secret_1_splitn[i].split()[0]), p)
        step_2_txt += chr(message)
    return step_2_txt, p, secret_1


def step_2(step_2_txt, p):
    p = int(p)
    input_txt = step_2_txt
    step_3_txt = ''
    secret_2 = ''
    if secret_2 == '':
        secret_2 = gen_secret_key(len(input_txt), p, 1)

    secret_2_splitn = secret_2.split('\n')
    for i in range(len(input_txt)):
        message = bin_pow(ord(input_txt[i]),
                          int(secret_2_splitn[i].split()[0]), p)
        step_3_txt += chr(message)
    return step_3_txt, secret_2


def step_3(step_3_txt, p, secret_1):
    p = int(p)
    input_txt = step_3_txt
    secret_1 = secret_1
    step_4_txt = ''
    if secret_1 == '':
        print('error')
    secret_1_splitn = secret_1.split('\n')
    for i in range(len(input_txt)):
        message = bin_pow(ord(input_txt[i]),
                          int(secret_1_splitn[i].split()[1]), p)
        step_4_txt += chr(message)
    return step_4_txt


def step_4(step_4_txt, p, secret_2):
    p = int(p)
    answer_txt = ''
    input_txt = step_4_txt
    secret_2 = secret_2
    if secret_2 == '':
        print('error')
    secret_2_splitn = secret_2.split('\n')
    for i in range(len(input_txt)):
        message = bin_pow(ord(input_txt[i]),
                          int(secret_2_splitn[i].split()[1]), p)
        answer_txt += chr(message)
    return answer_txt
