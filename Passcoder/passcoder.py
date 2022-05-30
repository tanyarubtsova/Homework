from random import randint
from math import sqrt
from math import gcd
import base64

def isPrime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n

def euclid_ext(a, b):
    if b == 0:  
        return a, 1, 0
    else:
        d, x, y = euclid_ext(b, a % b)
        return d, y, x - y * (a // b)

def keygen(n):
    low = 1 << (n - 2)
    high = (1 << (n - 1)) - 1
    p = 2 * randint(low, high) + 1
    while ((p % 4 != 3) and isPrime(p) == 0):
        p += 2
    q = 2 * randint(low, high) + 1
    while ((q % 4 != 3) and isPrime(q) == 0):
        q += 2
    N = p * q
    f1 = open('sk.txt', 'w')
    f1.write(str(p) + ' ' + str(q))
    f1.close()
    f2 = open('pk.txt', 'w')
    f2.write(str(N))
    f2.close()

def enc(N, M):
    c = M * M % N
    f = open('enc_passwd.txt', 'wb')
    #f.write(str(c))
    f.write(base64.b32encode(str(c).encode()))
    f.close()

def dec(sk, c):
    p, q = int(sk[0]), int(sk[1])
    N = p * q
    mp = pow(c % p, (p + 1) // 4, p)
    mq = pow(c % q, (q + 1) // 4, q)
    ext = euclid_ext(p, q) 
    p_inv, q_inv = ext[1], ext[2]
    mp = (mp * q % N) * q_inv % N
    mq = (mq * p % N) * p_inv % N
    m1 = (mp - mq) % N
    m2 = (mp + mq) % N
    m3 = N - m1
    m4 = N - m2
    #print(m1, m2, m3, m4)
    lst = [m1, m2, m3, m4]
    for i in lst:
        if i % 10 == 0: # label to determine the password
            print("Your password is: ", i)

# main
if len(sys.argv) > 1: 
    mode = sys.argv[1]
else:
    mode = str(input('Enter mode (reg, enc or dec):'))
if mode == 'reg':
    print('REGISTRATION_mode:')
    n = int(input('Enter parametr n:'))
    keygen(n)
elif mode == 'enc':
    print('ENCRYPTION_mode:')
    path_pk = str(input('Enter path to the file with public key:'))
    f_pk = open(path_pk, 'r')
    pk = f_pk.read()
    pk = int(pk)
    f_pk.close()
    passwd = int(input('Enter the password:')) #digital password
    while (passwd * 10 > pk or passwd * passwd * 100 < pk):
        print('Your password should be more than ', int(sqrt(pk)), ' and less than ', pk)
        print('Your password should be more than ', int(sqrt(pk / 100)), ' and less than ', pk // 10)
        passwd = int(input('Enter another password:'))
    passwd *= 10 # label to determine the password
    #print(passwd)
    enc(pk, passwd)
elif mode == 'dec':
    print('DECRYPTION_mode:')
    path_sk = str(input('Enter path to the file with secret key:'))
    path_encpasswd = str(input('Enter path to the file with encrypted password:'))
    f_sk = open(path_sk, 'r')
    sk = f_sk.read().split()
    f_sk.close()
    f_encpasswd = open(path_encpasswd, 'rb')
    #encpasswd = int(f_encpasswd.read())
    encpasswd = base64.b32decode(f_encpasswd.read())
    encpasswd = str(encpasswd)[2:]
    encpasswd = int(str(encpasswd)[:-1])
    f_encpasswd.close()
    dec(sk, encpasswd)
else:
    print('Wrong input')
