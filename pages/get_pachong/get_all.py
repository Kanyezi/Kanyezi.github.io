from user_problems import atcoderData,codeforcesData,matijiData
import data_converter,file_list_generator
import paths

if __name__ == "__main__":
    ps=paths.PathS()

    user=ps.users_path
    # 抓取
    atcoderData.atcoder_gets(user,ps.atcoder_path_contest)
    # codeforcesData.codeforces_gets()
    # matijiData.matiji_gets()
    # # 地址列表生成
    # file_list_generator.generate_file_list()
    # # 合并
    # data_converter.data_convert()