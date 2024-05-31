import hashlib
import random
import docx
import PyPDF2

HASH_ALGORITHMS = {
    "MD5": hashlib.md5,
}


MAX = 20


def hash_string(text, mode):
    """Hàm này dùng để băm chuỗi"""
    print("heeloo",HASH_ALGORITHMS[mode](text.encode()).hexdigest())
    return HASH_ALGORITHMS[mode](text.encode()).hexdigest()


def get_data_file(file_path):
    """Hàm đọc file trả về nội"""
    data = []
    file_extension = file_path.split(".")[-1]
    if file_extension == "docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            data.append(para.text)
        data = "\n".join(data)

    elif file_extension == "pdf":
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                data.append(page.extract_text())
            data = "\n".join(data)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        f.close()

    return data


def find_gcd(a: int, b: int) -> int:
    """Hàm tìm ước chung lớn nhất"""
    if b == 0:
        return a
    else:
        return find_gcd(b, a % b)


def check_prime(n: int) -> bool:
    """Hàm này dùng để kiểm tra 1 số có phải số nguyên tố không"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_prime() -> int:
    """Hàm này dùng để chọn 1 số nguyên tố ngẫu nhiên lớn"""
    while True:
        result = random.randint(2 ** (MAX - 2), 2 ** (MAX - 1) - 1)
        if check_prime(result):
            return result


def pow_mod(a: int, b: int, n: int) -> int:
    """Hàm này trả về a^b mod n áp dụng thuật toán bình phương và nhân"""
    p = 1
    s = bin(b)[2:]
    for i in range(len(s)):
        p *= p
        p %= n
        if s[i] == "1":
            p *= a
            p %= n
    return p


def mod_inverse(p: int, k: int) -> int:
    """Hàm này tìm phần tử nghịch đảo k^-1 mod p áp dụng Ơ clít mở rộng"""
    r = [1] * 100
    q = [0] * 100
    s = [0] * 100
    t = [0] * 100
    r[0], r[1] = p, k
    i = 0
    while True:
        q[i + 1] = r[i] // r[i + 1]
        r[i + 2] = r[i] % r[i + 1]
        if i == 0:
            s[0] = 1
            t[0] = 0
        elif i == 1:
            s[1] = 0
            t[1] = 1
        else:
            s[i] = s[i - 2] - q[i - 1] * s[i - 1]
            t[i] = t[i - 2] - q[i - 1] * t[i - 1]
        if r[i + 2] == 0:
            break
        else:
            i += 1
    i += 1
    s[i] = s[i - 2] - q[i - 1] * s[i - 1]
    t[i] = t[i - 2] - q[i - 1] * t[i - 1]
    return t[i] if t[i] > 0 else (t[i] + p)


def gen_alpha(p: int) -> int:
    """Hàm này để tạo số alpha ngẫu nhiên thuộc đoạn [2, p - 1]"""
    return random.randint(2, p - 1)


def gen_a(p: int) -> int:
    """Hàm này để chọn số a ngẫu nhiên thuộc đoạn [2, 3, .. , p - 2]"""
    return random.randint(2, p - 2)


def gen_k(p: int) -> int:
    """Hàm này để chọn số bí mật k thuộc đoạn [1, 2,..., p - 2] sao cho gcd(k, p - 1) = 1"""
    while True:
        k = random.randint(1, p - 2)
        if find_gcd(k, p - 1) == 1:
            return k


def cre_key() -> list:
    """Hàm này dùng để tạo khóa ngẫu nhiên"""
    p = find_prime()
    alpha = gen_alpha(p)
    a = gen_a(p)
    # tính beta = alpha^a mod p
    beta = pow_mod(alpha, a, p)
    k = gen_k(p)
    # gamal = alpha^k mod p
    gamal = pow_mod(alpha, k, p)

    return [p, alpha, a, beta, k, gamal]


def create_sign(text: str, hash: str, gamal: int, a: int, k: int, p: int) -> list:
    """Hàm này dùng để tạo chữ khóa"""
    text_hash = hash_string(text, hash)
    # print(text_hash, gamal, a, k, p)
    text_ascii = [ord(char) for char in text_hash]
    result = []
    k_inv = mod_inverse(p - 1, k)

    for char_ascii in text_ascii:
        # teta = (x - a * gamal) * k_inv % (p - 1)
        teta = (char_ascii - a * gamal) * k_inv % (p - 1)
        result.append(teta)
    # print(result)
    return [result, text_hash]


def verify_sign(
    text: str, hash: str, sign: str, beta: int, gamal: int, alpha: int, p: int
) -> bool:
    """Hàm này dùng để kiểm tra chữ ký số"""
    text_hash = hash_string(text, hash)
    text_ascii = [ord(char) for char in text_hash]

    try:
        sign = eval(sign)
    except:
        return False

    if len(text_ascii) != len(sign):
        return False

    for x, y in zip(sign, text_ascii):
        # (beta^gamal mod p) * (gamal^teta mod p) mod p
        beta_gamal = pow_mod(beta, gamal, p) * pow_mod(gamal, x, p) % p
        # alpha^x mod p
        alpha_x = pow_mod(alpha, y, p)
        if beta_gamal != alpha_x:
            return False

    return True
