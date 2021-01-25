# @Time : 2020/11/26 11:16 
# @modele : t1
# @Author : zhengzhong
# @Software: PyCharm
import zipfile


def zip_ya(test_dir,res_dir):
    myzip = zipfile.ZipFile(test_dir)
    myzip.extractall(res_dir)
    myzip.close()

zip_ya(r"C:\Users\Administrator\Desktop\ubuntu\xunnnn\xuanlianpingtai\docs\nanyoudaima\train.zip",r"C:\Users\Administrator\Desktop\ubuntu\xunnnn\xuanlianpingtai\docs\nanyoudaima\123")
