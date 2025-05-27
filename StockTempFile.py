import os
import json


def is_nan(obj):
  """检查对象是否为NaN（仅适用于数值类型）"""
  return isinstance(obj, float) and obj != obj  # NaN是唯一不等于自身的值
def fill_contract_and_save(folder_path):
    """
    遍历指定文件夹，执行以下操作：
    1. 删除所有后缀为 .temp 的文件。
    2. 遍历所有后缀为 .finished 的文件，读取其 JSON 数据。
    3. 将 JSON 数据中 "合约" 字段值为空或为 "nan" 的项替换为前一个非空值。
    4. 将处理后的数据保存为同名但后缀为 .temp 的文件。

    Args:
        folder_path (str): 文件夹路径，包含 .temp 和 .finished 文件。
    """
    # 删除所有 .temp 文件
    for file in os.listdir(folder_path):
        if file.endswith('.temp'):
            temp_path = os.path.join(folder_path, file)
            try:
                os.remove(temp_path)
                print(f"已删除: {temp_path}")
            except Exception as e:
                print(f"删除{temp_path}失败: {e}")

    # 处理 .finished 文件
    for file in os.listdir(folder_path):
        if file.endswith('.finished'):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    # 读取 JSON 数据
                    data = json.load(f)
                except Exception as e:
                    print(f"文件{file}读取失败: {e}")
                    continue

            # 替换 "合约" 字段为空或为 "nan" 的值
            last_contract = None
            for item in data:
                contract = item.get("合约")
                if is_nan(contract):
                    item["合约"] = last_contract
                else:
                    last_contract = contract

            # 保存处理后的数据为 .temp 文件
            new_file = os.path.splitext(file)[0] + '.temp'
            new_path = os.path.join(folder_path, new_file)
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            # print(f"已保存: {new_path}")

# 示例用法
folder_path = r"E:\stock_json"
fill_contract_and_save(folder_path)
