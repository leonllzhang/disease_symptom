import json
import re

# 从文件中读取疾病数据
with open('medical.json', 'r', encoding='utf-8') as file:
    disease_list = json.load(file)

# 清洗 get_prob 字段，只保留百分比
def process_get_prob(disease_list):
    for disease in disease_list:
        if 'get_prob' in disease and isinstance(disease['get_prob'], str):
            # 使用正则表达式从 get_prob 中提取数字部分
            match = re.search(r'(\d+(\.\d+)?)%', disease['get_prob'])
            if match:
                # 将百分比字符串转换为小数
                disease['get_prob'] = float(match.group(1)) / 100
            else:
                # 如果没有匹配到百分比，则设置为 0
                disease['get_prob'] = 0.0
        else:
            # 如果没有 get_prob 字段，或者字段不是字符串类型，则设置为 0
            disease['get_prob'] = 0.0


# 处理疾病数据，提取百分比
process_get_prob(disease_list)


# 过滤包含特定科室的疾病
def filter_by_department(disease_list, department):
    return [
        disease for disease in disease_list
        if any(department in dept for dept in disease.get('cure_department', []))
    ]

# 根据症状匹配疾病
def match_diseases_by_symptoms(symptoms, diseases):
    matched = [d for d in diseases if any(symptom in d.get('symptom', []) for symptom in symptoms)]
    matched.sort(key=lambda x: x['get_prob'], reverse=True)
    return matched

# 进行疾病分析
def analyze_symptoms(user_symptoms,  filtered_diseases ):
    # 初步匹配疾病
    matched_diseases = match_diseases_by_symptoms(user_symptoms, filtered_diseases)

    analysis_results = []  # 存放分析结果的列表
    analysis_limit = 2     # 最多两个分析过程

    # 分析疾病，提供独特症状选项
    for _ in range(analysis_limit):  # 重复两次分析过程
        unique_symptoms = set()
        for disease in matched_diseases:
            unique = set(disease.get('symptom', [])) - set(symptom for d in matched_diseases if d != disease for symptom in d.get('symptom', []))
            unique_symptoms.update(unique)

        # 如果有独特症状，提示用户选择
        if unique_symptoms:
            print(f"您是否有以下症状中的任何一个？ {', '.join(unique_symptoms)}")
            additional_symptom = input("请输入症状（或按 Enter 跳过）：")
            if additional_symptom:
                matched_diseases = match_diseases_by_symptoms([additional_symptom], matched_diseases)
            else:
                break
        else:
            break
    
     # 输出最终结果
    result = [{
        '用户输入': user_symptoms,
        '疾病名': disease['name'],
        '疾病症状': disease['symptom'],
        '疾病描述': disease['desc']
    } for disease in matched_diseases]

    print("最终匹配的疾病：")
    for r in result:
        print(json.dumps(r, ensure_ascii=False, indent=2)) 

# 示例用户输入
# user_symptoms = ['胸痛', '咳嗽']

# 科室类别
department = '肿瘤'

# 过滤出特定科室的疾病
filtered_diseases = filter_by_department(disease_list, department)

# 提示用户输入症状
user_input = input("请输入您的症状（多个症状用空格分隔）：")
user_symptoms = user_input.split()


# 进行疾病分析并输出结果
results = analyze_symptoms(user_symptoms, filtered_diseases)


