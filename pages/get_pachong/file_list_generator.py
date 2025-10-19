import os
import json

# 定义项目根目录和目标文件夹路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
TARGET_FOLDERS = ['atcoder', 'codeforces', 'matiji']


def get_file_list(folder_path):
    """
    获取指定文件夹下的所有文件名（不包含子文件夹）
    """
    try:
        # 获取文件夹中的所有项目
        items = os.listdir(folder_path)
        # 过滤出文件（排除文件夹）并返回文件名列表
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
        return sorted(files)  # 返回排序后的文件列表
    except Exception as e:
        print(f"读取文件夹 {folder_path} 时出错: {e}")
        return []


def generate_file_list_json():
    """
    生成文件列表JSON并保存到public目录
    """
    # 创建结果字典
    file_list_data = {}
    
    # 遍历每个目标文件夹
    for folder_name in TARGET_FOLDERS:
        folder_path = os.path.join(PUBLIC_DIR, folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            file_list_data[folder_name] = get_file_list(folder_path)
        else:
            print(f"文件夹 {folder_path} 不存在或不是有效目录")
            file_list_data[folder_name] = []
    
    # 保存结果到JSON文件
    output_file = os.path.join(PUBLIC_DIR, 'file_list.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(file_list_data, f, ensure_ascii=False, indent=2)
        print(f"文件列表已成功保存到 {output_file}")
        return True
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")
        return False


if __name__ == "__main__":
    generate_file_list_json()