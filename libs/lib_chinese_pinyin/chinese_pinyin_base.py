# 基于中文词汇或中文姓名获取姓、名的拼音

# 拼接并且格式化获取到的姓、名的拼音
from pypinyin import lazy_pinyin, Style

from libs.lib_chinese_pinyin.chinese_const import ALLOWED_STYLES
from libs.lib_run_str_attr.str_attr_run import string_run_attr, is_allowed_action_list
from libs.lib_log_print.logger_printer import output, LOG_DEBUG


def get_word_base_ele_list(name_str, pinyin_styles):
    # Pinyin extraction
    # 获取每个字的 全拼、首字母等 对整体进行操作
    pinyin_list = []
    # 判断样式是否正确
    if is_allowed_action_list(pinyin_styles, ALLOWED_STYLES):
        # 循环调用函数执行
        for pinyin_style in pinyin_styles:
            output(f"[*] {name_str} lazy_pinyin -> pinyin_style:{pinyin_style.name}", level=LOG_DEBUG)
            pinyin = lazy_pinyin(name_str, style=pinyin_style)
            for index, string in enumerate(pinyin):
                if not string.strip():
                    # print(f"{name_str[index]} 获取声母失败, 重新获取首字母.")
                    pinyin[index] = lazy_pinyin(name_str[index], style=Style.FIRST_LETTER)[0]
            pinyin_list.append(pinyin)

    # 去重列表
    pinyin_list = remove_duplicates(pinyin_list)
    return pinyin_list


def merge_base_ele_list(pinyin_list, temp_symbol, py_case_list):
    # 组合基本字符串
    str_list = []
    temp_string = temp_symbol.join(pinyin_list)

    if py_case_list:
        values = string_run_attr(temp_string, py_case_list)
        str_list.extend(values)

    if str_list:
        str_list = list(set(str_list))
    return str_list


# 实现二维列表去重  #保持顺序
def remove_duplicates(arr):
    new_list = []

    tmp_set = set()
    for inner_arr in arr:
        inner_tup = tuple(inner_arr)
        if inner_tup not in tmp_set:
            tmp_set.add(inner_tup)
            new_list.append(inner_arr)
    return new_list
