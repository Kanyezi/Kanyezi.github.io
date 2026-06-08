import requests
import json
import os

def atcoder_usrs(user_path):
    list = {}
    with open(user_path,'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            list[item['atcoder_id']]={"name":item['name']}
    return list
def get_atcoder_contest_standing(contests):
    url=f"https://atcoder.jp/contests/{contests}/standings/json"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Cookie":"_ga=GA1.1.256432136.1774538988; REVEL_FLASH=; timeDelta=-560; _ga_RC512FD18N=GS2.1.s1780916569$o27$g1$t1780917686$j56$l0$h0; REVEL_SESSION=35fb1c3c38dcb8815ced50d9fdf7d6f179a0dcc4-%00a%3Afalse%00%00w%3Afalse%00%00csrf_token%3Az1lS5WwS02ywVAmn05xzOfLxYbmbF0LBkShfEaRGEe4%3D%00%00_TS%3A1796469686%00%00SessionKey%3Afaab912fcdad2a212fb9e2ed5fd5fcc43769a7df8870994b59d93decefe4d0d7%00%00UserScreenName%3Ax_yeyue%00%00UserName%3Ax_yeyue%00"
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
def save_json_to_file(contest,contest_path):
    standing = get_atcoder_contest_standing(contest)
    if standing is None:
        print(f"AtCoder数据获取失败，未保存{contest}.json")
        return
    with open(contest_path+f"/{contest}.json",'w', encoding='utf-8') as f:
        json.dump(standing, f, ensure_ascii=False, indent=4)
        print(f"AtCoder排名数据已保存到{contest}.json")
def read_json(contest,contest_path):
    # current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # path_w = os.path.join(current_dir,"../public/contest/atcoder")
    filepath = contest_path+f"/{contest}.json"
    if not os.path.exists(filepath):
        print(f"AtCoder数据文件不存在: {filepath}")
        return None
    with open(filepath,'r', encoding='utf-8') as f:
        data = json.load(f)
    if data is None:
        print(f"AtCoder数据文件内容为null: {filepath}，需要重新获取")
        return None
    return data
if __name__ == "__main__":
    contest = "abc380"
    save_json_to_file(contest)
    
