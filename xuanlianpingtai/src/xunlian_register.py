import requests
import random
import base64

host = "https://xxxxxxxx"
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

def register(username):
    while True:
        phone = "1820064%s"%random.randint(999,9999)
        #获取图片KEY值
        captcha_url = "https://xxxxxxx/api/register-captcha"
        a1 = requests.get(captcha_url)
        key = a1.json().get("key")
        phone_url = "https://xxxxxxxx/api/register-sms"
        params = {
            "mobile":phone,
            "captcha_value":30,
            "key":key
        }
        code1 = requests.get(phone_url,params=params,headers=headers).json()
        if code1.get("code") == 20000:
            verification_code = code1.get("sms_code")
            data = {
                "username": username,
                "mobile": phone,
                "password": "xxxxxx",
                "captcha_value": 30,
                "verification_code": verification_code,
                "check": True
            }
            a2 = requests.post(host, data=data, headers=headers)
            break

    else:
        pass

def login_desk(username):
    """登录成功，修改配置的headers"""
    login_url = "https://xxxxxxxx" + '/api/login'
    data = {
        'username': username,
        'password': 'xxxxx',
    }
    # 获取登录的token
    res_login = requests.post(login_url, data=data)
    res_token = res_login.json().get('token_info').get('access_token')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
    headers['Authorization'] = 'Bearer %s' % res_token
    return  headers

def email_true(username):
    headers = login_desk(username)
    email = "1%s@qq.com" % random.randint(999, 9999)
    url = "https://xxxxxxx/api/user/base/bind-email/verification-code?email=asdas@qq.co"
    params={"email":email}
    code = requests.get(url,params=params,headers=headers).json()
    email_code = code.get("email_code")
    url1 = "https://xxxxxxx/api/user/base/bind-email"
    data = {
        "email":email,
        "verification_code":email_code
    }
    a1 = requests.post(url1,data=data,headers=headers)
    print(a1.json())

# email_true("zh123")
if __name__ == "__main__":
    for i in range(10):
        email_true("zheng%s"%i)