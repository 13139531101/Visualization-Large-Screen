import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('香港各区疫情数据_20250322.xlsx')

# 获取所有日期
dates = df['报告日期'].unique().tolist()
dates = [str(date) for date in dates]

# 获取所有区域名称
districts = df['地区名称'].unique().tolist()

# 计算每日新增确诊
daily_new = df.groupby('报告日期')['新增确诊'].sum().tolist()

# 计算累计确诊
total_confirmed = []
cumulative = 0
for day in daily_new:
    cumulative += day
    total_confirmed.append(cumulative)

# 计算增长率
growth_rate = []
for i in range(1, len(total_confirmed)):
    if total_confirmed[i-1] == 0:
        growth_rate.append(0)
    else:
        rate = ((total_confirmed[i] - total_confirmed[i-1]) / total_confirmed[i-1]) * 100
        growth_rate.append(round(rate, 2))

# 计算各区确诊数据
district_cases = []
district_percent = []
for district in districts:
    district_data = df[df['地区名称'] == district]
    district_cases.append(district_data['累计确诊'].iloc[-1])
    district_percent.append(round((district_data['累计确诊'].iloc[-1] / total_confirmed[-1]) * 100, 2))

# 生成热点区域列表
hotspots = [districts[i] for i, cases in enumerate(district_cases) if cases > 200]

# 构建JSON数据
output_data = {
    "dates": dates,
    "dailyNew": [int(x) for x in daily_new],
    "totalConfirmed": [int(x) for x in total_confirmed],
    "growthRate": growth_rate,
    "hotspots": hotspots,
    "districts": districts,
    "districtCases": [int(x) for x in district_cases],
    "districtPercent": district_percent
}

# 保存为JSON文件
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("数据已成功转换为JSON格式并保存为data.json")