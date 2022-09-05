
from random import sample
from hashlib import md5
import sys
import pymysql
from test.func import *

config = load_config()
db_config = config['db']


class DB():
    def __init__(self):
        try:
            self.connect = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                passwd=db_config['password'],
                db=db_config['db'],
                port=db_config['port']
            )
        except Exception as e:
            print(e)
            sys.exit(-1)
        else:
            print("db connect ok")

    def login(self, username, password):
        """
            校验用户名与密码
            返回是否成功
            如果失败返回提示信息
        """
        sql = f"""
            select password_md5,salt
            from user_info
            where username="{username}";
        """
        with self.connect.cursor(cursor=pymysql.cursors.DictCursor) as dict_cursor:
            dict_cursor.execute(sql)
            res = dict_cursor.fetchone()
            print(res)
            if res is None:
                flag, err_msg = False, "username not exits"
            elif res['password_md5'] == get_md5(password+res['salt']):
                flag, err_msg = True, None
            else:
                flag, err_msg = False, "wrong password"

            return flag, err_msg

    def register(self, username: str, name: str, password: str) -> bool:
        """
            根据用户名/姓名/密码生成一个账户
            返回是否成功
            如果失败,返回错误信息,交给前端进行显示
        """
        if password == "":
            # 密码为空
            return False, "password empty"
        if name == "":
            # 姓名为空
            return False, "name empty"

        salt = generate_salt()
        password_md5 = get_md5(password+salt)

        sql = f"""
            insert into user_info(username,`name`,`password_md5`,`salt`)
            VALUE ("{username}","{name}","{password_md5}","{salt}");
        """
        with self.connect.cursor() as cursor:
            try:
                cursor.execute(sql)
                self.connect.commit()
            except Exception as e:
                # 用户名重复
                print(e)
                return False, "username used"
            else:
                return True, None

    def name_select(self, username):
        """
            根据用户名查找用户的真实姓名
            返回是否成功
        """
        sql = f"""
            select name from user_info where username="{username}"
        """
        with self.connect.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchone()
            if res is None:
                flag, err_msg = False, "login error"
            else:
                flag, err_msg = True, res[0]
        return flag, err_msg

    def __del__(self):
        try:
            self.connect.close()
        except:
            pass
        finally:
            print("db close")


def generate_salt() -> str:
    """
        生成一个32位的随机字符串
    """
    res = ""
    for i in sample("abcdefghijklmnopqrstuvwxyz0123456789", 32):
        res += i
    return res


def get_md5(s: str) -> str:
    """
        对输入的字符串进行md5处理
    """
    md = md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()


if __name__ == "__main__":
    # salt = generate_salt()
    # print(f"salt, {salt}")
    # password = input("password: ")
    # password_md5 = get_md5(password + salt)
    # print(f"password_md5: {password_md5}")

    db = DB()
    # res = db.register("wh","王浩然",'')
    # print(res)

    name = db.name_select("wh")

    print(db.login("wh", "hello"))
