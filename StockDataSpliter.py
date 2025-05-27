import os
import pandas as pd
import json


def find_excel_files(folder_path):
    excel_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.xls', '.xlsx')):
                excel_files.append(os.path.join(root, file))
    return excel_files


def convert_excel_to_json(excel_file, output_folder):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(excel_file)

        # 筛选包含至少六个数值型且值非 NaN 的单元格的行
        filtered_rows = df[df.apply(lambda row: sum(
            [1 for cell in row if isinstance(cell, (int, float)) and not pd.isna(cell)]) > 6, axis=1)]

        # 查找包含关键字的行
        title_row = df[df.apply(lambda row: any(isinstance(cell, str) and any(
            keyword in cell for keyword in ["前收盘"]) for cell in row), axis=1)]

        # 构造输出文件路径
        base_name = os.path.basename(excel_file)
        base_name_no_ext = os.path.splitext(base_name)[0]

        # 保存包含关键字的行数据为 .title.json
        if not title_row.empty:
            title_data = title_row.to_dict(orient='records')
            title_output_path = os.path.join(output_folder, base_name_no_ext + '.title')
            with open(title_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(title_data, json_file, ensure_ascii=False, indent=4)
            print(f"成功转换: {excel_file} -> {title_output_path}")

        # 保存包含至少六个数值型且值非 NaN 的行数据为 .value.json
        if not filtered_rows.empty:
            value_data = filtered_rows.to_dict(orient='records')
            value_output_path = os.path.join(output_folder, base_name_no_ext + '.value')
            with open(value_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(value_data, json_file, ensure_ascii=False, indent=4)
            print(f"成功转换: {excel_file} -> {value_output_path}")

    except Exception as e:
        print(f"转换失败: {excel_file}, 错误: {e}")


# 示例用法
input_folder = r'E:\work_codes\Stock&Futures\上期所\原始数据'
output_folder = r'E:\stock_json'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

excel_files = find_excel_files(input_folder)
for excel_file in excel_files:
    convert_excel_to_json(excel_file, output_folder)
