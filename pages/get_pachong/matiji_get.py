import requests
import time
import random

list=[
    ""
#     "218118",
# "217005",
# "217113",
# "218083",
# "151967",
# "218264",
# "",
# "216994",
# "217815",
# "218127",
# "218207",
# "",
# "217113",
# "216968",
# "217859",
# "",
# "217855",
# "",
# "218193",
# "",
# "217035",
# "217485",
# "122691",
# "217489",
# "217991",
# "218204",

]

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

if __name__ == "__main__":
    print(get_user_ac_count(167506))