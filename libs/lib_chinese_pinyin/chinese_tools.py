# -*- coding: utf-8 -*-
import copy
import re

import jieba

from libs.lib_chinese_pinyin.chinese_const import PY_CN_USE_JIEBA
from libs.lib_chinese_pinyin.chinese_name_handle import get_xin_list_from_words
from libs.lib_chinese_pinyin.chinese_string_handle import gen_chinese_word_to_pinyin_list_dict
from libs.lib_log_print.logger_printer import output, LOG_ERROR, LOG_DEBUG
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str


# 判断列表内的元素是否存在有包含在字符串内的
def list_ele_in_str(list_=None, str_=None, default=False):
    if list_ is None:
        list_ = []

    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


def replace_str_by_replace_dict(string, replace_dict):
    # 替换列表中包含中文的字符串,返回一个字符串
    for replace_key, replace_value in replace_dict.items():
        if replace_key in string:
            string = str(string).replace(replace_key, replace_value)
    return string


def replace_list_by_replace_dict(string_list, replace_dict):
    # 批量替换字符串
    tmp_list = []
    for string in string_list:
        string = replace_str_by_replace_dict(string, replace_dict)
        tmp_list.append(string)
    return tmp_list


def split_chinese_or_none_list(string_list):
    # 分离列表里面中文字符串和没有中文的字符串
    chinese_str_list = []
    english_str_list = []
    for string in string_list:
        if has_chinese(string):
            chinese_str_list.append(string)
        else:
            english_str_list.append(string)
    return chinese_str_list, english_str_list


def has_chinese(string):
    # 字符串中是否包含中文
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    return bool(pattern.findall(string))


def extracting_chinese_str_by_re(chinese_string):
    # 通过正则表达式 提取字符串中连续的中文
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    keywords = pattern.findall(chinese_string)
    return keywords


def extracting_chinese_str_by_jieba(chinese_string):
    chinese_words = []

    try:
        # 通过jieba分词 提取字符串中连续的中文
        chinese_words = list(jieba.cut(chinese_string))
        # output(f"[+] jieba.cut({chinese_string}) -> {chinese_words}", level=LOG_DEBUG)
        # jieba.cut 湖南%%guan_li_yuan%%王作为猪八戒->['湖南', '%%', 'guan', '_', 'li', '_', 'yuan%', '%', '王', '作为', '猪八戒']

        if not len(chinese_words) > 0:
            output(f"[-] 使用jieba分词[{chinese_string}]失败...", level=LOG_ERROR)
        else:
            # 过滤列表中的所有中文元素
            chinese_words = [key for key in chinese_words if has_chinese(key)]

            # 判断中文列表里面是否存在单独的姓,如果有的话,就将 姓 和 姓的下一个索引拼接起来，返回新的列表
            if len(chinese_words) >= 2:
                name_xin_list = get_xin_list_from_words(chinese_words)
                if len(name_xin_list) > 0:
                    output(f"[+] 姓氏检测完毕: [{chinese_string}]存在姓氏[{name_xin_list}]", level=LOG_DEBUG)
                    # 合并姓和名 输出新的字典
                    chinese_words = merge_xin_min(name_xin_list, chinese_words, chinese_string)

    except Exception as error:
        output(f"[!] 使用jieba分词过程发生未知错误[{error}]", level=LOG_ERROR)
    return chinese_words


def merge_xin_min(name_xin_list, chinese_words, chinese_string):
    # 合并单独的姓氏和名字
    new_chinese_words = copy.copy(chinese_words)

    fixed = "$$$"
    # 合并姓氏和他后面的一个中文词汇
    for name_xin in name_xin_list:
        index = chinese_words.index(name_xin)
        if index + 1 < len(chinese_words):
            output(f"[*] 姓氏索引定位 [{name_xin}]->{chinese_words}->[{index}]")
            new_name = chinese_words[index] + chinese_words[index + 1]
            # 判断在原始字符串里,是不是有这个姓名
            if new_name in chinese_string:
                output(f"[*] 姓氏[{chinese_words[index]}] + 名字[{chinese_words[index + 1]}] -> [{new_name}]")
                new_chinese_words.append(new_name)
                # 如果不保存原始姓氏,就应把原始姓氏删除
                new_chinese_words[index] = fixed
                new_chinese_words[index + 1] = fixed
        else:
            output(f"[-] 跳过姓氏定位 [{name_xin}]->{chinese_words}->[-1]")

    # 去除新结果中的删除标记
    chinese_words = [word for word in new_chinese_words if word != fixed]
    return chinese_words


def replace_chinese_string_to_pinyin_list(chinese_string, options_dict, link_symbol):
    # 替换 整个 中文 到 新的 拼音 列表

    # 1、提取其中的连续的中文字符串
    chinese_word_list = []
    if options_dict[PY_CN_USE_JIEBA]:
        chinese_word_list = extracting_chinese_str_by_jieba(chinese_string)
        output(f"[+] 通过jieba提取[{chinese_string}]中文词组 结果:{chinese_word_list}")

    # 使用正则进行中文分词
    if len(chinese_word_list) < 1:
        chinese_word_list = extracting_chinese_str_by_re(chinese_string)
        output(f"[+] 通过正则提取[{chinese_string}]中文词组 结果:{chinese_word_list}")

    # 去重中文, 保证 将相同的中文 替换为 相同的数据
    if chinese_word_list:
        chinese_word_list = list(set(chinese_word_list))
        output(f"[*] 正则及jieba总提取中文词组 结果:{chinese_word_list}")

    # 生成 中文: 中文的拼音列表替换 字典  # 重点
    chinese_to_pinyin_key_dict, pinyin_key_to_value_list_dict = gen_chinese_word_to_pinyin_list_dict(chinese_word_list,
                                                                                                     options_dict=options_dict,
                                                                                                     link_symbol=link_symbol)

    # 生成新的字符串 # %%hunan%%%%guanliyuan%%%%wangzuowei%%
    chinese_string = replace_str_by_replace_dict(chinese_string, chinese_to_pinyin_key_dict)

    # 进行姓名变量替换
    chinese_string_gen_list, replace_count_, running_time = replace_list_has_key_str(
        will_replace_list=[chinese_string],
        replace_used_dict_=pinyin_key_to_value_list_dict)

    if chinese_string_gen_list:
        chinese_string_gen_list = list(set(chinese_string_gen_list))
    return chinese_string_gen_list


def replace_chinese_list_to_pinyin_list(chinese_string_list, options_dict, link_symbol):
    # 替换中文 列表 到 新的 拼音 列表
    new_string_list = []
    output(f"[*] 拼音转换处理: {str(chinese_string_list)[:50]}")
    for chinese_string in chinese_string_list:
        chinese_string_gen_list = replace_chinese_string_to_pinyin_list(chinese_string, options_dict, link_symbol)
        new_string_list.extend(chinese_string_gen_list)
    return new_string_list


