import json
import time
import datetime
from matiji_get import get_user_ac_count
import os

# 使用示例
if __name__ == "__main__":
    # 替换为你想查询的AtCoder用户名
    # username = "tourist"  # 示例：著名选手tourist
    data = {}
    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(current_dir)
    path_r = os.path.join(current_dir,"./public/data.json")
    print(path_r)
    path_w = os.path.join(current_dir,"./public/matiji/")
    print(path_w)
    with open(path_r,'r', encoding='utf-8') as f:
        data = json.load(f)
        # print(data)
    with open(path_w+str(datetime.date.today())+"_matiji.json",'w', encoding='utf-8') as f:
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