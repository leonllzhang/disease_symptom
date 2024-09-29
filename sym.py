import json
import pandas as pd
from collections import defaultdict

# 从文件中读取疾病数据
with open('medical.json', 'r', encoding='utf-8') as file:
    disease_list = json.load(file)

# 创建一个字典来存储症状之间的相关性
symptom_correlation = defaultdict(lambda: defaultdict(int))

# 遍历疾病数据并统计症状的相关性
for disease in disease_list:
    symptoms = disease.get('symptom', [])
    for i, symptom in enumerate(symptoms):
        for j, related_symptom in enumerate(symptoms):
            if i != j:  # 避免统计自身
                symptom_correlation[symptom][related_symptom] += 1

# 函数：输出所有症状及其相关症状和关联次数到文件
def save_symptom_correlations(correlation_dict, file_name='symptom_correlations.xlsx'):
    data = []
    for symptom, related_symptoms in correlation_dict.items():
        correlations = sorted(related_symptoms.items(), key=lambda x: x[1], reverse=True)
        for related, count in correlations:
            data.append({'症状': symptom, '相关症状': related, '关联次数': count})
    
    # 保存为 Excel 文件
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    
    # 保存为 JSON 文件（可选）
    with open('symptom_correlations.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 函数：获取与输入症状相关性最高的症状
def get_top_related_symptoms(input_symptom, correlation_dict, top_n=10):
    if input_symptom not in correlation_dict:
        return []

    # 获取与输入症状相关的症状及其次数
    related_symptoms = correlation_dict[input_symptom]

    # 按照次数从高到低排序，取出前 top_n 个症状
    sorted_related_symptoms = sorted(related_symptoms.items(), key=lambda x: x[1], reverse=True)

    return [(symptom, count) for symptom, count in sorted_related_symptoms[:top_n]]

# 保存相关性结果到文件
# save_symptom_correlations(symptom_correlation)

# 示例用户输入症状
input_symptom = '咳嗽'

# 获取与输入症状相关性最高的两到三个症状
top_related_symptoms = get_top_related_symptoms(input_symptom, symptom_correlation)

# 输出结果
if top_related_symptoms:
    result = ', '.join([f"{symptom}({count})" for symptom, count in top_related_symptoms])
    print(f"与症状 '{input_symptom}' 相关性最高的症状是: {result}")
else:
    print(f"未找到与症状 '{input_symptom}' 相关的症状")
