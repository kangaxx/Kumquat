import os
import json

def group_by_contract_and_save(folder_path):
    """
    遍历指定文件夹下所有 .temp 文件，按 "合约" 字段归类数据，
    并将每类数据写入以合约名为文件名的 .json 文件。
    """
    contract_map = {}

    # 遍历所有 .temp 文件
    for file in os.listdir(folder_path):
        if file.endswith('.temp'):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"读取失败: {file}, 错误: {e}")
                continue

            for item in data:
                contract = item.get("合约")
                if not contract:
                    continue
                safe_contract = str(contract).replace('/', '_').replace('\\', '_')
                contract_map.setdefault(safe_contract, []).append(item)

    # 写入分组后的 .json 文件
    for contract, items in contract_map.items():
        out_path = os.path.join(folder_path, f"{contract}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        print(f"已写入: {out_path}")
    # 删除所有 .temp 文件
    for file in os.listdir(folder_path):
        if file.endswith('.temp'):
            temp_path = os.path.join(folder_path, file)
            try:
                os.remove(temp_path)
                print(f"已删除: {temp_path}")
            except Exception as e:
                print(f"删除{temp_path}失败: {e}")
# 示例用法
folder_path = r"E:\stock_json"
group_by_contract_and_save(folder_path)
