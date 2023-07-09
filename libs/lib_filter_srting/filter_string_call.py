#!/usr/bin/env python
# encoding: utf-8

from libs.lib_dyna_rule.dyna_rule_tools import de_duplicate_tuple_list
from libs.lib_filter_srting.filter_const import *
from libs.lib_filter_srting.filter_string_rule import *


def format_string_list(string_list=[], options_dict={}):
    # 最后再处理一次字符串列表
    if string_list:
        if options_dict[FT_NO_DUPLICATE]:
            # 去重复  # 会保留空字符
            string_list = list(set(string_list)) if string_list else []

        if options_dict[FT_MAX_LEN_STR]:
            # 按长度筛选
            string_list = exclude_string_list_by_length(string_list=string_list,
                                                        min_len_str=options_dict[FT_MIN_LEN_STR],
                                                        max_len_str=options_dict[FT_MAX_LEN_STR],
                                                        ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                        ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                        )

        if options_dict[FT_BAN_SYMBOLS_STR]:
            # 不允许包含指定的字符列表
            string_list = exclude_string_list_by_symbols(string_list=string_list,
                                                         ban_symbols_str=options_dict[FT_BAN_SYMBOLS_STR],
                                                         ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                         ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                         )

        # 按格式排除
        if options_dict[FT_EXCLUDE_RULES_STR]:
            string_list = exclude_string_list_by_char_type(string_list=string_list,
                                                           expected_rules_str=options_dict[FT_EXCLUDE_RULES_STR],
                                                           ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                           ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                           )
        # 按格式提取
        if options_dict[FT_EXTRACT_RULES_STR]:
            string_list = extract_string_list_by_char_type(string_list=string_list,
                                                           expected_rules_str=options_dict[FT_EXTRACT_RULES_STR],
                                                           ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                           ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                           )

        # 按格式排除
        if options_dict[FT_EXCLUDE_REGEX_STR]:
            string_list = exclude_string_list_by_regex(string_list=string_list,
                                                       expected_regex_str=options_dict[FT_EXCLUDE_REGEX_STR],
                                                       ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                       ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                       )
        # 按格式提取
        if options_dict[FT_EXTRACT_REGEX_STR]:
            string_list = extract_string_list_by_regex(string_list=string_list,
                                                       expected_regex_str=options_dict[FT_EXTRACT_REGEX_STR],
                                                       ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                       ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                       )

    return string_list


