import requests
import json
import time
import datetime

# user = {
#     "孙叶":	    "chu4351",
#     "陈宣扬":	"cxy2006",
#     "杜光明":	"ruanmei",
#     "陈光照":	"MysterService",
#     "刘意群":	"liuning123",
#     "陈轩宇":	"kilty",
#     "胡悠茗":	"breadog",
#     "施宇轩":	"zhouxian",
#     "巫浩锋":	"Kyrie_11",
#     "连全威":	"Koijia",
#     "张宇翔":	"OOZYXOO",
#     "周晓飞":	"hei_di",
#     "刘云琪":	"tokyoww",
#     "吴春雷":	"wuchunlei",
#     "叶宇喆":	"gdyg666",
#     "王佳欣":	"lushishen",
#     "王西门":	"gggsss",
#     "燕诺":	    "Ywy1126",
#     "郑亦宇":	"zhengyiyu",
#     "徐文静":	"yesswlqbjs",
#     "符轩跃": 	"fuxuanyue",
#     "刘筱朵":	"lxd_",
#     "倪志杰":	"Ardmore"
# }
def get_user_ac_count_api(username):
    """
    使用AtCoderProblems API获取用户AC题目数量
    :param username: AtCoder用户名
    :return: AC题目数量（整数），失败返回None
    """
    # AtCoderProblems API接口
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank?user={username}"

    try:
        # 发送GET请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code != 200:
            print(f"API请求失败，状态码：{response.status_code}")
            return None
        
        # 解析JSON响应
        resjson = response.json()
        res = resjson['count']
        return res
    
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        return None
if __name__ == "__main__":
    print(get_user_ac_count_api("ykkkk"))