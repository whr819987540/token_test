
import itsdangerous
import time
try:
    from test.func import *
except:
    from func import *


config = load_config()
token_config = config['token']


def token_generate(username: str) -> str:
    """
        生成与username、时间戳相关的token
    """
    signer = itsdangerous.TimestampSigner(token_config['secret_key'])
    sign_bytes = signer.sign(username)
    sign_str = sign_bytes.hex()
    return sign_str


def token_verify(username: str, token_str: str):
    """
        验证token的有效性
        如果失败,可能是username与token不匹配(受到攻击)
        也可能是token超时了
    """
    signer = itsdangerous.TimestampSigner(token_config['secret_key'])
    try:
        # 验证成功(token与username对应且未失效)
        if signer.unsign(bytes.fromhex(token_str), max_age=token_config['expire_time']).decode() == username:
            flag, msg = True, None
        # token与username不对应
        else:
            flag, msg = False, "token verify failed, under attack"
    # token失效
    except itsdangerous.exc.SignatureExpired:
        flag, msg = False, "time exceed"
    # token被破坏
    except:
        flag, msg = False, "token verify failed, under attack"
        
    return flag, msg


if __name__ == "__main__":
    # signer = itsdangerous.TimestampSigner(config['token']['secret_key'])
    # uid = "whr"
    # sign_bytes = signer.sign(uid)
    # sign_str_hex = sign_bytes.hex()
    # print(sign_bytes == bytes.fromhex(sign_str_hex))
    # time.sleep(2)
    # # 如果超时，引发itsdangerous.exc.SignatureExpired异常
    # try:

    #     print(signer.unsign(sign_bytes,
    #                         max_age=config['token']['expire_time']).decode() == uid)
    # except itsdangerous.exc.SignatureExpired:
    #     print("time exceed")

    username = "1"
    token_str = token_generate(username)
    print(f"token_str {token_str}")
    print(token_verify(username, token_str))
    print(token_verify(3, token_str))

    print(token_verify(
        "3", "332e5978573453772e536e6350694b59785f746a476e3667426741774e36317242664d77"))
