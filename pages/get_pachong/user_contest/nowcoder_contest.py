import requests
import json
import os
import time
def get_nowcoder_contest_standing(contest,page):
    url=f"https://ac.nowcoder.com/acm-heavy/acm/contest/real-time-rank-data?token=&id={contest}&limit=0&page={page}"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Cookie":"NOWCODERUID=ba63651f9cf540cbb8845e9b7ced2971; NOWCODERCLINETID=693376EE442C8C584F225833621AD934; gr_user_id=8f5f6d84-ad02-4db0-9d40-bdbb33eed80f; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1762424861,1763741878; t=02FFD6D77986B4F4DD8F81B2C9EAE39B; c196c3667d214851b11233f5c17f99d5_gr_last_sent_cs1=684165880; acw_tc=0a03832c17637418768978811e6d63a6b21dc3f5d869bc1712cae577440fdd; c196c3667d214851b11233f5c17f99d5_gr_session_id=8f3b1d33-8d11-4bbe-b75a-9d7e1a8d2360; c196c3667d214851b11233f5c17f99d5_gr_session_id_sent_vst=8f3b1d33-8d11-4bbe-b75a-9d7e1a8d2360; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1763741878; HMACCOUNT=E76CECFB1268760C"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"NowCoder请求失败，状态码：{response.status_code}")
            return None
        data = response.json()
        # print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"NowCoder网络请求错误: {e}")
        return None
    except Exception as e:
        print(f"NowCoder处理过程中发生错误: {e}")
        return None
def get_nowcoder_contest_standings(contest):
    data=get_nowcoder_contest_standing(contest,1)
    page=2
    last=data
    while True:
        print(len(data['data']['rankData']))
        print(f"NowCoder正在获取第{page}页数据")
        standing = get_nowcoder_contest_standing(contest,page)
        if standing is None:
            break
        if standing['data']['rankData']==last['data']['rankData']:
            break
        last=standing
        data['data']['rankData'].extend(standing['data']['rankData'])
        page+=1
        time.sleep(0.3)
    return data
def save_json_to_file(contest):
    standing = get_nowcoder_contest_standings(contest)

    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(current_dir)
    path_r = os.path.join(current_dir,"./public/data.json")
    # print(path_r)
    path_w = os.path.join(current_dir,"../public/contest/nowcoder")
    # print(path_w)
    with open(path_w+f"/{contest}.json",'w', encoding='utf-8') as f:
        json.dump(standing, f, ensure_ascii=False, indent=4)
        print(f"NowCoder排名数据已保存到{contest}.json")
def read_json(contest):
    current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path_w = os.path.join(current_dir,"../public/contest/nowcoder")
    with open(path_w+f"/{contest}.json",'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
if __name__ == "__main__":
    contest = "122727"
    save_json_to_file(contest)