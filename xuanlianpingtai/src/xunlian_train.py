from xunlian_login import Zheng
from docs.config import Web_Config
import os
import time
from xunlian_log import zip_ya
import requests
class XLPT_Train(Zheng):
    """docstring for Train"""
    def __init__(self,username):
        super(XLPT_Train,self).__init__(username,"train")
    def push_git_code(self):
        user_message = self.get_git_path()
        # '''提交代码到远程仓库'''
        git_user = user_message.get('data').get('gitlab_username')
        git_pwd = user_message.get('data').get('gitlab_password')
        git_train_path = user_message.get('data').get('gitlab_path')[7:].replace("xxxxx","xxxxxx")
        git_ev_sdk_path = user_message.get('data').get('encoding_gpu_containers')[7:].replace("xxxxx","xxxxxx")

        git_train_dir_name = git_train_path.split('/')[-1]
        git_ev_sdk_dir_name = git_ev_sdk_path.split('/')[-1]
        os.chdir(Web_Config.git_path) #修改当前工作路径
        os.system("git clone http://%s:%s@%s" % (git_user, git_pwd, git_train_path))
        time.sleep(10)

        os.chdir(os.path.join(Web_Config.git_path,git_train_dir_name))
        print(os.path.join(Web_Config.git_path,"train.zip"))
        print(os.path.join(Web_Config.git_path,git_train_dir_name))
        zip_ya(os.path.join(Web_Config.git_path,"train.zip"),os.path.join(Web_Config.git_path,git_train_dir_name))

        os.system("git add .")
        os.system("git commit -m 'test'")
        os.system('git push')
        self.logger.info(self.username+"git代码提交完成")
        return True

    """报名"""
    def xu_apply(self):
        if self.apply_code == True:
            url = Web_Config.web_host+Web_Config.instance_url
            data = {
                "frame_id":1,
                "project_id":self.project_id
            }
            code = requests.post(url,data=data,headers=self.headers).json()
            self.instance_id = code.get("id") #返回实例ID
            print(self.instance_id )
            time.sleep(60)
            print(code)
        else:
            pass

    """创建实例"""
    def creat_instance(self):
        if self.instance_id == None:
            url = Web_Config.web_host+Web_Config.instance_url
            data = {
                "frame_id":1,
                "project_id":self.project_id
            }
            code = requests.post(url,data=data,headers=self.headers).json()
            self.instance_id = code.get("id") #返回实例ID
            print(self.instance_id )
            time.sleep(60)
        else:
            print(self.instance_id)

    """上传代码"""
    def push_code(self):
        res_git_account = self.push_git_code()
        return res_git_account

    """构建训练镜像"""
    def build_training(self):
        print("===开始构建")
        url = Web_Config.web_host+Web_Config.generate_url.format(instance_id=self.instance_id)
        code = requests.post(url,headers=self.headers).json()
        self.logger.info(self.username+":开始构建训练镜像")
        time.sleep(10)
        t1 = time.time()
        while True:
            url1 = Web_Config.web_host + Web_Config.generate_log_url.format(instance_id=self.instance_id)
            code = requests.get(url1,headers=self.headers).json()
            time.sleep(10)
            try:
                t2 = time.time() - t1
                logs = code.get("log")
                if "pushed done..." in logs:
                    self.logger.warning(self.username+":构建成功,时间花费%s秒"%t2)
                    time.sleep(10)
                    break
                elif t2>500:
                    self.logger.warning(self.username + ":构建超时")
                    break
            except Exception as e:
                self.logger.error(self.username+"请求构建日志出错了%s"%e)
                break

    """发起训练"""
    def creat_train(self):
        time.sleep(10)
        self.logger.info(self.username + "发起训练")
        url = Web_Config.web_host+Web_Config.train_url.format(instance_id=self.instance_id)
        data = {
         "exec_command":"bash /project/train/src_repo/start_train.sh"
        }
        code = requests.post(url,data=data,headers=self.headers).json()
        self.logger.info(self.username+":%s"%code.get("msg"))
        t1 = time.time()
        while True:
            url1 = Web_Config.web_host+Web_Config.train_code_url.format(instance_id=self.instance_id)
            code = requests.get(url1,headers=self.headers).json()
            train_code = code.get("list")[0].get("status_cn")
            if train_code == "排队中":
                time.sleep(60)
                t1 = time.time()
            else:
                time.sleep(4)
                t2 = time.time() - t1
                if code.get("list")[0].get("status_cn") == "训练完成":
                    self.logger.warning(self.username + ":训练完成，时间花费%s秒"%t2)
                    break
                elif t2>1000:
                    self.logger.warning(self.username + ":训练超时")
                    break


def train_main(name,code=False):
    zz = XLPT_Train(name)
    zz.xu_apply()
    zz.creat_instance()
    if code == True:
        zz.push_code()
    zz.build_training()
    zz.creat_train()
#
# for i in range(51,100):
#     name = "zz" + str(i)
#     train_main(name,True)
#     time.sleep(2)

