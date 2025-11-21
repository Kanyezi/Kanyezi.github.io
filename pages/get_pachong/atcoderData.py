import os
import json
import time
import datetime
from atcoder_get import get_user_ac_count_api

def atcoder_gets():
    data = {}
    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(current_dir)
    path_r = os.path.join(current_dir,"./public/data.json")
    print(path_r)
    path_w = os.path.join(current_dir,"./public/atcoder/")
    print(path_w)

    with open(path_r,'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(path_w+str(datetime.date.today())+"_atcoder.json",'w', encoding='utf-8') as f:
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
                print("获取数据失败，请检查用户名或网络连接")
            time.sleep(0.1)
        json.dump(ru,f)

# 使用示例
if __name__ == "__main__":
    atcoder_gets()