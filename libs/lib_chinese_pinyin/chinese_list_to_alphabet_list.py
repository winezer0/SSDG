# -*- coding: utf-8 -*-
import copy

from libs.lib_chinese_pinyin.chinese_const import *
from libs.lib_chinese_pinyin.chinese_dict import TRANSLATE_DICT
from libs.lib_chinese_pinyin.chinese_dict_handle import *
from libs.lib_chinese_pinyin.chinese_tools import replace_list_by_replace_dict, \
    split_chinese_or_none_list, replace_chinese_list_to_pinyin_list, list_ele_in_str
from libs.lib_log_print.logger_printer import output, LOG_DEBUG
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str


def handle_alphabet_list(alphabet_list, options_dict):
    # 最后再处理一次字符串列表
    if alphabet_list:
        if options_dict[PY_FT_NO_BLANK]:
            # 去除空格
            alphabet_list = [str(string).replace(" ", "") for string in alphabet_list]

        if options_dict[PY_FT_NO_DUPL]:
            # 去重复
            alphabet_list = list(set(alphabet_list)) if alphabet_list else []

        if options_dict[PY_FT_MAX_LEN]:
            # 按长度筛选
            alphabet_list = [pinyin for pinyin in alphabet_list
                             if len(pinyin) <= options_dict[PY_FT_MAX_LEN]
                             or list_ele_in_str(options_dict[PY_IGNORE_SYMBOL], str_=pinyin, default=False)
                             ]

    return alphabet_list


def chinese_list_to_alphabet_list(string_list, options_dict, store_chinese=False):
    # 中文转字母处理

    # 存储最终替换结果
    alphabet_list = []

    # 分离没有中文的字符串 不处理没有中文的字符串
    pre_chinese_list, pre_english_list = split_chinese_or_none_list(string_list)

    # 保留所有原始数据
    if store_chinese:
        alphabet_list.extend(string_list)
    else:
        # 对其中的英语不做处理
        alphabet_list.extend(pre_english_list)

    # 优化专业术语字典
    output(f"[*] 中文专业术语处理开始: [{str(list(TRANSLATE_DICT.keys()))[:50]}...]", level=LOG_DEBUG)
    translate_dict_optimize = optimize_translate_dict(TRANSLATE_DICT, options_dict=options_dict)

    # 预处理字符串中的专业术语,先不替换，等替换了拼音以后再替换
    chinese_to_pinyin_key_dict, pinyin_key_to_value_list_dict = gen_translate_replace_dict(translate_dict_optimize)
    # output(f"[*] 关键字<->关键字拼音:{str(chinese_to_pinyin_key_dict)[:50]}...", level=LOG_DEBUG)
    # output(f"[*] 关键字拼音<->值列表:{str(pinyin_key_to_value_list_dict)[:50]}...", level=LOG_DEBUG)

    # 先将列表中的 中文专业术语 替换为 %中文术语的拼音% 格式
    render_pro_list = replace_list_by_replace_dict(pre_chinese_list, chinese_to_pinyin_key_dict)
    output(f"[*] 中文专业术语处理结果: {str(render_pro_list)[:50]}...", level=LOG_DEBUG)

    # 仅需进行专业术语替换的列表
    need_term_repl_list = []
    # 区分没有姓名有有姓名的字符串
    render_pro_cn_list, render_pro_en_list = split_chinese_or_none_list(render_pro_list)
    need_term_repl_list.extend(render_pro_en_list)

    for link_symbol in options_dict[PY_LINK_SYMBOLS]:
        # 对字符串中的姓名进行拼音替换 # 重点函数
        output(f"[*] 中文词汇拼音 link:[{link_symbol}] 处理完毕:{str(render_pro_cn_list)[:50]}...", level=LOG_DEBUG)
        render_chinese_name_list = replace_chinese_list_to_pinyin_list(chinese_string_list=render_pro_cn_list,
                                                                       options_dict=options_dict,
                                                                       link_symbol=link_symbol)
        output(f"[*] 中文词汇拼音 link:[{link_symbol}] 处理完毕:{str(render_chinese_name_list)[:50]}...", level=LOG_DEBUG)
        need_term_repl_list.extend(render_chinese_name_list)
    output(f"[*] 中文词汇拼音 link:{options_dict[PY_LINK_SYMBOLS]} 处理完毕:{str(need_term_repl_list)[:50]}...", level=LOG_DEBUG)

    # 进行专业术语替换
    render_all_list, replace_count_, running_time = replace_list_has_key_str(will_replace_list=need_term_repl_list,
                                                                             replace_used_dict_=pinyin_key_to_value_list_dict)

    # 将渲染后的结果保存到结果列表
    alphabet_list.extend(render_all_list)

    # 最后再进行一次渲染结果处理
    alphabet_list = handle_alphabet_list(alphabet_list=alphabet_list, options_dict=options_dict)

    output(f"[*] 中文词汇渲染结果列表:{str(alphabet_list)[:50]}...", level=LOG_DEBUG)
    return alphabet_list


def dict_chinese_to_dict_alphabet(string_dict, options_dict, store_chinese=False):
    string_dict = copy.copy(string_dict)
    for key, string_list in string_dict.items():
        if string_list:
            string_dict[key] = chinese_list_to_alphabet_list(string_list=string_list,
                                                             options_dict=options_dict,
                                                             store_chinese=store_chinese)
    return string_dict


if __name__ == '__main__':
    import time

    start_time = time.time()

    # text = "管理员" # DEFAULT_OPTIONS->21
    # text = "管理" # DEFAULT_OPTIONS->150
    # text = "理解" # DEFAULT_OPTIONS->96
    # text = "sssssssssssssGG"  # DEFAULT_OPTIONS->1
    # text = "湖南省管理员郑GG"  # DEFAULT_OPTIONS->60984
    # text = "湖南省管理员猪八戒"  # DEFAULT_OPTIONS->617463  COMMON_OPTIONS->1134
    text = "管理员洪双喜"  # COMMON_OPTIONS->1008
    text_list = [text]
    my_options_dict = PY_BASE_OPTIONS
    result_list = chinese_list_to_alphabet_list(string_list=text_list,
                                                options_dict=my_options_dict,
                                                store_chinese=False)
    print(len(result_list))
    # print(result_list)
    end_time = time.time()
    print(f"运行时间: {end_time - start_time} 秒")
