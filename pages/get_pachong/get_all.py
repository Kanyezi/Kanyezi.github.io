import atcoderData,codeforcesData,matijiData
import data_converter,file_list_generator

if __name__ == "__main__":
    # 抓取
    atcoderData.atcoder_gets()
    codeforcesData.codeforces_gets()
    matijiData.matiji_gets()
    # 合并
    data_converter.data_convert()
    # 地址列表生成
    file_list_generator.generate_file_list()