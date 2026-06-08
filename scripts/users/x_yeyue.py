import sys
import os
# Add the parent directory to the path so we can import from main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *
if __name__ == "__main__":
    ps=paths.PathS()
    user=ps.users_path
    
    # print(atcoder_contest.atcoder_usrs(user))
    #抓取比赛数据
    # atcoder_contest.save_json_to_file("abc457",ps.atcoder_path_contest)
    codeforces_contest.save_json_to_file("2208",ps.codeforces_path_contest)
    # matiji_contest.save_json_to_file("296",ps.matiji_path_contest)
    # nowcoder_contest.save_json_to_file("122727",ps.nowcoder_path_contest)

    #读取比赛记录
    # type="atcoder"
    # contest="abc457"
    # users=atcoder_contest.atcoder_usrs(user)
    # format=[["Rank"],["UserName"]]
    # contest_path=ps.atcoder_path_contest
    
    type="codeforces"
    contest="2208"
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
    
    person_of_charges = ['尚淇淇', '符轩跃', '杜光明', '陈光照']
    person_of_charge = []
    print("name list : ")
    if(len(records) == 0):
        print("empty!!!")
    else:
        for it in records:
            print(it[0], end=',')
            if(it[0] in person_of_charges):
                person_of_charge.append(it[0])
    print()
    print(f"count of person: {len(records)}")
    print(f"person of charge: {person_of_charge}")
    