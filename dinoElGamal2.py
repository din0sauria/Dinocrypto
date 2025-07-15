from random import randint
import sympy
import sys

sys.setrecursionlimit(10000)

def fastExpMod(a, e, m):
    """
    快速幂模运算。
    参数:
        a -- 底数
        e -- 指数
        m -- 模数
    返回:
        a^e mod m 的结果
    """
    a = a % m
    res = 1
    while e != 0:
        if e & 1:
            res = (res * a) % m
        e >>= 1
        a = (a * a) % m
    return res

def primitive_element(p, q):
    """
    在给定的素数p和其因子q下，找到一个本原元素g。
    参数:
        p -- 素数
        q -- p的因子
    返回:
        本原元素g
    """
    while True:
        g = randint(2, p - 2)
        if fastExpMod(g, 2, p) != 1 and fastExpMod(g, q, p) != 1:
            return g

def primitive_root(p):
    """
    找到一个在模p下以2为指数的本原根。
    参数:
        p -- 素数
    返回:
        以2为指数的本原根
    """
    while True:
        g = randint(2, p - 2)
        if fastExpMod(g, 2, p) != 1:
            return g

def e_gcd(a, b):
    """
    扩展欧几里得算法。
    参数:
        a -- 第一个整数
        b -- 第二个整数
    返回:
        最大公约数g以及贝祖等式的系数x和y
    """
    if b == 0:
        return a, 1, 0
    g, x, y = e_gcd(b, a % b)
    return g, y, x - a // b * y

def encrypt(p, g, y, m):
    """
    使用ElGamal加密算法对消息m进行加密。
    参数:
        p -- 素数
        g -- 本原根
        y -- 公钥
        m -- 明文消息
    返回:
        加密后的密文(C1, C2)
    """
    while True:
        k = randint(2, p - 2)
        if e_gcd(k, p - 1)[0]:
            break
    c1 = fastExpMod(g, k, p)
    c2 = (m * fastExpMod(y, k, p)) % p
    return c1, c2

def decrypt(c1, c2, p, a):
    """
    使用ElGamal解密算法对密文进行解密。
    参数:
        c1 -- 密文的第一部分
        c2 -- 密文的第二部分
        p -- 素数
        a -- 私钥
    返回:
        解密后的明文消息
    """
    v = fastExpMod(c1, a, p)
    v_1 = e_gcd(v, p)[1]
    m_d = c2 * v_1 % p
    return m_d

def main():
    """
    主函数，生成大素数p，找到本原元素g，生成公私钥对，并对消息进行加密和解密。
    """
    m = 1
    while True:
        q = sympy.randprime(10 ** 149, 10 ** 150 / 2 - 1)
        if sympy.isprime(q):
            p = 2 * q + 1
            if len(str(p)) == 150 and sympy.isprime(p):
                break
    g = primitive_element(p, q)
    a = randint(2, p - 2)
    y = fastExpMod(g, a, p)
    c1, c2 = encrypt(p, g, y, m)
    m_d = decrypt(c1, c2, p, a)
    print("明文：m = %d\n公钥：\np = %d\ng = %d\ng^a = %d\n密文(C1, C2) = (%d,%d)\n明文m = %d"% (m, p, g, y, c1, c2, m_d))

    return m, p, g, y, c1, c2, m_d

def test2():
    p=5
    m=3
    g=primitive_root(p)
    x=randint(2,p-2)
    y=fastExpMod(g,x,p)
    c1,c2=encrypt(p,g,y,m)
    m_d=decrypt(c1,c2,p,x)
    print("明文：m = %d\n公钥：\np = %d\ng = %d\ng^x = %d\n密文：(C1, C2) = (%d,%d)\n解密明文：m = %d"% (m, p, g, y, c1, c2, m_d))

if __name__ == '__main__':
    test2()