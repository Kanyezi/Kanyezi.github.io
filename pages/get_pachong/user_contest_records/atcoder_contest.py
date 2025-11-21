import requests
import json
import os

def get_atcoder_contest_standing(contests):
    url=f"https://atcoder.jp/contests/{contests}/standings/json"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Cookie":"REVEL_SESSION=d152d00a2652f1652f7a6e5ac63a73f60a8b0f2d-%00UserScreenName%3Akanyezi%00%00UserName%3Akanyezi%00%00a%3Afalse%00%00w%3Afalse%00%00_TS%3A1779295763%00%00csrf_token%3A6M28Q8oit3d8V%2F87OvUU95Zp9nEtNCLC4WZ7CMET1zo%3D%00%00SessionKey%3A24276a9c6fceaea27ad7f3f8662c0379f24cf07a24ca0ded44272837a9b74a87%00; _ga_RC512FD18N=GS2.1.s1763743306$o7$g1$t1763743764$j58$l0$h0; _ga=GA1.1.1842048823.1762102707; REVEL_FLASH=; timeDelta=-364; OJB_Session_ojb_updateL10nWebsiteJson_zh=true"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"AtCoder请求失败，状态码：{response.status_code}")
            return None
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"AtCoder网络请求错误: {e}")
        return None
    except Exception as e:
        print(f"AtCoder处理过程中发生错误: {e}")
        return None
def save_json_to_file(contest):
    standing = get_atcoder_contest_standing(contest)

    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(current_dir)
    path_r = os.path.join(current_dir,"./public/data.json")
    # print(path_r)
    path_w = os.path.join(current_dir,"../public/contest/atcoder")
    # print(path_w)
    with open(path_w+f"/{contest}.json",'w', encoding='utf-8') as f:
        json.dump(standing, f, ensure_ascii=False, indent=4)
        print(f"AtCoder排名数据已保存到{contest}.json")
def read_json(contest):
    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path_w = os.path.join(current_dir,"../public/contest/atcoder")
    with open(path_w+f"/{contest}.json",'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
if __name__ == "__main__":
    contest = "abc380"
    save_json_to_file(contest)
    
