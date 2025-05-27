# -*- coding: utf-8 -*-
# @Time    : 2023/10/8 16:00
# @Author  : 顾欣欣
# @File    : StockFileTotallyProcess.py
# @Software: PyCharm
# @Description: 该脚本用于上期所原始数据，主要包括以下步骤：
# 1. 拆分Excel文件并生成json文件
# 2. 转换json文件中的字段
# 3. 处理临时文件
# 4. 合并文件
# @Version : 1.0

import StockDataSpliter
import StockJsonTransfer
import StockTempFile
import StockCombineFile

if __name__ == "__main__":
    # 1. 拆分Excel并生成json
    print("正在拆分Excel文件...")
    StockDataSpliter.main()  # 假设你将示例用法部分封装为main()

    # 2. 转换json字段
    print("正在转换json字段...")
    StockJsonTransfer.process_value_and_title_files(r"E:\stock_json")

    # 3. 处理临时文件
    print("正在处理临时文件...")
    StockTempFile.main()  # 假设有main函数

    # 4. 合并文件
    print("正在合并文件...")
    StockCombineFile.main()  # 假设有main函数

    print("全部处理完成。")
