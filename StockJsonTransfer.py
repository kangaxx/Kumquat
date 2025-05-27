import os
import json


def process_value_and_title_files(folder_path):
  # 遍历指定文件夹中的所有文件
  for file in os.listdir(folder_path):
    # 仅处理以 .value 结尾的文件
    if file.endswith(".value"):
      value_file_path = os.path.join(folder_path, file)  # 构造 .value 文件的完整路径
      title_file_path = os.path.join(folder_path, os.path.splitext(file)[
        0] + ".title")  # 构造对应 .title 文件的完整路径

      # 检查是否存在同名的 .title 文件
      if not os.path.exists(title_file_path):
        print(f"错误: 未找到同名的 .title 文件: {title_file_path}")
        continue

      try:
        # 读取 .title 文件并转换为 map
        with open(title_file_path, 'r', encoding='utf-8') as title_file:
          title_data = json.load(title_file)  # 加载 .title 文件的 JSON 数据
          if not isinstance(title_data, list) or not title_data:  # 检查数据是否为非空列表
            print(f".title 文件格式错误或为空: {title_file_path}")
            continue

        # 构造 title_map 列表
        title_map = []
        for item in title_data:
          if isinstance(item, dict):  # 确保每个元素是字典
            # 将字典的值按序号转换为键值对
            numeric_key_map = {str(index): value for index, value in
                               enumerate(item.values(), start=1)}
            title_map.append(numeric_key_map)

        # 打印 .title 文件的 map
        # print(json.dumps(title_map, ensure_ascii=False, indent=4))

        # 读取 .value 文件
        with open(value_file_path, 'r', encoding='utf-8') as value_file:
          value_data = json.load(value_file)  # 加载 .value 文件的 JSON 数据
          if not isinstance(value_data, list) or not value_data:  # 检查数据是否为非空列表
            print(f".value 文件格式错误或为空: {value_file_path}")
            continue

        # 将 .value 文件数据转换为 map 列表
        map_list = []
        for item in value_data:
          if isinstance(item, dict):  # 确保每个元素是字典
            # 将字典的值按序号转换为键值对
            numeric_key_map = {title_map[0].__getitem__(str(index)): value for
                               index, value in
                               enumerate(item.values(), start=1)}
            if "交易日期" in numeric_key_map:
              numeric_key_map["日期"] = numeric_key_map.pop("交易日期")
            map_list.append(numeric_key_map)

            # 打印 .value 文件的 map 列表
            # print(f"文件 {file} 的 .value map 列表:")
            # print(json.dumps(map_list, ensure_ascii=False, indent=4))


      except Exception as e:
        # 捕获并打印处理文件时的异常
        print(f"处理文件时出错: {file}, 错误: {e}")

      # 将 map_list 转换为 JSON 并存入 .finished 文件
      finished_file_path = os.path.join(folder_path,
                                        os.path.splitext(
                                          file)[
                                          0] + ".finished")
      with open(finished_file_path, 'w',
                encoding='utf-8') as finished_file:
        json.dump(map_list, finished_file, ensure_ascii=False,
                  indent=4)

      print(f"已生成文件: {finished_file_path}")
# 示例用法
folder_path = r"E:\stock_json"  # 指定文件夹路径
process_value_and_title_files(folder_path)  # 调用函数处理文件
