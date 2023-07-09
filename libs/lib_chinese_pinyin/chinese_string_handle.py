# -*- coding: utf-8 -*-

from pypinyin import lazy_pinyin, Style

# 生成拼音替换字典  管理员->%guanliyuan%
from libs.lib_chinese_pinyin.chinese_name_handle import chinese_word_to_any_pinyin
# 生成中文<->中文的pinyin的标记值替换
from libs.lib_log_print.logger_printer import output


def gen_chinese_to_pinyin_mark_dict(chinese_word_list):
    chinese_to_pinyin_key_dict = {}

    # 按长度排序字典，从长到短替换
    chinese_word_list = sorted(chinese_word_list, key=len, reverse=True)

    for chinese_word in chinese_word_list:
        # 姓名转基本的拼音字符串
        chinese_word_pinyin_key = '_'.join(lazy_pinyin(chinese_word, style=Style.NORMAL))
        chinese_to_pinyin_key_dict[chinese_word] = f"%%{chinese_word_pinyin_key}%%"
    return chinese_to_pinyin_key_dict


# 生成 中文<-->pinyin实际值的替换
def gen_chinese_word_to_pinyin_list_dict(chinese_word_list, options_dict, link_symbol):
    output(f"[*] 衍生单词列表的替换字典 开始:{chinese_word_list}")
    # 生成单词列表的替换字典 湖南 -> %hunan%， 王作为 -> %wangzuowei%
    chinese_word_to_pinyin_key_dict = gen_chinese_to_pinyin_mark_dict(chinese_word_list)
    # print(chinese_word_to_pinyin_key_dict) # {'王作为': '%%wangzuowei%%', '湖南': '%%hunan%%'}
    output(f"[*] 衍生单词列表的替换字典 完成:{chinese_word_to_pinyin_key_dict}")

    # 生成中文对应的拼音替换列表
    output(f"[*] 衍生中文对应拼音替换列表 开始:{str(chinese_word_to_pinyin_key_dict)[:50]}")
    chinese_pinyin_key_to_value_list_dict = {}
    for chinese_str, replace_str in chinese_word_to_pinyin_key_dict.items():
        pinyin_value_list = chinese_word_to_any_pinyin(chinese_str, options_dict=options_dict,
                                                       link_symbol=link_symbol)  # 重点函数
        chinese_pinyin_key_to_value_list_dict[replace_str] = pinyin_value_list
    output(f"[*] 衍生中文对应拼音替换列表 完成:{str(chinese_pinyin_key_to_value_list_dict)[:50]}")

    return chinese_word_to_pinyin_key_dict, chinese_pinyin_key_to_value_list_dict
