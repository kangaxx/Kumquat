import pandas as pd
from enum import Enum
import math

class ProcessType(Enum):
    NO_PROCESS = (0, "不做任何处理")
    ZEN_INCLUDE = (1, "缠中论禅")

    def __init__(self, value, desc):
        self._value_ = value
        self.desc = desc


def process_json_file(filename: str, process_type: ProcessType):
    df = pd.read_json(filename)
    if process_type == ProcessType.NO_PROCESS:
        return df
    elif process_type == ProcessType.ZEN_INCLUDE:
        return zen_include_process(df)
    else:
        raise ValueError("未知的处理类型")

    # 这里实现K线缠论的数据合并操作


def zen_include_process(df: pd.DataFrame):
    df = df.copy().reset_index(drop=True)
    #步骤1 ：合并包含关系的K线
    i = 1
    max_high = float('inf')  # 如果有连续包含，需要更新最大值时，找出最小的那个最大值
    min_low = float('-inf')  # 如果有连续包含，需要更新最小值时，找出最大的那个最小值
    while i < len(df):
        try:
            cur_high = float(df.at[i, "最高价"])
            cur_low = float(df.at[i, "最低价"])
        except Exception:
            print(f"第{i}行最高价或最低价无法转换为浮点数，已删除")
            df = df.drop(i).reset_index(drop=True)
            continue
        # 检查无效浮点数（包括nan、inf、-inf）
        if (math.isnan(cur_high) or math.isnan(cur_low) or
            math.isinf(cur_high) or math.isinf(cur_low)):
            print(f"第{i}行最高价或最低价无效（nan/inf），已删除")
            df = df.drop(i).reset_index(drop=True)
            continue
        # 打印调试信息
        print(
            f"第{i}行: 日期={df.at[i, '日期'] if '日期' in df.columns else '无'}, "
            f"最高价={df.at[i, '最高价']}, 最低价={df.at[i, '最低价']}, "
            f"开盘价={df.at[i, '开盘价']}, 收盘价={df.at[i, '收盘价']}"
        )
        cur_high = float(df.at[i, "最高价"])
        cur_low = float(df.at[i, "最低价"])
        pre_high = float(df.at[i - 1, "最高价"])
        pre_low = float(df.at[i - 1, "最低价"])
        # 包含关系判断
        if cur_high > pre_high and cur_low < pre_low:
            # 打印包含关系
            print(f"包含关系: 当前行({cur_high}, {cur_low}) 包含 前一行({pre_high}, {pre_low})")
            if pre_low > min_low:
                min_low = pre_low
            if pre_high < max_high:
                max_high = pre_high
            # 需要有前一条的前一条
            if i - 2 >= 0:
                pre2_high = float(df.at[i - 2, "最高价"])
                pre2_low = float(df.at[i - 2, "最低价"])
                if cur_high < pre2_high or cur_low > pre2_low:
                    if cur_high > pre2_high:
                        df.at[i, "最低价"] = min_low
                    else:
                        df.at[i, "最高价"] = max_high
            # 删除前一条
            df = df.drop(i - 1).reset_index(drop=True)
            i -= 1  # 删除后索引前移
        elif cur_high < pre_high and cur_low > pre_low:
            # 打印包含关系
            print(f"包含关系: 当前行({cur_high}, {cur_low}) 被被被 前一行({pre_high}, {pre_low}) 包含")
            if cur_low > min_low:
                min_low = cur_low
            if cur_high < max_high:
                max_high = cur_high
            # 需要有前一条的前一条
            if i - 2 >= 0:
                pre2_high = float(df.at[i - 2, "最高价"])
                if (i == len(df) - 1) or ((i < len(df) - 1) and (float(df.at[i + 1, "最高价"]) > pre_high or float(df.at[i + 1, "最低价"]) < pre_low)):
                    if pre_high > pre2_high:
                        df.at[i - 1, "最低价"] = min_low
                    else:
                        df.at[i - 1, "最高价"] = max_high
            # 删除当前这条
            df = df.drop(i).reset_index(drop=True)
        else:
            # 打印不包含关系
            print(f"不包含关系: 当前行({cur_high}, {cur_low}) 与 前一行({pre_high}, {pre_low}) 无包含关系")
            # 如果没有包含关系，更新最大值和最小值
            max_high = float('inf')  # 如果有连续包含，需要更新最大值时，找出最小的那个最大值
            min_low = float('-inf')  # 如果有连续包含，需要更新最小值时，找出最大的那个最小值
            i += 1

    # 步骤2：调整开盘价和收盘价
    for i, row in df.iterrows():
        open_p = float(row["开盘价"])
        close_p = float(row["收盘价"])
        high_p = float(row["最高价"])
        low_p = float(row["最低价"])
        if open_p > close_p:
            df.at[i, "开盘价"] = high_p
            df.at[i, "收盘价"] = low_p
        else:
            df.at[i, "开盘价"] = low_p
            df.at[i, "收盘价"] = high_p
    return df
