#!/usr/bin/env python
# encoding: utf-8

import re
from itertools import product


def has_chinese_func(string):
    # 存在中文
    return bool(re.search("[\u4e00-\u9fa5]", string))


# 判断字符中是否存在数字
def has_digit_func(string):
    for char in str(string):
        if char.isdigit():
            return True
    return False


# 判断字符中是否存在大写字母
def has_upper_func(string):
    for char in str(string):
        if char.isupper():
            return True
    return False


# 判断字符中是否存在小写字母
def has_lower_func(string):
    for char in str(string):
        if char.islower():
            return True
    return False


# 判断字符串中是否存在符号
def has_symbol_func(string):
    for char in str(string):
        if char in set('!@#$%^&*()_-+={}[]|\:;"<>,.?/~`'):
            return True
    return False


# 判断字符串中 数字、大写、小写、符号的情况
def analyse_string_per_char(string):
    # 分析字符串,判断是否包含指定的元素
    has_digit = has_digit_func(string)
    has_upper = has_upper_func(string)
    has_lower = has_lower_func(string)
    has_symbol = has_symbol_func(string)
    has_chinese = has_chinese_func(string)
    return has_digit, has_upper, has_lower, has_symbol, has_chinese


# 统计字符串中 数字、大写、小写、符号、其他的数量
def statistic_char_frequency(string):
    # 统计每种类型的符号数量
    upper_count = 0
    lower_count = 0
    symbol_count = 0
    digit_count = 0
    other_count = 0
    for letter in string:
        letter = str(letter)
        if letter.isupper():
            upper_count += 1
        elif letter.islower():
            lower_count += 1
        elif letter.isdigit():
            digit_count += 1
        elif letter in set('!@#$%^&*()_-+={}[]|\:;"<>,.?/~`'):
            symbol_count += 1
        else:
            other_count += 1
    return upper_count, lower_count, symbol_count, digit_count, other_count


# 扩展带有通配符的规则
def wildcard_rule_handle(rule_tuple):
    # 使用列表推导式和条件表达式将值为-1的元素替换为1和0
    # 创建一个新列表，将-1替换为[1, 0]
    replacement_list = [str(val) if val != -1 else ['1', '0'] for val in rule_tuple]
    # 使用itertools.product生成所有可能的组合
    return list(product(*replacement_list))


# 格式化用户输入的规则列表
def format_rule_list(tuple_list):
    # 通配符处理
    new_tuple_list=[]
    for rule in tuple_list:
        if -1 in rule:
            rule_list = wildcard_rule_handle(rule)
            new_tuple_list.extend(rule_list)
        else:
            new_tuple_list.append(rule)

    tuple_list = [
        (bool(int(has_digit)), bool(int(has_upper)),
         bool(int(has_lower)),  bool(int(has_symbol)), bool(int(has_chinese)))
        for has_digit, has_upper, has_lower, has_symbol, has_chinese in new_tuple_list
    ]
    return tuple_list


# 正则列表匹配
def regex_is_matched(pattern_list, string):
    return any(re.search(pattern, string) for pattern in pattern_list)