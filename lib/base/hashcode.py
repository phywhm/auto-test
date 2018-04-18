# -*- coding:utf-8 -*-


def convert_n_bytes(n, b):
    bits = b*8
    return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)


def convert_4_bytes(n):
    return convert_n_bytes(n, 4)


def hash_code(s):
    h = 0
    n = len(s)
    for i, c in enumerate(s):
        h = h + ord(c)*31**(n-1-i)
    return convert_4_bytes(h)


def get_bucket_num(s):
    return hash_code(s) & 15

if __name__ == '__main__':
    print (hash_code('testcid1') & 15)
    print hash_code('testcid1')
