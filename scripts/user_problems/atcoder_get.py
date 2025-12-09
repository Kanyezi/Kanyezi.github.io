import requests
import json
import time
import datetime

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
    print(get_user_ac_count_api("tokyoww"))