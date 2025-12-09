import json
import time
import datetime
import os
import requests
def get_user_ac_count(id):
    url = "https://www.matiji.net/exam-back/pc/queryUserDetailById.do"
    header={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "cookie":"JSESSIONID=18E11AFBE1DDF7C6933A183F7A33F819; Hm_lvt_91dd75297031f8bd0eaeb64ef3d6e20e=1763635541; Hm_lpvt_91dd75297031f8bd0eaeb64ef3d6e20e=1763635541; HMACCOUNT=60B37D0CFB75D3DB; SERVERID=b94def476a02d1e749557bf71c4ff9e4|1763635544|1763635501"
    }
    data={"userId" : id}
    requ = requests.post(url=url,headers=header,data=data);

    # print(requ.json())
    if(requ.status_code!=200 or requ.json()["error_no"]!="0"):
        return None
    else:
        return requ.json()["data"]["passNum"]
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
    # print(get_user_ac_count(218775))
    matiji_gets()