import sys
from random import randint
from math import gcd
import bitstring
import base64

def euclid_ext(a, b):
    if b == 0:  
        return a, 1, 0
    else:
        d, x, y = euclid_ext(b, a % b)
        return d, y, x - y * (a // b)
    

def keygen(n, b):
    #generation of u_i sequence:
    u = [0] * n
    st = 2 << (b - n)
    k, sum = 1, 0
    for i in range(n):
        u[i] = randint((k - 1) * st + 1, k * st - 1)
        k *= 2
        sum += u[i]
    N = randint(sum + 1, (2 << b) - 1)
    #generation of a (coprime with N) and a^(-1)modN:
    a = randint(2, N)
    while gcd(a, N) != 1:
        a += 1
    ext = euclid_ext(a,N) 
    a_inv = ext[1]
    #print(a_inv, (a * a_inv) % N) #проверочный вывод: (a*(обратный элемент)) % N == 1
    f1 = open('sk.txt', 'w')
    f1.write(str(a) + ' ')
    f1.write(str(N) + ' ')
    for i in range(n):
        f1.write(str(u[i]) + ' ')
    f1.close()
    #print(a, N, '\n')
    #generation of w_i sequence:
    w = [0] * n
    f2 = open('pk.txt', 'w')
    for i in range(n):
        w[i] = (a_inv * u[i]) % N
        #print(w[i], u[i], a_inv, u[i] * a_inv, N)
        f2.write(str(w[i]) + ' ')
    f2.close()

def enc(W, M):
    M_bytes = M.encode()
    M_bits = bitstring.BitArray(M_bytes)
    c = 0
    print(len(W), len(M_bits))
    #calculate the ciphertext
    for i in range(min(len(W), len(M_bits))):
        c += int(W[i]) * M_bits[i]
    print('First min(length(pk), number_of_bits(text))=', min(len(W), len(M_bits)), ' bits encrypted')
    f = open('ctext.txt', 'wb')
    f.write(base64.b32encode(str(c).encode()))
    f.close()

def basis(w, c):
    n = len(w)
    b0 = [0] * (n + 1)
    b = list()
    #print(w)
    for i in range(n):
        b0[i] += 1
        b0[n] -= int(w[i])
        b.append(b0.copy())
        b0[i] -= 1
        b0[n] += int(w[i])
    b0[n] = int(c)
    b.append(b0)
    #print(b)
    return b

def squared_norma(bi):
    res = 0
    for i in range(len(bi)):
        res += bi[i] * bi[i]
    return res

def mu(bi, bj):
    res = 0
    for i in range(len(bi)):
        res += bi[i] * bj[i]
    return res / squared_norma(bj)

def mul(a, v):
    av = v.copy()
    for i in range(len(v)):
        av[i] = a * v[i]
    return av

def plus(v1, v2):
    sum = v1.copy()
    for i in range(len(v1)):
        sum[i] = v1[i] + v2[i]
    return sum

def orthogonalizationGSh(b, n):
    b_ort = list()
    b_ort.append(b[0])
    for i in range(1, n):
        tmp = b[i].copy()
        for j in range(i):
            tmp = plus(tmp, mul(-mu(b[i], b_ort[j]), b_ort[j]))
        b_ort.append(tmp)
    #for i in range(n):
        #print(i, b[i], b_ort[i])
    return b_ort

def LLL(b, n):
    delta = 3 / 4
    b_ort = orthogonalizationGSh(b, n)
    flag = True
    while flag:
        flag = False
        for i in range(1, n):
            for j in range(i - 1, -1, -1):
                c = mu(b[i], b_ort[j])
                c = min(min(abs(int(c) - c), abs(int(c) + 1 - c)), abs(int(c) - 1 - c))
                b[i] = plus(b[i], mul(-c, b[j]))
                flag = True
            b_ort = orthogonalizationGSh(b, n)
        for i in range(1, n - 1):
            if delta * squared_norma(b_ort[i]) > squared_norma(plus(mul(mu(b[i + 1], b_ort[j]), b_ort[i]), b_ort[i + 1])):
                b[i], b[i + 1] = b[i + 1], b[i]
                flag = True
    return b


def check(b, n, w, c):
    for i in range(n):
        flag = True
        for j in range(n):
            if (b[i][j] != 0) or (b[i][j] != 1):
                flag = False
                break
        if flag:
            print(b[i])
            return b[i]
    print("Crack failed")

def dec(w, c):
    b = basis(w, c)
    b_LLL = LLL(b, len(w) + 1)
    n = len(b_LLL)
    res = check(b_LLL, n, w, int(c))
    if res[n - 1] == 1:
        s = 0
        for i in range(n - 1):
            s += b_LLL[i][n - 1]
        c = s - b_LLL[n - 1][n - 1]
        b = basis(w, c)
        b_LLL = LLL(b, len(w) + 1)
        n = len(b_LLL)
        res = check(b_LLL, n, w, int(c))
        if res[n - 1] != 0:
            print("Crack failed")
            return
    f = open('cracktext.txt', 'w')
    str = '0b'
    for i in range(len(res)):
        str += str(res[i])
    str_bit = bitstring.BitArray(str)
    cracktext = str_bit.hex.decode('utf-8')
    f.write(cracktext)
    f.close()

# main
if len(sys.argv) > 1: 
    mode = sys.argv[1]
else:
    mode = str(input('Enter mode (keygen, enc or dec):'))
if mode == 'keygen':
    print('KEYGEN_mode:')
    n = int(input('Enter parametr n:'))
    b = int(input('Enter parametr b:'))
    keygen(n, b)
elif mode == 'enc':
    print('ENCRYPTION_mode:')
    if len(sys.argv) > 3:
        path_pk = sys.argv[2]
        path_text = sys.argv[3]
    else:
        path_pk = str(input('Enter path to the file with public key:'))
        path_text = str(input('Enter path to the file with text:'))
    f_pk = open(path_pk, 'r')
    pk = f_pk.read().split()
    f_pk.close()
    f_text = open(path_text, 'r', encoding = "utf-8")
    text = f_text.read()
    f_text.close()
    #print(sys.getsizeof(text))
    enc(pk, text)
elif mode == 'dec':
    print('DECRYPTION_mode:')
    if len(sys.argv) > 3:
        path_pk = sys.argv[2]
        path_ctext = sys.argv[3]
    else:
        path_pk = str(input('Enter path to the file with public key:'))
        path_ctext = str(input('Enter path to the file with ciphertext:'))
    f_pk = open(path_pk, 'r')
    pk = f_pk.read().split()
    f_pk.close()
    f_ctext = open(path_ctext, 'rb')
    ctext = base64.b32decode(f_ctext.read())
    f_ctext.close()
    dec(pk, ctext)
else:
    print('Wrong input')
