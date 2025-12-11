import sys
import os
# Add the parent directory to the path so we can import from main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *
if __name__ == "__main__":
    ps=paths.PathS()
    user=ps.users_path


    # 抓取用户ac题目数

    # atcoderData.atcoder_gets(user,ps.atcoder_path_user)
    # codeforcesData.codeforces_gets(user,ps.codeforces_path_user)
    matijiData.matiji_gets(user,ps.matiji_path_user)

    # # 地址列表生成
    file_list_generator.generate_file_list_json(ps.root_path)
    # # 合并
    data_converter.convert_data(ps.root_path,user,ps.out_path)