# -*- coding: utf-8 -*-

# 获取单词列表中的姓氏
import itertools

from libs.lib_chinese_pinyin.chinese_const import *
from libs.lib_chinese_pinyin.chinese_dict import XIN_NAMES_DICT, gen_xin_names_dict_and_key_list
from libs.lib_chinese_pinyin.chinese_pinyin_base import get_word_base_ele_list, merge_base_ele_list, remove_duplicates
from libs.lib_log_print.logger_printer import output, LOG_DEBUG


# 从中文列表中获取其中的姓氏
def get_xin_list_from_words(word_list):
    """# 分析中文词汇列表中的中文姓氏"""
    xin_list = []
    for word in word_list:
        # 传递姓名字典
        optimize_xin_names, optimize_xin_names_key = gen_xin_names_dict_and_key_list(XIN_NAMES_DICT)
        for key in optimize_xin_names_key:
            if word in optimize_xin_names[key]:
                xin_list.append(word)
                break
    return xin_list


# 分割中文字符串中的中文姓氏和名字
def analyse_chinese_name(word, options_dict):
    """
    分割中文字符串中的中文姓氏和名字
    name_max_len 指定姓名的最大长度,一般最多就是4个字
    """
    default = None, None

    if not 2 <= len(word) <= options_dict[PY_CN_NAME_MAX_LEN]:
        return default

    # 传递姓名字典
    optimize_xin_names, optimize_xin_names_key = gen_xin_names_dict_and_key_list(XIN_NAMES_DICT)
    for key in optimize_xin_names_key:
        for xin_name in optimize_xin_names[key]:
            # 如果中文词汇是以中文姓氏开头,并且姓氏的长度是小于当前字符串的
            if word.startswith(xin_name) and len(xin_name) < len(word):
                # xin_name 姓氏 | min_name 名字
                min_name = word[len(xin_name):]
                return xin_name, min_name
    else:
        return default


# 姓 名 元组列表 倒序处理
def reverse_name(tuple_list):
    # 姓 名 元组列表 倒序处理
    new_list = [(list_tuple[1], list_tuple[0]) for list_tuple in tuple_list]
    return new_list


# 合并 姓氏、名字 的 所有 拼音 元素
def chinese_name_tuple_list_format(pinyin_tuple_list, options_dict, link_symbol):
    xin_name_list = []
    min_name_list = []
    for xin_ele_list, min_ele_list in pinyin_tuple_list:
        xin_ele_list = merge_base_ele_list(pinyin_list=xin_ele_list,
                                           temp_symbol=options_dict[PY_TEMP_SYMBOL],
                                           py_case_list=options_dict[PY_XIN_CASE],
                                           )
        min_ele_list = merge_base_ele_list(pinyin_list=min_ele_list,
                                           temp_symbol=options_dict[PY_TEMP_SYMBOL],
                                           py_case_list=options_dict[PY_MIN_CASE],
                                           )
        xin_name_list.extend(xin_ele_list)
        min_name_list.extend(min_ele_list)

    xin_name_list = [str(ele).replace(options_dict[PY_TEMP_SYMBOL], "") for ele in xin_name_list]
    if xin_name_list:
        xin_name_list = sorted(list(set(xin_name_list)), key=len)

    min_name_list = [str(ele).replace(options_dict[PY_TEMP_SYMBOL], "") for ele in min_name_list]
    if min_name_list:
        min_name_list = sorted(list(set(min_name_list)), key=len)

    cartesian_product_list = list(itertools.product(xin_name_list, min_name_list))
    cartesian_product_list = remove_duplicates(cartesian_product_list)
    # print(cartesian_product_list)

    unique_lst = []

    for tuple_s in cartesian_product_list:
        unique_lst.append(link_symbol.join(map(str, tuple_s)))

    # print(len(unique_lst))  # 生成 55个 字符串
    return unique_lst


# 合并一组汉字 的 所有 拼音 元素
def chinese_string_basic_list_format(pinyin_list_list, options_dict, link_symbol):
    # 合并一个 一组汉子的的 所有 拼音 元素
    pinyin_str_list = []
    for pinyin_list in pinyin_list_list:
        pinyin_list = merge_base_ele_list(pinyin_list=pinyin_list,
                                          temp_symbol=options_dict[PY_TEMP_SYMBOL],
                                          py_case_list= options_dict[PY_UNI_CASE],
                                          # py_upper=options_dict[PY_UPPER_UNI],
                                          # py_lower=options_dict[PY_LOWER_UNI],
                                          # py_title=options_dict[PY_TITLE_UNI],
                                          # py_caper=options_dict[PY_CAPER_UNI],
                                          )
        pinyin_str_list.extend(pinyin_list)

    # 保留原始字符串 # 好像没啥用
    # base_pinyin_str_list = copy.copy(result_list)

    # 修改连接字符串
    pinyin_str_list = [str(str_).replace(options_dict[PY_TEMP_SYMBOL], link_symbol) for str_ in pinyin_str_list]
    # 原则上生成 12个 字符串、
    # 当连接符为 符号 的时候,去重结果为11、
    # 当连接符为 空格 的时候,去重结果为9 因为 caper、title 此时相同
    if pinyin_str_list:
        pinyin_str_list = sorted(list(set(pinyin_str_list)), key=len)

    return pinyin_str_list


