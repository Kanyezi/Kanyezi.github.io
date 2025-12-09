import json
import time
import datetime
from .matiji_get import get_user_ac_count
import os

def matiji_gets(user_path,problems_path):
    data = {}
    
    with open(user_path,'r', encoding='utf-8') as f:
        data = json.load(f)
        # print(data)
    with open(problems_path+str(datetime.date.today())+"_matiji.json",'w', encoding='utf-8') as f:
        ru = {}
        for user in data:
            uname = user['name']
            uid = user['matiji_id']
            if(uid==""):
                print(f"用户 {uname} id未写入")
                continue
            ac_count = get_user_ac_count(uid)
            if ac_count is not None:
                print(f"用户 {uname} 在码题集上AC的题目数量为: {ac_count}")
                ru[uname]=ac_count
            else:
                print(uid,"获取数据失败，请检查用户名或网络连接")
            time.sleep(0.1)
        json.dump(ru,f)

# 使用示例
if __name__ == "__main__":
    matiji_gets()