import os
import json
import time
import datetime
import requests

def get_user_ac_count_api(username):
    """
    使用AtCoderProblems API获取用户AC题目数量
    :param username: AtCoder用户名
    :return: AC题目数量（整数），失败返回None
    """
    # AtCoderProblems API接口
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank?user={username}"

    try:
        # 发送GET请求
        response = requests.get(url)
        # 解析JSON响应
        resjson = response.json()
        res = resjson['count']
        return res
    
    except requests.exceptions.RequestException as e:
        return None

def atcoder_gets(user_path,problems_path):
    data = {}
    with open(user_path,'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(problems_path+str(datetime.date.today())+"_atcoder.json",'w', encoding='utf-8') as f:
        ru = {}
        for user in data:
            uname = user['name']
            uid = user['atcoder_id']
            if(uid==""):
                print(f"用户 {uname} id未写入")
                continue
            ac_count = get_user_ac_count_api(uid)
            if ac_count is not None:
                print(f"用户 {uname} 在AtCoder上AC的题目数量为: {ac_count}")
                ru[uname]=ac_count
            else:
                print(uname,"获取数据失败，请检查用户名或网络连接")
            time.sleep(0.1)
        json.dump(ru,f)

# 使用示例
if __name__ == "__main__":
    # print(get_user_ac_count_api("tokyoww"))
    atcoder_gets()