import os
import requests
import time
import random
import re


# 随机生成用户空间链接
def randomly_gen_uspace_url():
    url_list = []
    # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
    for i in range(12):
        uid = random.randint(10000, 35000)
        url = "https://www.hostloc.com/space-uid-{}.html".format(str(uid))
        url_list.append(url)
    return url_list


# 登录帐户
def login(username, password):
    headers = {
        "User-Angent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    login_url = "https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    login_data = {
        "fastloginfield": "username",
        "username": username,
        "password": password,
    }
    s = requests.Session()
    s.post(url=login_url, data=login_data, headers=headers)
    return s


# 通过抓取用户设置页面的标题检查是否登录成功
def check_login_status(s, number_c):
    test_url = "https://www.hostloc.com/home.php?mod=spacecp"
    res = s.get(test_url)
    res.encoding = "utf-8"
    test_title = re.findall("<title>.*?</title>", res.text)
    if test_title[0] != "<title>个人资料 -  全球主机交流论坛 -  Powered by Discuz!</title>":
        print("第" + str(number_c) + "个帐户登录失败！")
        return False
    else:
        print("第" + str(number_c) + "个帐户登录成功！")
        return True


# 依次访问随机生成的用户空间链接获取积分
def get_points(s, number_c):
    if check_login_status(s, number_c):
        url_list = randomly_gen_uspace_url()
        # 使用for和try/except实现当前链接访问出错时不中断程序继续访问下一个链接
        for url in url_list:
            try:
                s.get(url)
                print("用户空间链接：" + url + " 访问成功")
                time.sleep(4)  # 每访问一个链接后休眠4秒，以避免触发论坛的防cc机制
            except Exception as e:
                print("链接访问异常：" + str(e))
            continue
    else:
        print("请检查你的帐户是否正确！")


if __name__ == "__main__":
    username = os.environ["HOSTLOC_USERNAME"]
    password = os.environ["HOSTLOC_PASSWORD"]

    # 分割用户名和密码为列表
    user_list = username.split(",")
    passwd_list = password.split(",")

    # 使用for和try/except实现当前用户获取积分出错时不中断程序继续尝试下一个用户
    for i in range(len(user_list)):
        try:
            s = login(user_list[i], passwd_list[i])
            get_points(s, i + 1)
            print("******************************")
        except Exception as e:
            # 已知的一个能触发异常的问题，方便用户检查
            if str(e) == "list index out of range":
                print("用户名与密码个数不匹配！")
            else:
                print("获取积分异常：" + str(e))
        continue
