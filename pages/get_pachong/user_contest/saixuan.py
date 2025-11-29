try:
    from . import atcoder_contest
    from . import codeforces_contest
    from . import matiji_contest
    from . import nowcoder_contest
except ImportError:
    import atcoder_contest
    import codeforces_contest
    import matiji_contest
    import nowcoder_contest
#筛选比赛数据
def read_contest_records(type,contest,contest_path):
    if(type=="atcoder"):
        data=atcoder_contest.read_json(contest,contest_path)
        return data['StandingsData']
    elif(type=="codeforces"):
        data=codeforces_contest.read_json(contest,contest_path)
        return data['result']['rows']
    elif(type=="matiji"):
        data=matiji_contest.read_json(contest,contest_path)
        return data['data']['datas']
    elif(type=="nowcoder"):
        data=nowcoder_contest.read_json(contest,contest_path)
        return data['data']['rankData']
    return None
def check(type,record,users):
    name = ""
    if(type=="atcoder"):
        name=record["UserName"]
    elif(type=="codeforces"):
        name=record["party"]["members"][0]["handle"]
    elif(type=="matiji"):
        name=record["userId"]
    elif(type=="nowcoder"):
        name=record["uid"]
    name=str(name)
    # print(users,end='')
    if(name in users):
        # print("找到用户："+name)
        return users[name]["name"]
    return False
    
def saixuan_contest_records(type,contest,users,paths,contest_path):
    result = []
    data=read_contest_records(type,contest,contest_path)
    
    for record in data:
        # print(record["userId"])
        if check(type,record,users):
            name=check(type,record,users)
            user=[name]
            for path in paths:
                current = record
                for key in path:
                    current = current[key]
                user.append(current)
            result.append(user)
    return result
if __name__ == "__main__":
    type="atcoder"
    contest="abc380"
    users={"ykkkk","x_yeyue","ziying032"}
    format=[["Rank"],["UserName"]]
    
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

    records=saixuan_contest_records(type,contest,users,format)
    print(records)