from src.xunlian_train import train_main
from src.xunlian_test import test_main
from src.xunlian_login import Zheng
from multiprocessing import Pool
import time
def main_train():
    p = Pool(50)
    # 启动100个进程将数据切片后进行运算
    for i in range(51,100):
        name = "zz"+str(i)
        p.apply_async(train_main,args=(name,))
    p.close()
    p.join()
def main_test(sumber):
    p = Pool(sumber)
    # 启动100个进程将数据切片后进行运算
    for i in range(sumber):
        name = "zheng"+str(i)
        p.apply_async(test_main,args=(name,))
    p.close()
    p.join()


if __name__ == "__main__":
    for i in range(5000):
        try:
            main_train()
            time.sleep(60)
        except Exception as e:
            with open("errot.txt","a") as f:
                f.write(str(e)+'\n')

    """传入用户名，是否上传代码，默认不上传"""
    # train_main('zz1')
    # ones_list = []
    # threes_list = []
    # fives_list = []
    # servens_list = []
    # nines_list = []
    # tens_list = []
    # for _ in range(10):
    #     number = [1,3,5,7,9,10]
    #     for i in number:
    #         main_test(i)
    #         time.sleep(60)
    #         if i == 1:
    #             one_list = []
    #             for a in range(i):
    #                 name = "zheng" + str(a)
    #                 zz = Zheng(name)
    #                 res = zz.test_code()
    #                 one_list.append(res)
    #             ones_list.append(one_list)
    #         elif i == 3:
    #             three_list = []
    #             for a in range(i):
    #                 name = "zheng" + str(a)
    #                 zz = Zheng(name)
    #                 res = zz.test_code()
    #                 three_list.append(res)
    #             threes_list.append(three_list)
    #         elif i == 5:
    #             five_list = []
    #             for a in range(i):
    #                 name = "zheng" + str(a)
    #                 zz = Zheng(name)
    #                 res = zz.test_code()
    #                 five_list.append(res)
    #             fives_list.append(five_list)
    #         elif i == 7:
    #             serven_list = []
    #             for a in range(i):
    #                 name = "zheng" + str(a)
    #                 zz = Zheng(name)
    #                 res = zz.test_code()
    #                 serven_list.append(res)
    #             servens_list.append(serven_list)
    #         elif i == 9:
    #             nine_list = []
    #             for a in range(i):
    #                 name = "zheng" + str(a)
    #                 zz = Zheng(name)
    #                 res = zz.test_code()
    #                 nine_list.append(res)
    #             nines_list.append(nine_list)
    #         elif i == 10:
    #             ten_list = []
    #             for a in range(i):
    #                 name = "zheng" + str(a)
    #                 zz = Zheng(name)
    #                 res = zz.test_code()
    #                 ten_list.append(res)
    #             tens_list.append(ten_list)
    #
    # print("一路运行的列表")
    # print(ones_list)
    # print("三路运行的列表")
    # print(threes_list)
    # print("五路运行的列表")
    # print(fives_list)
    # print("七路运行的列表")
    # print(servens_list)
    # print("九路运行的列表")
    # print(nines_list)
    # print("十路运行的列表")
    # print(tens_list)




    # train_main("zz2",code=True)
    # main_test()
