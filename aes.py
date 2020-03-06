# -*- coding: utf-8 -*-
import galois_math

field = galois_math.Galois()


def hexprint(arr):
    for el in arr:
        print(hex(el)[2:], ' ', end='')
    print()


def circ_l_shift(a, n=1, k=8):
    for i in range(n):
        a <<= 1
        if a & 1 << k:
            a ^= 1 << k
            a ^= 1
    return a


def s_box(num, mode=False):
    def affine(n):
        aff = 0x63
        s = n ^ circ_l_shift(n, 1)
        s ^= circ_l_shift(n, 2)
        s ^= circ_l_shift(n, 3)
        s ^= circ_l_shift(n, 4)
        s ^= aff
        return s

    def inv_affine(n):
        aff = 0x5
        t = circ_l_shift(n, 1)
        t ^= circ_l_shift(n, 3)
        t ^= circ_l_shift(n, 6)
        t ^= aff
        return t

    if mode == 0:
        # Encryption
        b = field.inv(num)
        b = affine(b)
    else:
        # Decryption
        b = inv_affine(num)
        b = field.inv(b)
    return b


def shift_arr(arr, n=1, dir=False):
    res = arr[:]
    for i in range(n):
        if dir == False:
            temp = res[1:]
            temp.append(res[0])
        else:
            temp = res[:-1]
            temp.insert(0, res[-1])
        res[:] = temp[:]
    return res


def shift_rows(state, mode=False):
    rows = []
    for r in range(4):
        rows.append(state[r::4])
        if mode == False:
            # Encryption
            rows[r] = rows[r][r:] + rows[r][:r]
        else:
            # Decryption
            rows[r] = rows[r][4 - r:] + rows[r][:4 - r]
    return [r[c] for c in range(4) for r in rows]


def mix_columns(state, mode=False):
    def mult(a, b):
        return field.mult(a, b)

    matrices = [[2, 3, 1, 1], [14, 11, 13, 9]]
    m = matrices[mode]
    res = []
    for i in range(4):
        col = state[i * 4:(i + 1) * 4]
        temp = []
        # print('rd_column: ', end='')
        # hexprint(col)
        for j in range(len(col)):
            temp.append(0)
            for k in range(len(m)):
                temp[j] ^= mult(col[k], m[k])
            m = shift_arr(m, 1, True)
        # print('mixed_col: ', end='')
        # hexprint(temp)
        res.extend(temp)
    return res


def xor_arr(s1, s2):
    return tuple(a ^ b for a, b in zip(s1, s2))


def key_schedule(key, nb=4, nr=10):
    def sub_word(word):
        return (s_box(b) for b in word)

    def rot_word(word):
        return shift_arr(word)

    rcon = (0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a)
    expanded = []
    expanded.extend(map(ord, key))
    for i in range(nb, nb * (nr + 1)):
        t = expanded[(i - 1) * 4:i * 4]
        if i % nb == 0:
            t = xor_arr(sub_word(rot_word(t)), (rcon[i // nb], 0, 0, 0))
        elif nb > 6 and i % nb == 4:
            t = sub_word(t)
        expanded.extend(xor_arr(t, expanded[(i - nb) * 4:(i - nb + 1) * 4]))
    return expanded


def add_round_key(state, rkey):
    for i, b in enumerate(rkey):
        state[i] ^= b


def encrypt(block, key, nb=4, nr=10):
    n = nb * 4
    state = list(map(ord, block))
    keys = key_schedule(key)
    add_round_key(state, keys[0:n])
    for r in range(1, nr):
        state = [s_box(a) for a in state]
        state = shift_rows(state)
        state = mix_columns(state)
        k = keys[r * n:(r + 1) * n]
        add_round_key(state, k)

    state = [s_box(a) for a in state]
    state = shift_rows(state)
    add_round_key(state, keys[nr * n:])
    hexprint(state)
    return "".join(map(chr, state))


def decrypt(block, key, nb=4, nr=10):
    n = nb * 4
    state = list(map(ord, block))
    keys = key_schedule(key)
    k = keys[nr * n:(nr + 1) * n]
    add_round_key(state, k)
    for r in range(nr - 1, 0, -1):
        state = shift_rows(state, 1)
        state = [s_box(a, 1) for a in state]
        k = keys[r * n:(r + 1) * n]
        add_round_key(state, k)
        state = mix_columns(state, 1)

    state = shift_rows(state, 1)
    state = [s_box(a, 1) for a in state]
    add_round_key(state, keys[0:n])
    return "".join(map(chr, state))


# arr = []
# for i in range(4):
#     arr.append([])
#     for j in range(4):
#         arr[i].append(i + j)
# arr = [219, 19, 83, 69, 242, 10, 34, 92, 213, 213, 215, 214, 45, 38, 49, 76]
# print(arr)
# arr = mix_columns(arr)S
# print(arr)
word = 'JeanMishelDakuo2'
key = 'Krikunhohhahahah'
print("Source word:", word)
print("Key:", key)
enc = encrypt(word, key)
print("Encrypted data:", enc)
dec = decrypt(enc, key)
print("Decrypted data:", dec)
