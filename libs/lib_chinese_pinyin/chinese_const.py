# -*- coding: utf-8 -*-
from pypinyin import Style

######################################
# 定义一些通用常量
from libs.lib_run_str_attr.str_attr_const import *

STYLE_NORMAL = Style.NORMAL  # 返回完整拼音 （"中文"-> ["zhong", "wen"]）
STYLE_FIRST = Style.FIRST_LETTER  # 返回首字母 （"中文" -> ["z", "w"]）
STYLE_INITIALS = Style.INITIALS  # 返回声母部分 无声母用首字母补充 （ "中文"-> ["zh", "w"]）
ALLOWED_STYLES = [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS]
######################################
PY_OPTIMIZED = "PY_OPTIMIZED"  # 已优化
PY_TEMP_SYMBOL = "PY_TEMP_SYMBOL"  # 连接字符串,不会对其他数据有影响, 使用下划线即可
######################################
# 专业术语字典优化选项
PY_SY_CASE = "PY_SY_CASE"  # 专业术语字典的拼音大小写处理
######################################
# 基于中文词汇、中文姓名转拼音的处理 相关的常量

# 设置中文名字的最大长度 大于这个长度的不作为名字考虑
PY_CN_NAME_MAX_LEN = "PY_CN_NAME_MAX_LEN"

# 是否使用结巴分词
PY_CN_USE_JIEBA = "PY_CN_USE_JIEBA"

# 基本的词汇生成
PY_POSITIVE = "PY_POSITIVE"  # 通用的姓名处理,需要默认开启  当解析出姓、名的时候进行
PY_REVERSE = "PY_REVERSE"  # 额外的姓名处理，倒序安装姓名  当解析出姓、名的时候可选
PY_UNIVERS = "PY_UNIVERS"  # 通用的词汇处理,需要默认开启 当没有解析出姓、名的时候进行

# 额外的词汇生成
PY_XM2CH = "PY_XM2CH"  # 把姓名也当作词汇，再作做一遍字典生成
PY_CH2XM = "PY_CH2XM"  # 把词汇也当做姓名处理,第一个字作为姓氏处理 （小于2的长度的好像没有意义,需要测试）

# 普通词汇的 基本拼接元素的生成
PY_UNI_STYLES = "PY_UNI_STYLES"

# 对 普通词汇的 每个组合的姓名字典做大小写等处理
PY_UNI_CASE = "PY_UNI_CASE"
######################################
# 姓名的姓氏的 基本拼接元素的生成
PY_XIN_STYLES = "PY_XIN_STYLES"

# 姓名的名字的  每个组合的姓名字典做大小写等处理
PY_XIN_CASE = "PY_XIN_CASE"
##################
# 姓名的姓氏的 基本拼接元素的生成
PY_MIN_STYLES = "PY_MIN_STYLES"

# 姓名的名字的  每个组合的姓名字典做大小写等处理
PY_MIN_CASE = "PY_XIN_CASE"
######################################
# 中文转换结果的最后处理选项
PY_FT_NO_BLANK = "PY_FT_NO_BLANK"  # 去空格
PY_FT_NO_DUPL = "PY_FT_NO_DUPL"  # 去重复
PY_FT_MAX_LEN = "PY_FT_MAX_LEN"  # 生成的拼音长度不大于这个选项
PY_IGNORE_SYMBOL = "PY_IGNORE_SYMBOL"  # 忽略对包含指定字符的字符串的过滤,主要是担心影响存在基本|因变量
######################################
# 用于连接拼音之间的字符串 会影响一倍的结果
PY_LINK_SYMBOLS = "PY_LINK_SYMBOLS"
######################################
# 参考的配置选项字典
PY_MAX_OPTIONS = {
    PY_TEMP_SYMBOL: "_",
    PY_LINK_SYMBOLS: ["_", ".", ""],
    PY_CN_NAME_MAX_LEN: 4,

    PY_SY_CASE: [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

    PY_CN_USE_JIEBA: True,
    PY_POSITIVE: True,
    PY_REVERSE: True,
    PY_UNIVERS: True,
    PY_XM2CH: True,
    PY_CH2XM: True,

    PY_FT_NO_BLANK: True,
    PY_FT_NO_DUPL: True,
    PY_FT_MAX_LEN: 12,
    PY_IGNORE_SYMBOL: ["%%", "%", "}$"],

    PY_UNI_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_UNI_CASE: [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

    PY_XIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_XIN_CASE: [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

    PY_MIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_MIN_CASE: [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],
}

PY_BASE_OPTIONS = {
    PY_TEMP_SYMBOL: "_",
    PY_LINK_SYMBOLS: [""],
    PY_CN_NAME_MAX_LEN: 4,

    PY_SY_CASE: [ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

    PY_CN_USE_JIEBA: False,

    PY_POSITIVE: True,
    PY_REVERSE: True,
    PY_UNIVERS: True,

    PY_XM2CH: False,
    PY_CH2XM: False,

    PY_FT_NO_BLANK: True,
    PY_FT_NO_DUPL: True,
    PY_FT_MAX_LEN: 12,
    PY_IGNORE_SYMBOL: ["%%", "%", "}$"],

    PY_UNI_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_UNI_CASE:  [ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

    PY_XIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_XIN_CASE:  [ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

    PY_MIN_STYLES: [STYLE_NORMAL, STYLE_FIRST, STYLE_INITIALS],

    PY_MIN_CASE: [ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],

}
######################################
if __name__ == '__main__':
    # 获取当前作用域中的所有变量名
    variables = list(locals().keys())
    variables = [key for key in variables if not key.startswith("_")]
    print(variables)
