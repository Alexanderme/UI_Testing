import logging
import os.path
import time
import zipfile
def loggs(logname=""):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = "%s"%logname+time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    log_path = "/zheng/xuanlianpingtai" + '/Logs/'
    log_name = log_path + rq + '.Logs'
    logfile = log_name
    fh = logging.FileHandler(logfile,encoding="utf-8",mode="a")
    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    return logger
def zip_ya(test_dir,res_dir):
    myzip = zipfile.ZipFile(test_dir)
    myzip.extractall(res_dir)
    myzip.close()