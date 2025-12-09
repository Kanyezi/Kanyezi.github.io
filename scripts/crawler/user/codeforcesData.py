import requests
import json
import time
import datetime
import os
def get_user_ac_count(handle):
    """
    获取指定用户的AC题目数量
    :param handle: Codeforces用户名
    :return: AC题目数量（整数）
    """
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    
    try:
        # 发送API请求
        response = requests.get(url)
        data = response.json()
        
        # 检查API响应状态
        if data['status'] != 'OK':
            print(f"错误: {data.get('comment', '未知错误')}")
            return None
        
        submissions = data['result']
        ac_problems = set()  # 使用集合存储唯一题目标识
        
        for submission in submissions:
            # 筛选AC提交
            if submission.get('verdict') == 'OK':
                problem = submission['problem']
                # 生成题目唯一标识 (contestId, index)
                problem_id = (problem['contestId'], problem['index'])
                ac_problems.add(problem_id)
        
        return len(ac_problems)
    
    except requests.exceptions.RequestException as e:
        print(f"网络错误: {e}")
        return None
    except Exception as e:
        print(f"处理错误: {e}")
        return None
# 使用示例
def codeforces_gets(user_path,problems_path):
    data = {}

    with open(user_path,'r', encoding='utf-8') as f:
        data = json.load(f)
        # print(data)
    with open(problems_path+str(datetime.date.today())+"_codeforces.json",'w', encoding='utf-8') as f:
        ru = {}
        for user in data:
            uname = user['name']
            uid = user['codeforces_id']
            if(uid==""):
                print(f"用户 {uname} id未写入")
                continue
            ac_count = get_user_ac_count(uid)
            if ac_count is not None:
                print(f"用户 {uname} 在Codeforces上AC的题目数量为: {ac_count}")
                ru[uname]=ac_count
            else:
                print("获取数据失败，请检查用户名或网络连接")
            time.sleep(0.1)
        json.dump(ru,f)
if __name__ == "__main__":
    # print(get_user_ac_count("YonagiKei"))
    codeforces_gets()