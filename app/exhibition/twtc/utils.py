from typing import Any


def get_next_element(loop_list: list, input_value: Any):
    # 找到輸入數字在列表中的索引
    index = loop_list.index(input_value)

    # 使用模數運算找到下一個元素的索引
    next_index = (index + 1) % len(loop_list)

    # 返回下一個元素
    return loop_list[next_index]
