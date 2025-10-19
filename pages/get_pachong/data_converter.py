import json
import os
import re
from datetime import datetime

# 文件路径定义
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
DATA_JSON_PATH = os.path.join(PUBLIC_DIR, 'data.json')
ALL_DATA_PATH = os.path.join(PUBLIC_DIR, 'all_data.json')

# 平台目录映射
PLATFORM_DIRS = {
    'atcoder': os.path.join(PUBLIC_DIR, 'atcoder'),
    'codeforces': os.path.join(PUBLIC_DIR, 'codeforces'),
    'matiji': os.path.join(PUBLIC_DIR, 'matiji')
}

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载文件 {file_path} 失败: {e}")
        return None

def extract_date_from_filename(filename):
    """从文件名中提取日期"""
    # 匹配形如 YYYY-MM-DD 或 YYYY-M-DD 的日期格式
    match = re.match(r'(\d{4})[-_](\d{1,2})[-_](\d{1,2})', filename)
    if match:
        year, month, day = match.groups()
        # 返回格式：YYYY-MM-DD 或 YYYY-M-DD（保留原始格式）
        return f"{year}-{month}-{day}"
    return None

def convert_data():
    """转换数据并生成all_data.json，读取所有数据文件并按日期组织"""
    print("开始转换数据...")
    
    # 1. 读取各平台的所有数据文件
    platform_date_data = {
        'atcoder': {},
        'codeforces': {},
        'matiji': {}
    }
    
    total_files = 0
    for platform, dir_path in PLATFORM_DIRS.items():
        if not os.path.exists(dir_path):
            print(f"目录不存在: {dir_path}")
            continue
        
        # 获取目录中的所有JSON文件
        for filename in os.listdir(dir_path):
            if filename.endswith('.json'):
                file_path = os.path.join(dir_path, filename)
                # 提取日期
                date_str = extract_date_from_filename(filename)
                if not date_str:
                    print(f"无法从文件名提取日期: {filename}")
                    continue
                
                # 加载文件数据
                data = load_json_file(file_path)
                if data:
                    if date_str not in platform_date_data[platform]:
                        platform_date_data[platform][date_str] = {}
                    
                    # 将当前文件的数据合并到对应日期
                    for username, value in data.items():
                        platform_date_data[platform][date_str][username] = value
                    
                    print(f"读取到{platform}数据: {filename}，日期: {date_str}")
                    total_files += 1
    
    print(f"总共读取了 {total_files} 个数据文件")
    
    # 2. 读取data.json
    students = load_json_file(DATA_JSON_PATH)
    if not students:
        print("无法读取data.json")
        return False
    print(f"读取到学生数据，共{len(students)}名学生")
    
    # 3. 构建all_data.json格式的数据
    all_data = {
        'users': [],
        'data': {},
        'lastUpdate': datetime.now().isoformat()
    }
    
    # 处理users数组和data对象
    for student in students:
        name = student['name']
        
        # 计算各平台所有日期的总和
        sum_atcoder = 0
        sum_codeforces = 0
        sum_matiji = 0
        
        # 遍历各平台的所有日期数据并求和
        for platform in ['atcoder', 'codeforces', 'matiji']:
            for date_str, date_data in platform_date_data[platform].items():
                if name in date_data:
                    if platform == 'atcoder':
                        sum_atcoder += date_data[name]
                    elif platform == 'codeforces':
                        sum_codeforces += date_data[name]
                    elif platform == 'matiji':
                        sum_matiji += date_data[name]
        
        # 构建用户数据
        user_data = {
            **student,
            'atcoder': sum_atcoder,
            'codeforces': sum_codeforces,
            'matiji': sum_matiji
        }
        # 移除可能存在的total字段
        if 'total' in user_data:
            del user_data['total']
        
        all_data['users'].append(user_data)
        
        # 初始化data对象中的结构，按日期组织数据
        all_data['data'][name] = {
            'atcoder': {},
            'codeforces': {},
            'matiji': {}
        }
        
        # 填充各平台按日期组织的数据
        for platform in ['atcoder', 'codeforces', 'matiji']:
            for date_str, date_data in platform_date_data[platform].items():
                if name in date_data:
                    all_data['data'][name][platform][date_str] = date_data[name]
        
    print("数据转换完成")
    
    # 4. 保存到all_data.json
    try:
        with open(ALL_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"数据已成功保存到: {ALL_DATA_PATH}")
        return True
    except Exception as e:
        print(f"保存all_data.json失败: {e}")
        return False

if __name__ == "__main__":
    success = convert_data()
    if success:
        print("数据转换任务完成！")
    else:
        print("数据转换任务失败！")