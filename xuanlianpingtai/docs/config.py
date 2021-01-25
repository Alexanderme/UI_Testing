import os


class Web_Config:
    git_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"xxxxxxxxxxx")
    abc = "/api/project/{id}"
    web_host="xxxxxxxxxxxxxxxxx" #域名
    desk_login_url = "/api/login" #前端登录url
    get_project_id = "/api/project/paginate?pageSize=5&project_type=1" #获取项目ID
    get_base_user = "/api/user/base" #获取用户信息，主要是邮箱
    baoming_url = "/api/project/register/{project_id}" #报名url
    instance_url = "/api/online-train/instance" #创建实例url
    generate_url = "/api/online-coding/instance/{instance_id}/generate-train-mirror"#构建训练镜像url
    paginate_url = "/api/online-train/instance/paginate?type=project&pageSize=5"#获取训练ID的url，实例的状态
    train_url = "/api/online-train/instance/{instance_id}/train"#发起训练的url
    generate_log_url = "/api/online-coding/instance/{instance_id}/generate-train-mirror/real-time-log/false" #构建训练镜像是否生成
    train_code_url = "/api/online-train/instance/{instance_id}/train/paginate?pageSize=5" #训练的进度


    generate_test_url = "/api/online-coding/instance/{instance_id}/generate-open_vino-mirror"  #构建测试镜像
    generate_test_log_url = "/api/online-coding/instance/{instance_id}/generate-open_vino-mirror/real-time-log/false" #构建的测试镜像是否生成
    select_models_url = "/api/online-train/instance/sdk-test/{instance_id}/model-dir" #获取模型列表
    test_url = "/api/online-train/instance/{instance_id}/sdk-test-open-vino"  #发起openvino测试
    test_code_url = "/api/online-train/instance/{instance_id}/sdk-test/paginate?id=15&pageSize=5" #测试的进度
    go_in_list_url= "/api/online-train/instance/sdk-test/enter-leader-board/{test_task_id}" #进入排行榜 #测试ID
    select_test_task_url = "/api/online-train/instance/{instance_id}/sdk-test/paginate?id={instance_id}&current=1&pageSize=5" #查询测试任务情况
    git_encapsulate_url = "/api/online-train/instance/algo/{instance_id}/sdk-package/base-info/4"  #提交封装
    select_mo_url = "/api/online-train/instance/{instance_id}/model/paginate?instanceid=13&pageSize=5" #查询模型数量
    stop_test1 = "/api/online-train/instance/sdk-test/{test_task_id}/aborted" #停止测试任务




class Admin_Config:
    admin_host = "xxxxxxxxxxxxxx"#域名
    background_login_url = ""#后端登录url
    instancelist_url = "/api/instance-manage/instance/list"#实例列表，为获取git账号url
    git_url = "/api/instance-manage/instance/info?id={id}"#git账号等信息
    go_in_lsit_url = "/api/project-manage/contest-questions/leader-board?id=%s&page=1&per_page=10" #后台排行榜
    go_in_houxuan = "/api/project-manage/contest-questions/enter-candidate"  #进入候选




