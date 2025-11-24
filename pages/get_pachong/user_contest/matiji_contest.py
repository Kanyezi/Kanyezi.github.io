import requests
import json
import os

def get_matiji_contest_standing(contest):
    url=f"https://www.matiji.net/exam-back/pc/queryMatchRankListById.do"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Cookie":"JSESSIONID=2C51BB74572A173298FC3EC7E2B339B4; SERVERID=b94def476a02d1e749557bf71c4ff9e4|1763743352|1763743345; Hm_lvt_91dd75297031f8bd0eaeb64ef3d6e20e=1763743348; Hm_lpvt_91dd75297031f8bd0eaeb64ef3d6e20e=1763743348; HMACCOUNT=805CFE86B17DDDF1"
    }
    #start=0&limit=10&matchId=296
    data = {
        "start":"0",
        "limit":"1",
        "matchId":f"{contest}"
    }
    try:
        requ = requests.post(url, headers=headers,data=data)
        data["limit"]=requ.json()["data"]["total"];
        # print(data["limit"])
        response = requests.post(url, headers=headers,data=data)
        if response.status_code != 200:
            print(f"matiji请求失败，状态码：{response.status_code}")
            return None
        data = response.json()
        # print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"matiji网络请求错误: {e}")
        return None
    except Exception as e:
        print(f"matiji处理过程中发生错误: {e}")
        return None
def save_json_to_file(contest):
    standing = get_matiji_contest_standing(contest)

    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(current_dir)
    path_r = os.path.join(current_dir,"./public/data.json")
    # print(path_r)
    path_w = os.path.join(current_dir,"../public/contest/matiji")
    # print(path_w)
    with open(path_w+f"/{contest}.json",'w', encoding='utf-8') as f:
        json.dump(standing, f, ensure_ascii=False, indent=4)
        print(f"matiji排名数据已保存到{path_w}/{contest}.json")
def read_json(contest):
    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path_w = os.path.join(current_dir,"../public/contest/matiji")
    with open(path_w+f"/{contest}.json",'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
if __name__ == "__main__":
    contest = "296"
    save_json_to_file("296")
    
