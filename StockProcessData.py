import pandas as pd
from enum import Enum

class ProcessType(Enum):
    NO_PROCESS = 0      # 不做任何处理
    ZEN_INCLUDE = 1     # Zen包含处理

def process_json_file(filename: str, process_type: ProcessType):
    df = pd.read_json(filename)
    if process_type == ProcessType.NO_PROCESS:
        return df
    elif process_type == ProcessType.ZEN_INCLUDE:
        return zen_include_process(df)
    else:
        raise ValueError("未知的处理类型")

def zen_include_process(df: pd.DataFrame):
    # 这里实现K线缠论的包含关系处理
    # TODO: 实现缠论包含处理逻辑
    return df