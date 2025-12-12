import sys
import os
# Add the parent directory to the path so we can import from main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *
if __name__ == "__main__":
    ps=paths.PathS()
    user=ps.users_path

    #抓取比赛数据
    # atcoder_contest.save_json_to_file("abc380",ps.atcoder_path_contest)
    codeforces_contest.save_json_to_file("2176",ps.codeforces_path_contest)
    # matiji_contest.save_json_to_file("296",ps.matiji_path_contest)
    # nowcoder_contest.save_json_to_file("122727",ps.nowcoder_path_contest)

    #读取比赛记录
    # type="atcoder"
    # contest="abc380"
    # users=atcoder_contest.atcoder_usrs(user)
    # format=[["Rank"],["UserName"]]
    # contest_path=ps.atcoder_path_contest
    
    type="codeforces"
    contest="2176"
    users=codeforces_contest.codeforces_usrs(user)
    format=[["rank"],["party", "members", 0, "handle"]]
    contest_path=ps.codeforces_path_contest

    # type="matiji"
    # contest="296"
    # users=matiji_contest.matiji_usrs(user)
    # print(users)
    # format=[["orderIndex"],["nickname"]]
    # contest_path=ps.matiji_path_contest

    # type="nowcoder"
    # contest="122727"
    # users=nowcoder_contest.nowcoder_usrs(user)
    # print(users)
    # format=[["ranking"],["userName"]]
    # contest_path=ps.nowcoder_path_contest

    records=saixuan.saixuan_contest_records(type,contest,users,format,contest_path)
    print(records)

    # 抓取用户
    # atcoderData.atcoder_gets(user,ps.atcoder_path_user)
    # codeforcesData.codeforces_gets(user,ps.codeforces_path_user)
    # matijiData.matiji_gets(user,ps.matiji_path_user)

    # # 地址列表生成
    # file_list_generator.generate_file_list_json(ps.root_path)
    # # 合并
    # data_converter.convert_data(ps.root_path,user,ps.out_path)