import math


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def sha1(message):
    message = bytearray(message, 'utf8')  # переписываем в массив байтов
    orig_len_in_bits = (
        8 * len(message)
    ) & 0xffffffffffffffff  #массив байтов умножаем на 8 и получаем длину битов и отсекаем по 2**64
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='big')

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for chunk_ofst in range(0, len(message), 64):
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        chunk = message[chunk_ofst:chunk_ofst + 64]
        w = [0] * 80
        for n in range(0, 16):
            w[n] = int.from_bytes(chunk[4 * n:4 * n + 4], byteorder='big')

        for i in range(16, 80):
            w[i] = left_rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]),
                               1)

        #самый наш основной цикл
        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def getHashSha(bufer_in):
    #bufer_in = bytearray(input_txt.get("1.0", 'end-1c'), encoding='utf-8')
    return sha1(bufer_in)
