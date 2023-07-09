#!/usr/bin/env python
# encoding: utf-8
import copy
import os
import pathlib
import time

from libs.lib_chinese_pinyin.chinese_const import *
from libs.lib_dyna_rule.dyna_rule_const import *
from libs.lib_filter_srting.filter_const import *
from libs.lib_run_str_attr.str_attr_const import *
from libs.lib_social_dict.repl_const import *

############################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()
############################################################
# 排除历史爆破记录的功能
GB_EXCLUDE_FLAG = True
# 排除历史爆破文件名称
GB_EXCLUDE_FILE = "history_file.txt"
# 记录历史账号密码时的const_sign 的 连接符号 # 无需修改
GB_CONST_LINK = '<-->'
############################################################
# 基本变量文件夹 里面的每个文件都代表一个替换变量
GB_BASE_VAR_DIR = GB_BASE_DIR.joinpath("dict_base")
# 存储 需要用户的输入的基本变量, 防止文件太多所以进行分离
GB_BASE_DYNA_DIR = GB_BASE_DIR.joinpath("dict_dyna")
# 存储 仅用户账号相关的基本变量
GB_BASE_NAME_DIR = GB_BASE_DIR.joinpath("dict_name")
# 存储 仅用户密码相关的基本变量
GB_BASE_PASS_DIR = GB_BASE_DIR.joinpath("dict_pass")

# 基本变量字典文件的后缀名列表 通过file.endswith匹配
GB_BASE_DICT_SUFFIX = [".min.txt", ".man.txt"]
# 存储 自定义 基本变量
GB_BASE_VAR_REPLACE_DICT = {}
###################
# 存储 自定义 因变量
GB_DEPENDENT_VAR_REPLACE_DICT = {
    STR_VAR_DEPENDENT: [],  # 存储自定义因变量
    STR_VAR_DOMAIN: [],  # 存储动态PATH因变量-无需处理
    STR_VAR_PATH: [],  # 存储动态域名因变量-无需处理
    STR_VAR_BLANK: [''],
}

# DOMAIN PATH 因变量中的 符号替换规则, 替换后追加到域名因子列表
GB_SYMBOL_REPLACE_DICT = {":": ["_"], ".": ["_"]}
# 删除带有 特定符号 的因变量（比如:）的元素
GB_NOT_ALLOW_SYMBOL = [":"]
# 忽略IP格式的域名
GB_IGNORE_IP_FORMAT = True
# 手动指定获取域名因变量的域名 # 仅用于单独调用口令生成脚本
GB_TARGET_URL = None
###################
# 指定用户名变量字符串 # 在密码字典中用这个变量表示用户名
GB_USER_NAME_MARK = "%%USERNAME%%"
############################################################
# 账号密码目录
GB_RULE_DICT_DIR = GB_BASE_DIR.joinpath("dict_rule")
# 账号密码字典文件的格式
GB_NAME_FILE_STR = str(GB_RULE_DICT_DIR.joinpath("level{LEVEL}.mode1_name.txt"))
GB_PASS_FILE_STR = str(GB_RULE_DICT_DIR.joinpath("level{LEVEL}.mode1_pass.txt"))
# 账号密码对文件命名格式
GB_PAIR_FILE_STR = str(GB_RULE_DICT_DIR.joinpath("level{LEVEL}.mode2_pairs.txt"))
###################
# 实际调用的字典级别设置
GB_RULE_LEVEL_NAME = 1  # 调用 level1.mode1_name.txt
GB_RULE_LEVEL_PASS = 1  # 调用 level1.mode1_pass.txt
GB_RULE_LEVEL_PAIR = 1  # 调用 level1.mode2_pairs.txt
GB_RULE_LEVEL_EXACT = True  # 是否仅调用精确的字典级别,不调用更下级的字典
###################
# 直接输入账号密码对文件
# 账号密码对文件 连接符号
GB_PAIR_LINK_SYMBOL = ':'
# 使用账号:密码对文件进行爆破，默认使用账号字典、密码字典
GB_PAIR_FILE_FLAG = False
# 使用账号:密码对文件进行爆破时,是否进行基本变量替换
GB_USE_PAIR_BASE_REPL = False
##################################################################
# 设置输出结果文件目录
GB_RESULT_DIR = GB_BASE_DIR.joinpath("result")
# 指定记录字典文件的目录
GB_TEMP_DICT_DIR = GB_RESULT_DIR.joinpath(f"dict.{time.strftime('%Y-%m-%d-%H-%M', time.localtime())}")
############################################################
# 用户名中的中文转拼音处理
GB_CHINESE_TO_PINYIN = True  # 开启中文转拼音的操作
GB_STORE_CHINESE = True  # 保留原始的中文字符串 便于中文用户名的爆破
# GB_IGNORE_SYMBOLS = ["%%", "%", "}$"] # }$规则解析应该已经被处理|%基本变量应该已经被处理
GB_IGNORE_SYMBOLS = ["%%", "</"]  # %% 表明字符串还需要因变量替换、 </表明还需要tag_exec处理
###################
# 中文转拼音处理时，通过长度对最后的（账号:密码）进行过滤的依据
GB_USER_NAME_MIN_LEN = 0  # 用户名最小长度（含）
GB_USER_NAME_MAX_LEN = 12  # 用户名最大长度（含）

