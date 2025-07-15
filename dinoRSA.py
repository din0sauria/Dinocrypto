import random


def int2bytes(integer: int) -> bytes:
    """
    整数转换成字节串
    :param integer:
    :return: 返回字节串
    """
    # 1.计算所需的最小字节数
    if integer == 0:
        len = 1
    else:
        len = int((integer.bit_length() + 7) // 8)

    # 2.整数转换为字节串
    byte_string = integer.to_bytes(len, byteorder='big')
    return byte_string


def calculate_block_size(n: int) -> int:
    """
    计算块大小
    :param n: 模数n
    :return: 返回块大小，单位:字节/块
    """
    return (n.bit_length() - 1) // 8


def gcd(a: int, b: int) -> int:
    """
    欧几里得算法-求两个数的最大公约数
    :param a: 整数
    :param b: 整数
    :return: 返回a、b的最大公约数
    """
    while b != 0:
        a, b = b, a % b
    return a


def ext_gcd(a: int, b: int) -> tuple:
    """
    扩展欧几里得算法-求乘法逆元
    :param a: 整数
    :param b: 整数
    :return: (gcd, x, y)，其中gcd是a和b的最大公约数，x和y是整数，满足 a*x + b*y = gcd
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    gcd, x, y = a, x0, y0
    return gcd, x, y


def miller_rabin(n: int, k: int = 100) -> bool:
    """
    使用 Miller-Rabin 算法判断一个整数是否为素数
    :param n: 待检测的整数
    :param k: 迭代次数，k 越大，准确率越高
    :return: 如果 n 是素数，返回 True；否则返回 False
    """
    # 特殊情况处理
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # 将 n-1 写成 2^r * d 的形式
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # 进行 k 次迭代
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def gen_prime(bits: int) -> int:
    """
    随机生成指定位数的素数
    :param bits: 指定随机生成素数的位数
    :return: 返回指定位数的随机生成素数
    """
    while True:
        # 1.生成一个随机的bits的位奇数
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1  # 确保最高位和最低位为1
        # 2.使用Miller-Rabin素性检测算法判断是否为素数
        if miller_rabin(candidate):
            return candidate


def quick_mod(a: int, b: int, mod: int) -> int:
    """
    模重复平方算法-大数的模幂运算
    :param a: 底数
    :param b: 指数
    :param mod: 模数
    :return: 返回余数d
    """
    c, d = 0, 1
    # 将 b 转为二进制字符串
    bin_b = bin(b)[2:]
    for i in bin_b:
        c = c * 2
        d = d * d % mod
        if i == '1':
            c = c + 1
            d = (d * a) % mod
    return d


def gen_key(bits: int = 1024) -> tuple:
    """
    生成密钥对
    :param bits: 指定生成p,q两个质因数的位数
    :return: (e,n),(d,n)
    """
    # 1.生成p和q两个质因数
    p = gen_prime(bits)
    while True:
        q = gen_prime(bits)
        if p != q:
            break

    # 2.计算除数n和n的欧拉函数值phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # 3.生成与phi互质的公钥e
    # e=65537
    while True:
        e = random.randint(2, phi - 1)
        # 判断是e、phi否互质
        if gcd(e, phi) == 1:
            break

    # 4.计算私钥d
    # 确保d是正数并且在 phi 的范围内
    d = ext_gcd(e, phi)[1] % phi

    return (e, n), (d, n)


def rsa_encrypt(m: bytes, public_key: int, n: int) -> tuple:
    """
    RSA加密函数
    :param m: 明文
    :param public_key: 公钥
    :param n: 模数
    :return: 返回加密明文
    """
    # 1.计算块的大小
    # 保证每明文块的十进制数小于n,单位:字节/块
    block_size = calculate_block_size(n)

    # 2.进行加密
    bytes_encrypted_blocks = []
    int_encrypted_blocks = []
    for i in range(0, len(m), block_size):
        # 取出单个明文快
        block = m[i:i + block_size]
        # 将明文块转换为整数
        int_block = int.from_bytes(block, byteorder='big')
        # 对明文快进行加密
        int_encrypted_block = quick_mod(int_block, public_key, n)
        int_encrypted_blocks.append(int_encrypted_block)
        # 整数转成字节串
        bytes_encrypted_block = int2bytes(int_encrypted_block)
        bytes_encrypted_blocks.append(bytes_encrypted_block)
    return bytes_encrypted_blocks, int_encrypted_blocks  # 字节串列表/整数列表


def rsa_decrypt(c: list, private_key: int, n: int) -> tuple:
    """
    RSA解密函数
    :param c: 密文
    :param public_key: 私钥
    :param n: 模数
    :return: 返回解密密文
    """
    # 1.计算块的大小
    block_size = calculate_block_size(n)

    # 2.进行解密
    bytes_decrypted_blocks = []
    int_decrypted_blocks = []
    for block in c:
        # 将密文块转换为整数
        int_block = int.from_bytes(block, byteorder='big')
        # 对密文块进行解密
        int_decrypted_block = quick_mod(int_block, private_key, n)
        int_decrypted_blocks.append(int_decrypted_block)
        # 整数转成字节串
        bytes_decrypted_block = int2bytes(int_decrypted_block)
        bytes_decrypted_blocks.append(bytes_decrypted_block)
    return bytes_decrypted_blocks, int_decrypted_blocks  # 字节串列表/整数列表


def main():
    # 1.生成密钥对
    public_key, private_key = gen_key()
    print(f'公钥e:{public_key[0]}')
    print(f'私钥d:{private_key[0]}')
    print(f'模数n:{private_key[1]}')

    # 2.加密
    m = 'dinosaur'
    m_bytes = m.encode()
    print("明文:",m)

    c = rsa_encrypt(m_bytes, public_key[0], public_key[1])
    print('密文(int):',c[1][0])

    # 3.解密
    m = rsa_decrypt(c[0], private_key[0], private_key[1])
    print('解密密文:',b''.join(m[0]).decode())


def test1():
    p=3
    q=11
    d=7
    m=5
    n=p*q
    phi=(p-1)*(q-1)
    e=ext_gcd(d,phi)[1]
    c=quick_mod(m,e,n)
    print(c)

def test2():
    e=3
    n=33
    C=9
    for p in range(2,n):
        if n%p==0:
            q=n//p
            break
    phi=(p-1)*(q-1)
    d = ext_gcd(e, phi)[1]
    print(quick_mod(C,d,n))

def test3():
    p=17
    q=11
    e=7
    m=88
    n=p*q
    phi=(p-1)*(q-1)
    d=ext_gcd(e,phi)[1]
    c=quick_mod(m,e,n)
    print(c)

    

if __name__ == '__main__':
    test3()