import requests
from docs.config import Web_Config,Admin_Config
import json
from src.xunlian_log import loggs
import time
class Zheng():
    def __init__(self,username,logname=""):
        self.username = username  #用户名
        self.headers = self.login_desk() #headers
        self.headers_admin = self.login_background()  #amdin_headers
        self.project_id = self.get_id()   #项目ID
        self.email = self.get_email()     #邮箱
        self.instance_id = self.get_instance_id() #实例ID
        self.logger = loggs(logname)
        self.logger.info(self.username+"用户的信息已获取完毕")
        self.apply_code = self.get_apply()
        #前台登录，返回headers

    def login_desk(self):
        """登录成功，修改配置的headers"""
        login_url = Web_Config.web_host + '/api/login'
        data = {
            'username': self.username,
            'password': 'xxxxxxx',
        }
        # 获取登录的token
        res_login = requests.post(login_url, data=data)
        res_token = res_login.json().get('token_info').get('access_token')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
        headers['Authorization'] = 'Bearer %s' % res_token
        return headers


    def login_background(self):
        # login
        url_login = Admin_Config.admin_host + '/api/login'
        # url_login = Admin_Config.admin_host + '/login'
        headers = {"Content-Type": "application/json"}
        data = {
            'username': 'admin',
            'password': 'xxxxxx',
        }
        data = json.dumps(data)
        # 获取登录的token

        res_login = requests.post(url_login, data=data, headers=headers)
        res_token = res_login.json().get('data').get('access_token')
        headers = {'Authorization': 'Bearer %s' % (res_token)}
        return headers


    #获取项目id
    def get_id(self):
        url = Web_Config.web_host + Web_Config.get_project_id
        code = requests.get(url, headers=self.headers).json()
        project_id = code.get("list")[3].get("id")
        return project_id
    """获取邮箱"""
    def get_email(self):
        url = Web_Config.web_host+Web_Config.get_base_user
        code = requests.get(url,headers=self.headers).json()
        email = code.get("email")
        return email

    #获取实例ID
    def get_instance_id(self):
        time.sleep(1)
        url = Web_Config.web_host + Web_Config.paginate_url
        code1 = requests.get(url, headers=self.headers).json()
        print(code1)
        # print("OK")

        # time.sleep(1)
        try:
            # print(code1)
            instance_id = code1.get("list")[0].get("id")
            return instance_id
        except Exception as e:
            print(self.username,"获取实例ID错误")
            return None
    #判断是否报名
    def get_apply(self):
        url = Web_Config.web_host + Web_Config.get_project_id
        code = requests.get(url,headers=self.headers).json()
        status_operate_zh = code.get("list")[3].get("status_operate_zh")
        # print(status_operate_zh)
        if status_operate_zh == "报名中" or status_operate_zh == "创建实例":
            return True
        else:
            return False

    #判断是否全部完成训练
    def train_code(self):
        url = Web_Config.web_host + Web_Config.train_code_url.format(instance_id=self.instance_id)
        # time.sleep(1)
        code = requests.get(url,headers=self.headers).json()
        # print(code)
        try:
            if code.get("list")[0].get("status_cn") == "训练完成":
                if "10-20" in code.get("list")[0].get("updated_at"):
                    pass
                else:
                    print(self.username+"状态%s"%code.get("list")[0].get("status_cn"),"时间:%s"%code.get("list")[0].get("updated_at"))
                # print(self.username,"========",code.get("list")[0].get("status_cn"))
            else:
                print(self.username+"状态%s"%code.get("list")[0].get("status_cn"))
        except Exception as e:
            print(self.username,"========None",)
    """训练中止或撤销"""
    def stop_train(self):
        url = Web_Config.web_host + Web_Config.train_code_url.format(instance_id=self.instance_id)
        code = requests.get(url, headers=self.headers).json()
        if code.get("list")[0].get("status_cn") == "排队中":
            url = "http://xxxxxxx/api/online-train/instance/train/%s/revoked" % code.get("list")[0].get("id")
            a1 = requests.patch(url, headers=self.headers)
        elif code.get("list")[0].get("status_cn") != "训练中":
            url = "http://xxxxxxx/api/online-train/instance/train/%s/aborted" % code.get("list")[0].get("id")
            a1 = requests.patch(url, headers=self.headers)

    """测试查询状态"""
    def test_code(self):
        url = Web_Config.web_host + Web_Config.select_test_task_url.format(instance_id=self.instance_id)
        code = requests.get(url,headers=self.headers).json()
        if code.get("list")[0].get("status_cn") == "测试完成":
            return  code.get("list")[0].get("fps")
        else:
            return self.username + "状态%s" % code.get("list")[0].get("status_cn")

    """中止测试"""
    def stop_test(self):
        url = Web_Config.web_host + Web_Config.select_test_task_url.format(instance_id=self.instance_id)
        code = requests.get(url,headers=self.headers).json()
        if code.get("list")[0].get("status_cn") == "排队中":
            url = "http://xxxxxxx/api/online-train/instance/sdk-test/%s/revoked" % code.get("list")[0].get("id")
            a1 = requests.patch(url, headers=self.headers)
        elif code.get("list")[0].get("status_cn") != "测试中":
            url = "http://xxxxxxx/api/online-train/instance/sdk-test/%s/aborted" % code.get("list")[0].get("id")
            a1 = requests.patch(url, headers=self.headers)







    """获取Git仓库等信息"""
    def get_git_path(self):
        url = Admin_Config.admin_host + Admin_Config.instancelist_url

        try:
            codes = requests.get(url,headers=self.headers_admin).json().get("data")
            for code in codes:
                name = code.get("username")
                if name == self.username:
                    id_num = code.get("id")
                    # 获取git账号
                    url_git_account = Admin_Config.admin_host + Admin_Config.git_url.format(id=id_num)
                    res_git_account = requests.get(url_git_account, headers=self.headers_admin).json()
                    self.logger.info(self.username+"git信息获取完毕")
                    return res_git_account
        except Exception as e:
            self.logger.info(self.username+"获取信息失败%s"%e)


# if __name__ == "__main__":
#     for i in range(10):
#         name = "zheng"+str(i)
#         zz = Zheng(name)
#         zz.test_code()
#         print(time.strftime('%Y-%m-%d-%H', time.localtime(time.time())))