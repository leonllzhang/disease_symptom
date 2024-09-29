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



# 进行疾病分析
def analyze_symptoms(user_symptoms,  filtered_diseases ):
    # 根据症状，按得病概率从高到低排序
    sorted_diseases = sorted(filtered_diseases, key=lambda x: x['get_prob'], reverse=True)

    analysis_results = []  # 存放分析结果的列表
    analysis_limit = 2     # 最多两个分析过程

    for disease in sorted_diseases:
        if analysis_limit == 0:
            break

        # 检查用户的症状是否与疾病的症状字段匹配
        matched_symptoms = [symptom for symptom in user_symptoms if symptom in disease['symptom']]
        
        if matched_symptoms:
            # 获取未输入的症状作为提示选项
            additional_symptoms = [symptom for symptom in disease['symptom'] if symptom not in user_symptoms]
            
            if additional_symptoms:
                # 询问用户是否有这些症状
                print(f"对于疾病 {disease['name']}，你有以下症状吗？: {', '.join(additional_symptoms)}")
                user_response = input("请输入 '是' 或 '否': ")

                if user_response == '是':
                    # 完成当前疾病分析过程
                    analysis_results.append({
                        '用户输入': user_symptoms,
                        '疾病名': disease['name'],
                        '疾病症状': disease['symptom'],
                        '疾病描述': disease['desc']
                    })
                    analysis_limit -= 1
            else:
                # 如果没有其他症状需要询问，直接记录分析结果
                analysis_results.append({
                    '用户输入': user_symptoms,
                    '疾病名': disease['name'],
                    '疾病症状': disease['symptom'],
                    '疾病描述': disease['desc']
                })
                analysis_limit -= 1

    return analysis_results

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

for result in results:
    print(f'********************************************8')
    print(f"用户输入: {result['用户输入']}")
    print(f"疾病名: {result['疾病名']}")
    print(f"疾病症状: {result['疾病症状']}")
    print(f"疾病描述: {result['疾病描述']}")
    print()
