import os
import requests
import time
import random
import re


def randomly_gen_uspace_url():
    uid_list = random.sample(range(10000,35000),12)
    return list(map(lambda n:"https://www.hostloc.com/space-uid-{}.html".format(str(n)), uid_list))


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


def check_login_status(s, number_c):
    # 获取设置页面标题以测试是否登录成功
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


def get_points(s, number_c):
    if check_login_status(s, number_c):
        url_list = randomly_gen_uspace_url()
        for url in url_list:
            try:
                s.get(url)
                print("用户空间链接：" + url + " 访问成功")
                time.sleep(4)
            except Exception as e:
                print(str(e))
            continue
    else:
        print("请检查你的帐户是否正确！")


if __name__ == "__main__":
    username = os.environ["HOSTLOC_USERNAME"]
    password = os.environ["HOSTLOC_PASSWORD"]

    user_list = username.split(",")
    passwd_list = password.split(",")

    for i in range(len(user_list)):
        try:
            s = login(user_list[i], passwd_list[i])
            get_points(s, i + 1)
            print("******************************")
        except Exception as e:
            print("密码个数不匹配，错误信息：" + str(e))
        continue
