import random

def pgcd(a, b):
    if b == 0:
        return a
    return pgcd(b, a%b)

assert(pgcd(1,1) == 1)
assert(pgcd(25,5) == 5)
assert(pgcd(64,256) == 64)
assert(pgcd(256,64) == 64)

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if pgcd(i, n) > 1:
            return False
        i += 1
    return True

assert(is_prime(2))
assert(not is_prime(4))
assert(not is_prime(42))
assert(not is_prime(15))
assert(is_prime(17))
assert(is_prime(101))
assert(is_prime(257))


# def generate_prime(a, i):
#     primes = []
#     for k in range(a, a+i+1):
#         if is_prime(k):
#             primes.append(k)
#     return random.choice(primes)

# assert(is_prime(generate_prime(1, 100)))

def prime_with(n):
    while True:
        k = random.randint(2, n)
        if pgcd(n, k) == 1:
            return k

assert(pgcd(prime_with(100),100) == 1)

def euclide_etendu(a, b):
    d,u,v,d1,u1,v1 = a,1,0,b,0,1
    while d1 != 0:
        q = d // d1
        d,u,v,d1,u1,v1 = d1,u1,v1,d-q*d1,u-q*u1,v-q*v1
    return (d,u,v)

assert(euclide_etendu(72,12) == (12,0,1))

def inverse_modulaire(a,n):
    (d,b,v) = euclide_etendu(a, n)
    assert(d == 1)
    return b

assert(inverse_modulaire(12, 55) == 23)

def expo_modulaire(e, b, n, debug=False):
    def expo_modulaire_aux(e, b, n, count):
        (countx, countmod) = count
        if e == 1:
            return (b%n, (countx, countmod+1))
        (c, (countx, countmod)) = expo_modulaire_aux(e-1, b, n, count)
        return ((c*b)%n, (countx+1, countmod+1))
    (c, count) = expo_modulaire_aux(e, b, n, (0,0))
    if debug:
        print("(count_x, count_mod) = {}".format(count))
    return c

assert(expo_modulaire(11, 111, 13) == 2)

def expo_modulaire_rapide(e, b, n, debug=False):
    def expo_modulaire_rapide_aux(e, b, n, count):
        (countx, countmod) = count
        if e == 1:
            return (b%n, (countx, countmod+1))
        (c, (countx, countmod)) = expo_modulaire_rapide_aux(e//2, b, n, count)
        if e%2 == 0:
            return ((c*c)%n, (countx+1, countmod+1))
        else:
            return ((c*c*b)%n, (countx+2, countmod+1))

    (c, count) = expo_modulaire_rapide_aux(e, b, n, (0,0))
    if debug:
        print("(count_x, count_mod) = {}".format(count))
    return c

assert(expo_modulaire_rapide(11, 111, 13) == 2)

def crible_eratosthene(n):
    def crible_eratosthene_aux(n, lst, ret):
        a = lst[0]
        if a*a > n:
            return ret + lst
        ret.append(a)
        for k in range(len(lst)):
            if (lst[len(lst)-1-k] % a) == 0:
                del lst[len(lst)-1-k]
        return crible_eratosthene_aux(n, lst, ret)

    return crible_eratosthene_aux(n, range(2,n), [])

assert(len(set(crible_eratosthene(10)) - set([2,3,5,7])) == 0)

# def crible_eratosthene_it(n):
#     lst = range(2,n)
#     ret = []
#     while lst[0]*lst[0] <= n:
#         ret.append(lst[0])
#         for k in range(len(lst)):
#             if (lst[len(lst)-1-k] % lst[0]) == 0:
#                 del lst[len(lst)-1-k]
#     return ret + lst

def test_fermat(n, t):
    for x in random.sample(range(1,n), t):
        if expo_modulaire_rapide(n-1, x, n) > 1:
            return False
    return True

assert(test_fermat(97, 10))
assert(test_fermat(257, 10))
assert(not test_fermat(123, 10))

def decomposition_rabin(n):
    r = 0
    v = 1
    while (n-1) % (2*v) == 0:
        r += 1
        v *= 2
    return (r, (n-1)//v)

assert(decomposition_rabin(337) == (4, 21))

def temoin_rabin(n, r, u, a):
    a_u = expo_modulaire_rapide(u, a, n)
    if (a_u == 1) or (a_u == n-1):
        return False
    for i in range(r):
        if expo_modulaire_rapide(pow(2, i)*u, a, n) == n-1:
            return False
    return True

def test_rabin(n, k):
    if n%2 == 0:
        return n==2
    (r, u) = decomposition_rabin(n)
    for i in range(k):
        a = random.randint(1, n-1)
        if (pgcd(a, n) != 1) or temoin_rabin(n, r, u, a):
            return False
    return True

assert(test_rabin(257, 10))
assert(test_rabin(43, 10))
assert(not test_rabin(1729, 10))

def generate_prime(a=256**14, b=256**15, k_rabin=100):
    while True:
        i = random.randint(a, b)
        if test_rabin(i, k_rabin):
            return i

def generate_rsa_keys():
    (p,q) = (generate_prime(), generate_prime())
    n = p*q
    phi = (p-1)*(q-1)
    e = prime_with(phi)
    d = inverse_modulaire(e, phi) % phi
    return ((n,e), (n,d))


def rsa_encrypt(n, public_key):
    return pow(n, public_key[1], public_key[0])

def rsa_decrypt(n, private_key):
    return pow(n, private_key[1], private_key[0])

pub, priv = generate_rsa_keys()
assert(rsa_decrypt(rsa_encrypt(12, pub), priv) == 12)

def str_to_b256(message):
    n = 0
    p = 1
    for k in range(len(message)):
        n += ord(message[k])*p
        p *= 256
    return n

def b256_to_str(n):
    p = 1
    k = 1
    while p <= n:
        k += 1
        p *= 256
    p //= 256
    k -= 1

    message = ""
    for k in range(k):
        for i in range(256):
            if i*p > n:
                message = str(unichr(i-1)) + message
                n -= (i-1) * p
                break

        p //= 256
    return message

#print(b256_to_str(25185))
#print(str_to_b256("ab"))

e = rsa_encrypt(str_to_b256("hello world!"), pub)
print(rsa_decrypt(e, priv))
print(b256_to_str(rsa_decrypt(e, priv)))
