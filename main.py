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
argcat.add_key("notification")
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

# 3. 如果发送失败，则通过server酱来发送信息  https://sct.ftqq.com/
if qiandao_content['status'] != '1':
    print("============== 签到失败，发送通知 ==============")
    print(qiandao_content)
    print("--------------------------------------------")
    params_str = 'title=%E7%AD%BE%E5%88%B0%E5%A4%B1%E8%B4%A5%E5%95%A6&channel=9'
    notification_rul = "https://sctapi.ftqq.com/" + argcat.get_string("notification") + ".send?" + params_str
    response_notification = requests.request("GET", notification_rul)
    notification_content = json.loads(response_notification.text)
    print(notification_content)
