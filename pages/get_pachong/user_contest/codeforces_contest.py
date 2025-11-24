import requests
import json
import os

def get_codeforces_contest_standing(contest):
    url = f"https://codeforces.com/api/contest.standings?contestId={contest}"

    try:
        response = requests.get(url)
        data=response.json()
        if data.get('status') != 'OK':
            print(f"Codeforces API返回错误: {data.get('comment', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Codeforces网络请求错误: {e}")
        return None
    except Exception as e:
        print(f"Codeforces处理过程中发生错误: {e}")
        return None
    return data
def save_json_to_file(contests):
    standing = get_codeforces_contest_standing(contests)

    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(current_dir)
    path_r = os.path.join(current_dir,"./public/data.json")
    # print(path_r)
    path_w = os.path.join(current_dir,"../public/contest/codeforces")
    # print(path_w)
    with open(path_w+f"/{contests}.json",'w', encoding='utf-8') as f:
        json.dump(standing, f, ensure_ascii=False, indent=4)
        print(f"codeforces排名数据已保存到{contests}.json")
def read_json(contest):
    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path_w = os.path.join(current_dir,"../public/contest/codeforces")
    with open(path_w+f"/{contest}.json",'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
if __name__ == "__main__":
    # 测试codeforces排名获取
    contests = "2126"
    standing = save_json_to_file(contests)
    # standing = {"测试": "test"}
    # print(standing)
