import os
import json
import re
import time
import datetime
import requests

def get_user_ac_count_api(username):
    # AtCoderProblems API接口
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank?user={username}"

    try:
        # 发送GET请求
        response = requests.get(url)
        # 解析JSON响应
        resjson = response.json()
        res = resjson['count']
        return res
    
    except requests.exceptions.RequestException as e:
        return None

def atcoder_gets(user_path,problems_path):
    data = {}
    with open(user_path,'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(problems_path+str(datetime.date.today())+"_atcoder.json",'w', encoding='utf-8') as f:
        ru = {}
        for user in data:
            uname = user['name']
            uid = user['atcoder_id']
            if(uid==""):
                print(f"用户 {uname} id未写入")
                continue
            ac_count = get_user_ac_count_api(uid)
            ra = get_user_rating_api(uid)
            us={}
            if ac_count is not None:
                us['ac_count']=ac_count
                print(f"用户 {uname} \t 在AtCoder上AC的题目数量为:{ac_count}",end='')
            else:
                print(uname,"获取ac数据失败，请检查用户名或网络连接")
                continue

            if  ra is not None:
                rating = ra['rating']
                highest_rating = ra['highest_rating']
                us['rating']=rating
                us['highest_rating']=highest_rating
                print(f" \t 目前Rating为:{rating} \t 最高Rating为:{highest_rating}")
            else:
                print(f"\n{uname} \t 获取Rating数据失败，请检查用户名或网络连接")
            time.sleep(0.1)
            ru[uname]=us
        json.dump(ru,f)
def get_user_rating_api(username):
    # AtCoderProblems API接口
    url = f"https://atcoder.jp/users/{username}"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Cookie":"REVEL_SESSION=d152d00a2652f1652f7a6e5ac63a73f60a8b0f2d-%00UserScreenName%3Akanyezi%00%00UserName%3Akanyezi%00%00a%3Afalse%00%00w%3Afalse%00%00_TS%3A1779295763%00%00csrf_token%3A6M28Q8oit3d8V%2F87OvUU95Zp9nEtNCLC4WZ7CMET1zo%3D%00%00SessionKey%3A24276a9c6fceaea27ad7f3f8662c0379f24cf07a24ca0ded44272837a9b74a87%00; _ga_RC512FD18N=GS2.1.s1763743306$o7$g1$t1763743764$j58$l0$h0; _ga=GA1.1.1842048823.1762102707; REVEL_FLASH=; timeDelta=-364; OJB_Session_ojb_updateL10nWebsiteJson_zh=true"
    }

    try:
        # 发送GET请求
        response = requests.get(url=url,headers=headers)
        # 解析JSON响应
        resjson = response.text
        # resjson="""
        # <table class="dl-table mt-2">
        #                                         <tr><th class="no-break">Rank</th><td>22640th</td></tr>
        #                                         <tr><th class="no-break">Rating</th><td><img src="//img.atcoder.jp/assets/user/user-brown-4.png" class="user-rating-stage-m"><span class='user-brown'>718</span>
        #                                                 </td></tr>
        #                                         <tr><th class="no-break">Highest Rating</th><td><img src="//img.atcoder.jp/assets/user/user-brown-4.png" class="user-rating-stage-m"><span class='user-brown'>758</span>
        #                                                 <span class="gray">―</span>
        #                                                 <span class="bold">7 Kyu</span>

        #                                                         <span class="gray">(&#43;42 to promote)</span>

        #                                         </td></tr>
        #                                         <tr><th class="no-break">Rated Matches <span class='glyphicon glyphicon-question-sign' aria-hidden='true' data-html='true' data-toggle='tooltip' title="Counts only rated contests"></span></th><td>26</td></tr>
        #                                         <tr><th class="no-break">Last Competed</th><td>2025/08/16</td></tr>
        #                                 </table>
        # """
        #rating,highest_rating
        rating = re.search(r'Rating</th><td>.*?</td></tr>', resjson, re.DOTALL)
        rating = re.search(r'<span .*?>.*?</span>', rating.group(0), re.DOTALL)
        rating = re.search(r'>.*?<', rating.group(0), re.DOTALL)
        rating = rating.group(0)[1:-1]
        highest_rating = re.search(r'Highest Rating</th><td>.*?</td></tr>', resjson, re.DOTALL)
        highest_rating = re.search(r'<span .*?>.*?</span>', highest_rating.group(0), re.DOTALL)
        highest_rating = re.search(r'>.*?<', highest_rating.group(0), re.DOTALL)
        highest_rating = highest_rating.group(0)[1:-1]
        # print(rating,highest_rating)
        data={
            "rating":rating,
            "highest_rating":highest_rating
        }
        # if rating and highest_rating:
        # res = resjson['rating']
        return data
    
    except Exception as e:
        return None
# 使用示例
if __name__ == "__main__":
    # print(get_user_ac_count_api("tokyoww"))
    # data=get_user_rating_api("ykkkk")
    # print(data)
    atcoder_gets()