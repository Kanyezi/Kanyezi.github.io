import requests
import json
import os

def codeforces_usrs(user_path):
    list = {}
    with open(user_path,'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            list[item['codeforces_id']]={"name":item['name']}
    return list
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
def save_json_to_file(contests,contest_path):
    standing = get_codeforces_contest_standing(contests)
    if standing is None:
        print(f"Codeforces数据获取失败，未保存{contests}.json")
        return
    with open(contest_path+f"/{contests}.json",'w', encoding='utf-8') as f:
        json.dump(standing, f, ensure_ascii=False, indent=4)
        print(f"codeforces排名数据已保存到{contests}.json")
def read_json(contest,contest_path):
    filepath = contest_path+f"/{contest}.json"
    if not os.path.exists(filepath):
        print(f"Codeforces数据文件不存在: {filepath}")
        return None
    with open(filepath,'r', encoding='utf-8') as f:
        data = json.load(f)
    if data is None:
        print(f"Codeforces数据文件内容为null: {filepath}，需要重新获取")
        return None
    return data
if __name__ == "__main__":
    # 测试codeforces排名获取
    contests = "2126"
    standing = save_json_to_file(contests)
    # standing = {"测试": "test"}
    # print(standing)
