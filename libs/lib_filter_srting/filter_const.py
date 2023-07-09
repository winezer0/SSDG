#!/usr/bin/env python
# encoding: utf-8

# 定义一些常量名称
#########################
# 去重
FT_NO_DUPLICATE = "FT_NO_DUPLICATE"
#########################
FT_IGNORE_EMPTY = "FT_IGNORE_EMPTY"  # 忽略空字符的处理
FT_IGNORE_SYMBOLS = "FT_IGNORE_SYMBOLS"  # 过滤操作时时忽略包含特定字符的字符串
#########################
# 长度过滤
# # 列表
FT_MIN_LEN_STR = "FT_MIN_LEN_STR"
FT_MAX_LEN_STR = "FT_MAX_LEN_STR"
# # 元组
FT_MIN_LEN_NAME = "FT_MIN_LEN_NAME"
FT_MAX_LEN_NAME = "FT_MAX_LEN_NAME"
FT_MIN_LEN_PASS = "FT_MIN_LEN_PASS"
FT_MAX_LEN_PASS = "FT_MAX_LEN_PASS"
#########################
# 不允许包含的字符
# # 列表
FT_BAN_SYMBOLS_STR = "FT_BAN_SYMBOLS_STR"
# # 元组
FT_BAN_SYMBOLS_NAME = "FT_BAN_SYMBOLS_NAME"
FT_BAN_SYMBOLS_PASS = "FT_BAN_SYMBOLS_PASS"
#########################
# 字符串中的字符字符种类过滤 排除规则
# # 列表
FT_EXCLUDE_RULES_STR = "FT_EXCLUDE_RULES_STR"
# # 元组
FT_EXCLUDE_RULES_NAME = "FT_EXCLUDE_RULES_NAME"
FT_EXCLUDE_RULES_PASS = "FT_EXCLUDE_RULES_PASS"
#########################
# 字符串中的字符字符种类过滤 提取规则
# # 列表
FT_EXTRACT_RULES_STR = "FT_EXTRACT_RULES_STR"
# # 元组
FT_EXTRACT_RULES_NAME = "FT_EXTRACT_RULES_NAME"
FT_EXTRACT_RULES_PASS = "FT_EXTRACT_RULES_PASS"
#########################
# 字符串中正则过滤 排除规则
# # 列表
FT_EXCLUDE_REGEX_STR = "FT_EXCLUDE_REGEX_STR"
# # 元组
FT_EXCLUDE_REGEX_NAME = "FT_EXCLUDE_REGEX_NAME"
FT_EXCLUDE_REGEX_PASS = "FT_EXCLUDE_REGEX_PASS"
#########################
# 字符串中正则过滤 提取规则
# # 列表
FT_EXTRACT_REGEX_STR = "FT_EXTRACT_REGEX_STR"
# # 元组
FT_EXTRACT_REGEX_NAME = "FT_EXTRACT_REGEX_NAME"
FT_EXTRACT_REGEX_PASS = "FT_EXTRACT_REGEX_PASS"
#########################
# 过滤使用的配置参考
FT_STRING_OPTIONS = {
    FT_IGNORE_SYMBOLS: ["%%","%","}$"],
    FT_IGNORE_EMPTY: True,

    FT_NO_DUPLICATE: True,

    FT_BAN_SYMBOLS_STR: [],

    FT_MIN_LEN_STR: 0,
    FT_MAX_LEN_STR: 12,

    FT_EXTRACT_RULES_STR: [],
    FT_EXCLUDE_RULES_STR: [],

    FT_EXTRACT_REGEX_STR: [],
    FT_EXCLUDE_REGEX_STR: [],
}
#########################
FT_TUPLE_OPTIONS = {
    FT_IGNORE_SYMBOLS: ["%%","%","}$"],
    FT_IGNORE_EMPTY: True,

    FT_NO_DUPLICATE: True,

    FT_BAN_SYMBOLS_NAME: [],
    FT_BAN_SYMBOLS_PASS: [],

    FT_MAX_LEN_NAME: 12,
    FT_MIN_LEN_NAME: 0,
    FT_MAX_LEN_PASS: 12,
    FT_MIN_LEN_PASS: 0,

    FT_EXCLUDE_RULES_NAME: [],
    FT_EXCLUDE_RULES_PASS: [],
    FT_EXTRACT_RULES_NAME: [],
    FT_EXTRACT_RULES_PASS: [],

    FT_EXCLUDE_REGEX_NAME: [],
    FT_EXCLUDE_REGEX_PASS: [],
    FT_EXTRACT_REGEX_NAME: [],
    FT_EXTRACT_REGEX_PASS: [],
}