GB_USER_PASS_MIN_LEN = 0  # 密码最小长度（含）
GB_USER_PASS_MAX_LEN = 12  # 密码最大长度（含）
#######################
# 中文转拼音处理时，对字符串列表处理时的配置字典
# GB_CHINESE_OPTIONS_LIST = copy.copy(PY_BASE_OPTIONS)  # MAX_OPTIONS->最大化配置,不建议使用
# GB_CHINESE_OPTIONS_LIST[PY_FT_MAX_LEN] = GB_USER_NAME_MAX_LEN  # 最终生成的字符串不能超过这个长度
# GB_CHINESE_OPTIONS_LIST[PY_IGNORE_SYMBOL] = GB_IGNORE_SYMBOLS  # 长度过滤时忽略带有这些字符的元素
#######################
# 对账号中依赖的中文处理方案
GB_CHINESE_OPTIONS_NAME = {
    PY_TEMP_SYMBOL: "_",
    PY_LINK_SYMBOLS: [""],
    PY_CN_NAME_MAX_LEN: 4,

    PY_SY_CASE: [ATTR_LOWER],

    PY_CN_USE_JIEBA: True,

    PY_POSITIVE: True,
    PY_REVERSE: False,
    PY_UNIVERS: True,

    PY_XM2CH: False,
    PY_CH2XM: False,

    PY_FT_NO_BLANK: True,
    PY_FT_NO_DUPL: True,
    PY_FT_MAX_LEN: GB_USER_NAME_MAX_LEN,
    PY_IGNORE_SYMBOL: GB_IGNORE_SYMBOLS,

    PY_UNI_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_UNI_CASE: [ATTR_LOWER],

    PY_XIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_XIN_CASE: [ATTR_LOWER],

    PY_MIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_MIN_CASE: [ATTR_LOWER],

}
#######################
# 对密码中依赖的中文处理方案
GB_CHINESE_OPTIONS_PASS = {
    PY_TEMP_SYMBOL: "_",
    PY_LINK_SYMBOLS: [""],
    PY_CN_NAME_MAX_LEN: 4,

    PY_SY_CASE: [ATTR_LOWER, ATTR_UPPER, ATTR_TITLE, ATTR_CAPER],

    PY_CN_USE_JIEBA: True,

    PY_POSITIVE: True,
    PY_REVERSE: False,
    PY_UNIVERS: True,

    PY_XM2CH: False,
    PY_CH2XM: False,

    PY_FT_NO_BLANK: True,
    PY_FT_NO_DUPL: True,
    PY_FT_MAX_LEN: GB_USER_NAME_MAX_LEN,
    PY_IGNORE_SYMBOL: GB_IGNORE_SYMBOLS,

    PY_UNI_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_UNI_CASE: [ATTR_LOWER, ATTR_UPPER, ATTR_TITLE, ATTR_CAPER],

    PY_XIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_XIN_CASE: [ATTR_LOWER, ATTR_UPPER, ATTR_TITLE, ATTR_CAPER],

    PY_MIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_MIN_CASE: [ATTR_LOWER, ATTR_UPPER, ATTR_TITLE, ATTR_CAPER],

}
#######################
# 中文转拼音处理时，对元组列表处理时的配置字典
# GB_CHINESE_OPTIONS_TUPLE = copy.copy(PY_BASE_OPTIONS)  # MAX_OPTIONS->最大化配置,不建议使用
# GB_CHINESE_OPTIONS_TUPLE[PY_FT_MAX_LEN] = GB_USER_NAME_MAX_LEN * 2  # 最终生成的字符串不能超过这个长度
# GB_CHINESE_OPTIONS_TUPLE[PY_IGNORE_SYMBOL] = GB_IGNORE_SYMBOLS  # 长度过滤时忽略带有这些字符的元素
GB_CHINESE_OPTIONS_TUPLE = copy.copy(GB_CHINESE_OPTIONS_NAME)
GB_CHINESE_OPTIONS_TUPLE[PY_FT_MAX_LEN] = GB_USER_NAME_MAX_LEN * 2
############################################################
# 对生成的账号|密码列表进行排除的选项配置
GB_IGNORE_EMPTY = True  # 进行格式过滤时保留空值[""]
# 排除列表 排除姓名的配置
# GB_FILTER_OPTIONS_NAME = copy.copy(FILTER_STRING_OPTIONS)
GB_FILTER_OPTIONS_NAME = {
    FT_IGNORE_SYMBOLS: GB_IGNORE_SYMBOLS,
    FT_IGNORE_EMPTY: GB_IGNORE_EMPTY,

    FT_NO_DUPLICATE: True,
    FT_BAN_SYMBOLS_STR: [],

    FT_MIN_LEN_STR: GB_USER_NAME_MIN_LEN,
    FT_MAX_LEN_STR: GB_USER_NAME_MAX_LEN,

    # 排除规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXCLUDE_RULES_STR: [
        (0, 0, 0, 1, 0),  # 排除纯符号
        (-1, 1, -1, -1, 1),  # 排除中英文混合 有大写+中文
        (-1, -1, 1, -1, 1),  # 排除中英文混合 有小写+中文
    ],
    # 提取规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXTRACT_RULES_STR: [],
    # 正则排除
    FT_EXCLUDE_REGEX_STR: [],
    # 正则提取
    FT_EXTRACT_REGEX_STR: [],
}
#######################
# 排除列表 排除密码的配置
# GB_FILTER_OPTIONS_PASS = copy.copy(FILTER_STRING_OPTIONS)
GB_FILTER_OPTIONS_PASS = {
    FT_IGNORE_SYMBOLS: GB_IGNORE_SYMBOLS,
    FT_IGNORE_EMPTY: GB_IGNORE_EMPTY,

    FT_NO_DUPLICATE: True,
    FT_BAN_SYMBOLS_STR: [],

    FT_MIN_LEN_STR: GB_USER_PASS_MIN_LEN,
    FT_MAX_LEN_STR: GB_USER_PASS_MAX_LEN,

    # 排除规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXCLUDE_RULES_STR: [
        (0, 0, 0, 1, 0),  # 排除仅符号
        (0, 1, 0, 0, 0),  # 排除仅大写
        (0, 1, 0, 1, 0),  # 排除仅大写+符号
        (-1, 1, -1, -1, 1),  # 排除中英文混合 必须有大写+中文
        (-1, -1, 1, -1, 1),  # 排除中英文混合 必须有小写+中文
    ],

    # 提取规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXTRACT_RULES_STR: [],
    # 正则排除
    FT_EXCLUDE_REGEX_STR: [],
    # 正则提取
    FT_EXTRACT_REGEX_STR: [],
}
#######################
# 对生成的账号|密码元组进行排除的选项配置
# 排除元组 通过长度
# GB_FILTER_TUPLE_OPTIONS = copy.copy(FILTER_TUPLE_OPTIONS)
GB_FILTER_TUPLE_OPTIONS = {
    FT_IGNORE_SYMBOLS: GB_IGNORE_SYMBOLS,
    FT_IGNORE_EMPTY: GB_IGNORE_EMPTY,

    FT_NO_DUPLICATE: True,

    FT_BAN_SYMBOLS_NAME: [],
    FT_BAN_SYMBOLS_PASS: [],

    FT_MAX_LEN_NAME: GB_USER_NAME_MAX_LEN,
    FT_MIN_LEN_NAME: GB_USER_NAME_MIN_LEN,
    FT_MAX_LEN_PASS: GB_USER_PASS_MAX_LEN,
    FT_MIN_LEN_PASS: GB_USER_PASS_MIN_LEN,

    # 排除规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXCLUDE_RULES_NAME: [
        (0, 0, 0, 1, 0),  # 排除纯符号
    ],
    FT_EXCLUDE_RULES_PASS: [
        (0, 0, 0, 1, 0),  # 排除仅符号
        (0, 1, 0, 0, 0),  # 排除仅大写
        (0, 1, 0, 1, 0),  # 排除仅大写+符号
        (-1, 1, -1, -1, 1),  # 排除中英文混合 必须有大写+中文
        (-1, -1, 1, -1, 1),  # 排除中英文混合 必须有小写+中文
    ],

    # 提取规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXTRACT_RULES_NAME: [],
    FT_EXTRACT_RULES_PASS: [],

    # 正则排除
    FT_EXCLUDE_REGEX_NAME: [],
    FT_EXCLUDE_REGEX_PASS: [],
    # 正则提取
    FT_EXTRACT_REGEX_NAME: [],
    FT_EXTRACT_REGEX_PASS: [],
}
############################################################
# 对密码中的用户名替换时候的一些选项
# GB_SOCIAL_USER_OPTIONS_DICT = copy.copy(SOCIAL_USER_OPTIONS_DICT)
GB_SOCIAL_USER_OPTIONS_DICT = {
    SO_NAME_CASE: [ATTR_LOWER],  # 用户名大小写处理
    SO_NAME_KEEP: False,  # 当开启用户名格式处理时,依旧保留原始用户名

    SO_PASS_CASE: [],  # 密码用户名 大小写处理 （如果密码中有用户名 就密码内的 用户名全部大小写处理,否则就密码整体全部大小写处理）
    SO_PASS_KEEP: False,  # 当开启密码格式处理时,依旧保留原始密码

    SO_PASS_REVERSE: False,  # 增加用户名的反向序列作为密码
    SO_ONLY_MARK_PASS: False  # 仅对 密码中包含用户名变量的密码 进行以上操作
}
############################################################
# GB_SOCIAL_PASS_OPTIONS_DICT = copy.copy(SOCIAL_PASS_OPTIONS_DICT)
GB_SOCIAL_PASS_OPTIONS_DICT = {
    SO_PASS_KEEP: True,  # 对密码进行格式化时, 保留原始密码
    SO_PASS_REPL: [  # 密码字符替换
        # {"o": "0"},
        # {"o": "@"},
    ],
    SO_PASS_SEGMENT: [  # 密码字母按段索引大小写
        # {0: "upper"},
        # {1: "upper"},
        # {0: "upper", 1: ATTR_UPPER},
        # {0: "upper", 2: ATTR_UPPER},
        # {0: ATTR_UPPER, "*": ATTR_LOWER},
    ],
    SO_PASS_INDEXED: [  # 密码字母按字母索引大小写
        # {1:ATTR_UPPER,"*":ATTR_LOWER},
        # {0: "upper", "*": "lower"},
        # {-1: ATTR_UPPER, "*": "u"},
    ],
}
############################################################
# 最后爆破时，对中文账号密码进行进行中文编码
GB_CHINESE_ENCODE_CODING = ["utf-8"]  # 可选 ["utf-8","gb2312","unicode_escape"]
GB_CHINESE_CHAR_URLENCODE = True  # 对中文编码时操作、同时进行URL编码
GB_ONLY_CHINESE_URL_ENCODE = True  # 仅对包含中文的字符串进行中文及URL编码操作
############################################################