# 中文词汇转中文拼音,可能是姓名、也有可能只是普通的词汇
def chinese_word_to_any_pinyin(chinese_word, options_dict, link_symbol):
    """
    中文词汇转中文拼音,可能是姓名、也有可能只是普通的词汇
    根据姓氏前缀进行分析，判断是不是中文姓名 是的话 就获取他的（姓氏,名字）
    对于普通的词汇 作为普通词汇进行处理，（也可以将第一个汉字作为姓氏来处理，考虑增加这个开关）
    """
    result_list = []

    # 分析中文词汇中是否存在姓名
    xin_name, min_name = analyse_chinese_name(chinese_word, options_dict=options_dict)

    if xin_name and min_name:
        output("[*] 发现中文姓名,即将进行姓|名拆分处理", level=LOG_DEBUG)

        # 正序处理 （姓,名）
        if options_dict[PY_POSITIVE]:
            # 生成中文姓，名的基本元素列表  # 并进行笛卡尔积组合
            xin_name_list = get_word_base_ele_list(name_str=xin_name,
                                                   pinyin_styles=options_dict[PY_XIN_STYLES],
                                                   )
            min_name_list = get_word_base_ele_list(name_str=min_name,
                                                   pinyin_styles=options_dict[PY_MIN_STYLES],
                                                   )
            pinyin_list = list(itertools.product(xin_name_list, min_name_list))
            # "王安石" [(['wang'], ['an', 'shi']), (['wang'], ['a', 's']), (['wang'], ['a', 'sh']), (['w'], ['an', 'shi'])...
            #  大小写处理
            positive_list = chinese_name_tuple_list_format(pinyin_list,
                                                           options_dict=options_dict,
                                                           link_symbol=link_symbol)
            result_list.extend(positive_list)

            # 倒序处理 （名,姓）
            if options_dict[PY_REVERSE]:
                reverse_list = chinese_name_tuple_list_format(reverse_name(pinyin_list),
                                                              options_dict=options_dict,
                                                              link_symbol=link_symbol)
                result_list.extend(reverse_list)

        # 扩展成普通汉字词汇处理
        if options_dict[PY_XM2CH]:
            pinyin_list = get_word_base_ele_list(name_str=chinese_word,
                                                 pinyin_styles=options_dict[PY_UNI_STYLES],
                                                 )
            univers_list = chinese_string_basic_list_format(pinyin_list,
                                                            options_dict=options_dict,
                                                            link_symbol=link_symbol)
            result_list.extend(univers_list)

    else:
        if options_dict[PY_UNIVERS]:
            # 生成汉语单词的基本元素列表
            pinyin_list = get_word_base_ele_list(name_str=chinese_word,
                                                 pinyin_styles=options_dict[PY_UNI_STYLES],
                                                 )
            #  "我安石" [['wo', 'an', 'shi'], ['w', 'a', 's'], ['w', 'a', 'sh']]
            #  大小写处理
            univers_list = chinese_string_basic_list_format(pinyin_list,
                                                            options_dict=options_dict,
                                                            link_symbol=link_symbol)
            result_list.extend(univers_list)

        # 扩展成中文姓名处理,第一个字为姓氏,之后的为名字
        if options_dict[PY_CH2XM] and len(chinese_word) > 1:
            # 生成中文姓，名的基本元素列表  # 并进行笛卡尔积组合
            xin_name, min_name = chinese_word[1], chinese_word[1:]
            xin_name_list = get_word_base_ele_list(name_str=xin_name,
                                                   pinyin_styles=options_dict[PY_XIN_STYLES],
                                                   )
            min_name_list = get_word_base_ele_list(name_str=min_name,
                                                   pinyin_styles=options_dict[PY_MIN_STYLES],
                                                   )
            pinyin_list = list(itertools.product(xin_name_list, min_name_list))
            # "王安石" [(['wang'], ['an', 'shi']), (['wang'], ['a', 's']), (['wang'], ['a', 'sh']), (['w'], ['an', 'shi'])...
            #  大小写处理
            positive_list = chinese_name_tuple_list_format(pinyin_list,
                                                           options_dict=options_dict,
                                                           link_symbol=link_symbol)
            result_list.extend(positive_list)

            # 倒序处理 （名,姓）
            if options_dict[PY_REVERSE]:
                reverse_list = chinese_name_tuple_list_format(reverse_name(pinyin_list),
                                                              options_dict=options_dict,
                                                              link_symbol=link_symbol)
                result_list.extend(reverse_list)

    return result_list
