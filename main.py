from arg_cat import ArgCat
import requests
import json

# 0. 设置公用变量
url = "https://www.imacso.com/wp-admin/admin-ajax.php"
# 1. 登录，获取cookie
# 1.1 获取用户名和密码参数
argcat = ArgCat()
argcat.add_key("username")
argcat.add_key("password")
argcat.from_arg_and_environ(environ_override_all=False)
# 1.2 登录，并获取cookie
payload_login = {'action': 'user_login',
                 'username': argcat.get_string("username"),
                 'password': argcat.get_string("password")}
response_login = requests.request("POST", url, data=payload_login)
cookies = response_login.cookies.get_dict()
login_content = json.loads(response_login.text)
print(login_content['msg'])
# 2. 使用cookie，进行签到
payload_qiandao = {'action': 'user_qiandao'}
response_qiandao = requests.request("POST", url, data=payload_qiandao, cookies=cookies)
qiandao_content = json.loads(response_qiandao.text)
print("status: " + qiandao_content['status'])
print(qiandao_content['msg'])

