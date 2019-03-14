import hashlib


def md5():
    hash1 = hashlib.md5()  # md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
    hash1.update(bytes('admin', encoding='utf-8'))  # 要对哪个字符串进行加密，就放这里
    return hash1.hexdigest()  # 拿到加密字符串


# hash2=hashlib.sha384()#不同算法，hashlib很多加密算法
# hash2.update(bytes('admin',encoding='utf-8'))
# print(hash.hexdigest())

def md5_params():
    hash3 = hashlib.md5(bytes('abd', encoding='utf-8'))
    """
    如果没有参数，所以md5遵守一个规则，生成同一个对应关系，如果加了参数，
    就是在原先加密的基础上再加密一层，这样的话参数只有自己知道，防止被撞库，
    因为别人永远拿不到这个参数
    """
    hash3.update(bytes('admin', encoding='utf-8'))
    return hash3.hexdigest()


def md5_no_params():
    pwd4 = 'gua'
    hash4 = hashlib.md5()
    hash4.update(bytes(pwd4, encoding='utf-8'))
    return hash4.hexdigest()


def sha():
    pwd4 = 'gua'
    hash4 = hashlib.sha1()
    hash4.update(bytes(pwd4, encoding='utf-8'))
    return hash4.hexdigest()


def md5_2():
    m = '123'.encode('ascii')
    p = hashlib.md5(m)
    print(p.hexdigest())


def get_pwd_by_hash(hashcode):
    """
    有可能可以通过暴力破解的方式获取你的原始密码
    可以通过将常用的一些密码数据全部获取后放到一个字典中，拿到用户数据密码后进行查询
    """
    for i in range(200):
        m = str(i).encode('ascii')
        p = hashlib.md5(m)
        pwd = p.hexdigest()
        if hashcode == pwd:
            print('原密码信息为:', i)


if __name__ == '__main__':
    # md5_2()
    get_pwd_by_hash(hashcode='202cb962ac59075b964b07152d234b70')