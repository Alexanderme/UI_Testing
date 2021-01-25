from xunlian_login import  Zheng
import os
from xunlian_log import zip_ya
from docs.config import Web_Config,Admin_Config
import requests
import time
import random

class XLPT_Test(Zheng):
    def __init__(self,username):
        super(XLPT_Test,self).__init__(username,"test")

    # 提交测试代码
    def git_push_code(self):
        user_message = self.get_git_path()
        # '''提交代码到远程仓库'''
        git_user = user_message.get('data').get('gitlab_username')
        git_pwd = user_message.get('data').get('gitlab_password')
        git_train_path = user_message.get('data').get('gitlab_path')[7:].replace("xxxxxxx", "xxxxxxxx").replace("train-code","open-vino")
        git_ev_sdk_path = user_message.get('data').get('encoding_gpu_containers')[7:].replace("xxxxxx","xxxxxxx")
        git_train_dir_name = git_train_path.split('/')[-1]
        git_ev_sdk_dir_name = git_ev_sdk_path.split('/')[-1]
        os.chdir(Web_Config.git_path)  # 修改当前工作路径
        os.system("git clone http://%s:%s@%s" % (git_user, git_pwd, git_train_path))
        time.sleep(10)
        os.chdir(os.path.join(Web_Config.git_path, git_train_dir_name))
        zip_ya(os.path.join(Web_Config.git_path, "open_vino.zip"), os.path.join(Web_Config.git_path, git_train_dir_name))
        os.system("git add .")
        os.system("git commit -m 'test'")
        os.system('git push')

    #构建测试镜像
    def initiate_testing(self):
        self.logger.info(self.username+"开始构建镜像")
        url = Web_Config.web_host + Web_Config.generate_test_url.format(instance_id=self.instance_id)
        requests.post(url,headers=self.headers)
        time.sleep(10)
        try:
            while True:
                url1 = Web_Config.web_host + Web_Config.generate_test_log_url.format(instance_id=self.instance_id)
                code = requests.get(url1,headers=self.headers).json()
                time.sleep(10)
                logs = code.get("log")
                if "Success" in logs:
                    self.logger.info(self.username + "构建镜像成功")
                    break
        except Exception as e:
            self.logger.info(self.username+"请求日志出错%s"%e)

    #查询模型列表
    def select_models(self):
        url = Web_Config.web_host + Web_Config.select_models_url.format(instance_id=self.instance_id)
        code = requests.get(url,headers=self.headers).json()
        try:
            self.number_test_id =code.get("list")[1].get("id")
        except Exception as  e:
            self.logger.info(self.username + "模型生成有误")


    #发起openvino测试
    def testing(self):
        url = Web_Config.web_host + Web_Config.test_url.format(instance_id=self.instance_id)

        data ={"model_dir_ids": [self.number_test_id], "algorithm_name": "测试1", "algorithm_tag": "a1"}
        code = requests.post(url,json=data,headers=self.headers).json()
        openvino_code =code.get("msg")
        self.logger.info(self.username + "%s"%openvino_code)
        t1 = time.time()
        while True:
            time.sleep(10)
            url1 = Web_Config.web_host + Web_Config.test_code_url.format(instance_id=self.instance_id)
            code = requests.get(url1,headers=self.headers).json()
            t2 = time.time() - t1
            if code.get("list")[0].get("status_cn") == "测试完成":
                self.logger.info(self.username + "openvino测试成功OK")
                break
            elif t2 > 220:
                self.logger.info(self.username + "openvino测试成功卡住了")
                break

    #查询测试任务的ID
    def select_test_id(self):
        try:
            url = Web_Config.web_host + Web_Config.select_test_task_url.format(instance_id=self.instance_id)
            code = requests.get(url,headers=self.headers).json()
            self.test_task_id = code.get("list")[0].get("id")
        except:
            pass

    #进入排行榜
    def go_in_list(self):
        url = Web_Config.web_host + Web_Config.go_in_list_url.format(test_task_id=self.test_task_id)
        requests.post(url,headers=self.headers)
        print("进入排行榜")
        self.logger.info(self.username + "进入排行榜成功")

    #进入候选
    def go_in_candidate(self):
        url = Admin_Config.admin_host+Admin_Config.go_in_lsit_url%self.project_id
        code = requests.get(url,headers=self.headers_admin).json()
        codes = code.get("data")
        for i in codes:
            if i.get("username") == self.username:
                self.houxuan_id = i.get("id")
                url1 = Admin_Config.admin_host + Admin_Config.go_in_houxuan
                data = {"id":self.houxuan_id,"type":random.randint(0,1)}
                self.type_cpu_gpu = data.get("type")
                requests.post(url1,json=data,headers=self.headers_admin)
                print("后台已进入候选")
                self.logger.info(self.username + "后台已进入候选，请等整点查看")

    #编码环境三的代码提交

    #提交封装
    def encapsulate(self):
        url = Web_Config.web_host + Web_Config.git_encapsulate_url.format(instance_id=self.instance_id)
        code = requests.get(url,headers=self.headers).json()
        if code.get("msg") == "此算法候选不存在":
            print("算法未能成功在排行榜排上名")

def test_main(name,code=False):
    zz = XLPT_Test(name)
    if code == True:
        zz.git_push_code()
    # zz.initiate_testing()
    zz.select_models()
    zz.testing()
    # zz.select_test_id()
    # zz.go_in_list()
    # zz.go_in_candidate()

#
# for i in range(10):
#     name = "zheng" + str(i)
#     test_main(name)
#     time.sleep(10)




