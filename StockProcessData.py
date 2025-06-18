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


class Type(Enum):
    TOP = "顶分型"
    BOTTOM = "底分型"


def zen_include_process(df: pd.DataFrame):
    df = df.copy().reset_index(drop=True)
    # 初始化每行最后一个字段为dict，包含value、包含数据、顶底分型
    last_col = df.columns[-1]
    df["包含数据"] = 1
    df["顶底分型"] = None
    df["连笔编号"] = 0
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
        if cur_high >= pre_high and cur_low <= pre_low:
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
            df.at[i, "包含数据"] += df.at[i - 1, "包含数据"]
            df = df.drop(i - 1).reset_index(drop=True)
            i -= 1  # 删除后索引前移
        elif cur_high <= pre_high and cur_low >= pre_low:
            # 打印包含关系
            print(f"包含关系: 当前行({cur_high}, {cur_low}) 被被被 前一行({pre_high}, {pre_low}) 包含")
            if cur_low > min_low:
                min_low = cur_low
            if cur_high < max_high:
                max_high = cur_high
            # 需要有前一条的前一条
            if i - 2 >= 0:
                pre2_high = float(df.at[i - 2, "最高价"])
                if (i == len(df) - 1) or ((i < len(df) - 1) and (
                        float(df.at[i + 1, "最高价"]) > pre_high or float(df.at[i + 1, "最低价"]) < pre_low)):
                    if pre_high > pre2_high:
                        df.at[i - 1, "最低价"] = min_low
                    else:
                        df.at[i - 1, "最高价"] = max_high
            # 删除当前这条
            df.at[i - 1, "包含数据"] += df.at[i, "包含数据"]
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

        # 判定顶底分型（排除首尾行）
        if 0 < i < len(df) - 1:
            pre_row = df.iloc[i - 1]
            next_row = df.iloc[i + 1]
            if high_p > float(pre_row["最高价"]) and high_p > float(next_row["最高价"]):
                df.at[i, "顶底分型"] = Type.TOP
            elif high_p < float(pre_row["最高价"]) and high_p < float(next_row["最高价"]):
                df.at[i, "顶底分型"] = Type.BOTTOM

    # 步骤3：缠论笔的分型校验
    fenxing_idx = []
    for i, row in df.iterrows():
        if df.at[i, "顶底分型"] is not None:
            fenxing_idx.append(i)

    # 用连续笔的分型来检测顶底有效性
    # 从第一个顶底参数开始，连续画笔
    # 假设 j0 和 j1 无法构成一个笔，则按照类型来判断
    # 首先如果两者是间距过近，且类型相同，则判断势能更强的那个是有效的
    # 如果两者类型不同，则暂时无法判断哪个是有效哦，需要根据后续的节点来判断，有可能两者都能形成笔或者多笔，如果存在包含关系
    # 则被包含的的连续笔都是无效的。
    # 如果有多个连续笔最后都没有包含关系，则将其一起绘制在图上
    # 如果是因为两者顶底分型类型相同，则j1是无效的顶底分型
    # 假设j0 和 j1 能够形成一笔，则j0肯定是有效的一个顶底分型，接下来只需要判定 j1和j2之间是否成笔，如果不成笔则需要判定哪一个顶底
    # 分型是无效的。
    valid_idx = []
    for j in range(1, len(fenxing_idx) - 1):
        i0, i1, i2 = fenxing_idx[j - 1], fenxing_idx[j], fenxing_idx[j + 1]
        fx0, fx1, fx2 = df.at[i0, "顶底分型"], df.at[i1, "顶底分型"], df.at[i2, "顶底分型"]
        # 首先排除fx0与fx1紧密相连导致无法成笔的情况,两者过近时，如果类型相同则直接清除fx1
        #      如果fx0和fx1类型不同，则判断fx1与fx2的类型是否相同，如果fx1与fx2类型相同，则清除fx1
        #      如果fx1与fx2类型不同，则判断
        if i1 - i0 < 3 or (i1 - i0 == 3 and df.at[i0, "包含数据"] < 2 and df.at[i1, "包含数据"] < 2
                            and df.at[i0 + 1, "包含数据"] < 2 and df.at[i0 + 2, "包含数据"] < 2):
            continue
        # 必须间隔至少一根K线
        if i1 - i0 < 2 or i2 - i1 < 2:
            continue
        # 极值校验
        if fx1 == Type.TOP:
            # i1区间内最高
            if df.at[i1, "最高价"] != max(df.loc[i0:i2, "最高价"]):
                continue
        elif fx1 == Type.BOTTOM:
            # i1区间内最低
            if df.at[i1, "最低价"] != min(df.loc[i0:i2, "最低价"]):
                continue
        valid_idx.append(i1)

    # 先清空所有分型
    #df["顶底分型"] = None
    #for idx in valid_idx:
        #df.at[idx, "顶底分型"] = Type.TOP if df.at[idx, "最高价"] == max(
            #df.loc[idx - 1:idx + 1, "最高价"]) else Type.BOTTOM

    return df
