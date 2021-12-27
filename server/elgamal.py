from tkinter import *
from tkinter import scrolledtext
import random
import math


def bin_pow(a,x,p):
    bin_x=bin(x)[2:]
    result = a
    for i in range(1, len(bin_x)):
        result = ((result * result) * pow(a, int(bin_x[i]))) % p
    return result

def gen_p_q_g():
    l = 0
    while l == 0:
        k = 0
        while k == 0:
            p = random.randint(1000, 10000)
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
        if pow(g, q) != 1:
            flag = 1
    return p,g


def secret_key_generation(index,p,g):
    p = int(p)
    g = int(g)
    openK = 0
    secK = 0
    c = random.randint(2, p - 2)
    if index == 0:
        secK = c
        openK = bin_pow(g, c, p)
        return secK, openK
    elif index == 1:
        secK = c
        openK = bin_pow(g, c, p)
        return secK, openK


def key_generation():
    p, g = gen_p_q_g()
    secKeyA, openKeyA = secret_key_generation(0,p,g)
    secKeyB, openKeyB = secret_key_generation(1,p,g)
    return p, g, secKeyA, openKeyA, secKeyB, openKeyB


def send_message(txt, p , g,openKeyB):
    txt_input = txt
    sended_message = ''
    p = int(p)
    g = int(g)
    c = int(openKeyB)
    r_number = []
    for i in range(len(txt_input)):
        k = random.randint(1, p - 2)
        r_number.append(bin_pow(g, k, p))
        sended_message += chr((ord(txt_input[i]) * pow(c, k)) % p)
    return sended_message, r_number


def decode_message_el(txt, r_number,secKeyB,p):
    txt_input = txt
    r_number = r_number
    c = int(secKeyB)
    p = int(p)
    decoded_message=''
    for i in range(len(txt_input)):
        decoded_message+=chr((ord(txt_input[i]) * pow(r_number[i], p - 1 - c)) % p)
    return decoded_message