# 对每次生成的(账号,密码)列表进行统一的格式化
def format_tuple_list(tuple_list=[], options_dict={}):
    # 最后再处理一次字符串列表
    if tuple_list:
        if options_dict[FT_NO_DUPLICATE]:
            # 去重复
            tuple_list = de_duplicate_tuple_list(tuple_list=tuple_list)

        # 不允许包含指定的字符列表
        if options_dict[FT_BAN_SYMBOLS_NAME] or options_dict[FT_BAN_SYMBOLS_PASS]:
            tuple_list = exclude_tuple_list_by_symbols(tuple_list=tuple_list,
                                                       ban_symbols_name=options_dict[FT_BAN_SYMBOLS_NAME],
                                                       ban_symbols_pass=options_dict[FT_BAN_SYMBOLS_PASS],
                                                       ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                       ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                       )

        if options_dict[FT_MIN_LEN_NAME] or options_dict[FT_MIN_LEN_PASS]:
            # 按长度筛选 # 需要传递两种长度
            tuple_list = exclude_pair_tuples_by_length(tuple_list=tuple_list,
                                                       min_len_name=options_dict[FT_MIN_LEN_NAME],
                                                       max_len_name=options_dict[FT_MAX_LEN_NAME],
                                                       min_len_pass=options_dict[FT_MIN_LEN_PASS],
                                                       max_len_pass=options_dict[FT_MAX_LEN_PASS],
                                                       ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                       ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                       )

        # 按格式排除 # 需要传递两种规则列表
        if options_dict[FT_EXCLUDE_RULES_NAME] or options_dict[FT_EXCLUDE_RULES_PASS]:
            tuple_list = exclude_tuple_list_by_char_type(tuple_list=tuple_list,
                                                         expected_rules_name=options_dict[FT_EXCLUDE_RULES_NAME],
                                                         expected_rules_pass=options_dict[FT_EXCLUDE_RULES_PASS],
                                                         ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                         ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                         )
        # 按格式提取 # 需要传递两种规则列表
        if options_dict[FT_EXTRACT_RULES_NAME] or options_dict[FT_EXTRACT_RULES_PASS]:
            tuple_list = extract_tuple_list_by_char_type(tuple_list=tuple_list,
                                                         expected_rules_name=options_dict[FT_EXTRACT_RULES_NAME],
                                                         expected_rules_pass=options_dict[FT_EXTRACT_RULES_PASS],
                                                         ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                         ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                         )

        # 按格式排除 # 需要传递两种规则列表
        if options_dict[FT_EXCLUDE_REGEX_NAME] or options_dict[FT_EXCLUDE_REGEX_PASS]:
            tuple_list = exclude_tuple_list_by_regex(tuple_list=tuple_list,
                                                         expected_regex_name=options_dict[FT_EXCLUDE_REGEX_NAME],
                                                         expected_regex_pass=options_dict[FT_EXCLUDE_REGEX_PASS],
                                                         ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                         ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                         )
        # 按格式提取 # 需要传递两种规则列表
        if options_dict[FT_EXTRACT_REGEX_NAME] or options_dict[FT_EXTRACT_REGEX_PASS]:
            tuple_list = extract_tuple_list_by_regex(tuple_list=tuple_list,
                                                         expected_regex_name=options_dict[FT_EXTRACT_REGEX_NAME],
                                                         expected_regex_pass=options_dict[FT_EXTRACT_REGEX_PASS],
                                                         ignore_empty=options_dict[FT_IGNORE_EMPTY],
                                                         ignore_symbols=options_dict[FT_IGNORE_SYMBOLS],
                                                         )
    return tuple_list


if __name__ == '__main__':
    str_list = ["admin123", "111", "", "猪八戒"]
    # OPTIONS = {
    #     FT_IGNORE_SYMBOLS: ["%%","%","}$"],
    #     FT_IGNORE_EMPTY: False,
    #
    #     FT_NO_DUPLICATE: True,
    #
    #     FT_BAN_SYMBOLS_STR: [],
    #
    #     FT_MIN_LEN_STR: 1,
    #     FT_MAX_LEN_STR: 12,
    #     # has_digit, has_upper, has_lower, has_symbol
    #     FT_EXTRACT_RULES_STR: [(True, False, True, False)],
    #     FT_EXCLUDE_RULES_STR: []
    # }
    # new_str_list = format_string_list(string_list=str_list, options_dict=OPTIONS)
    # print(new_str_list)
    #
    # tuple_list = [("admin", "admin123"),
    #               ("猪八戒", "猪八戒"),
    #               ("111", "111"),
    #               ]
    #
    # OPTIONS = {
    #     FT_IGNORE_SYMBOLS: ["%%","%","}$"],
    #     FT_IGNORE_EMPTY: True,
    #
    #     FT_NO_DUPLICATE: True,
    #
    #     FT_BAN_SYMBOLS_NAME: [],
    #     FT_BAN_SYMBOLS_PASS: [],
    #
    #     FT_MAX_LEN_NAME: 12,
    #     FT_MIN_LEN_NAME: 0,
    #     FT_MAX_LEN_PASS: 12,
    #     FT_MIN_LEN_PASS: 0,
    #
    #     FT_EXCLUDE_RULES_NAME: [],
    #     FT_EXCLUDE_RULES_PASS: [],
    #
    #     FT_EXTRACT_RULES_NAME: [],
    #     FT_EXTRACT_RULES_PASS: [],
    # }
    #
    # new_tuple_list = format_tuple_list(tuple_list=tuple_list, options_dict=OPTIONS)
    # print(new_tuple_list)
