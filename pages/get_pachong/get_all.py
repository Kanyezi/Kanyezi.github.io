from user_problems import atcoderData,codeforcesData,matijiData
from user_contest import atcoder_contest,codeforces_contest,matiji_contest,nowcoder_contest,saixuan
import data_converter,file_list_generator
import paths

if __name__ == "__main__":
    ps=paths.PathS()

    user=ps.users_path
    #抓取比赛数据
    atcoder_contest.save_json_to_file("abc380",ps.atcoder_path_contest)
    # codeforces_contest.save_json_to_file("2126",ps.codeforces_path_contest)
    # matiji_contest.save_json_to_file("296",ps.matiji_path_contest)
    # nowcoder_contest.save_json_to_file("122727",ps.nowcoder_path_contest)

    #读取比赛记录
    # type="atcoder"
    # contest="abc380"
    # users={"ykkkk","x_yeyue","ziying032"}
    # format=[["Rank"],["UserName"]]
    
    # type="codeforces"
    # contest="2126"
    # users={"Gai_yk","x_yeyue"}
    # format=[["rank"],["party", "members", 0, "handle"]]

    # type="matiji"
    # contest="296"
    # users={"185244","111198"}
    # format=[["orderIndex"],["nickname"]]

    # type="nowcoder"
    # contest="122727"
    # users={"738977420","795955061"}
    # format=[["ranking"],["userName"]]

    # records=saixuan.saixuan_contest_records(type,contest,users,format)
    # print(records)


    # 抓取用户ac题目数

    # atcoderData.atcoder_gets(user,ps.atcoder_path_user)
    # codeforcesData.codeforces_gets(user,ps.codeforces_path_user)
    # matijiData.matiji_gets(user,ps.matiji_path_user)

    # # 地址列表生成
    # file_list_generator.generate_file_list()
    # # 合并
    # data_converter.data_convert()