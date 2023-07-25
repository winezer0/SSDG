#!/usr/bin/env python
# encoding: utf-8

import inspect

######################################################
# 默认参数相关
GB_BASE_DIR = ""
GB_RUN_TIME = ""
GB_VERSION = ""
GB_DEBUG_FLAG = ""
# 日志路径相关
GB_LOG_INFO_FILE = ""
GB_LOG_DEBUG_FILE = ""
GB_LOG_ERROR_FILE = ""
# 结果路径相关
GB_RESULT_DIR = ""
GB_TEMP_DICT_DIR = ""
######################################################
# 自定义输入参数相关
GB_TARGET = ""  # 指定获取域名因变量的域名
######################################################
GB_DEFAULT_NAME_LIST = ""
GB_DEFAULT_PASS_LIST = ""
######################################################
# 最后对中文账号密码进行进行中文编码
GB_CHINESE_ENCODE_CODING = ""
GB_CHINESE_CHAR_URLENCODE = ""
GB_ONLY_CHINESE_URL_ENCODE = ""
######################################################
# 排除历史爆破记录的功能
GB_EXCLUDE_FLAG = None
GB_EXCLUDE_FILE = None
GB_CONST_LINK = None
# 基本变量文件夹
GB_BASE_VAR_DIR = None
GB_BASE_DYNA_DIR = None
GB_BASE_NAME_DIR = None
GB_BASE_PASS_DIR = None
GB_BASE_DICT_SUFFIX = None
############################################################
GB_BASE_VAR_REPLACE_DICT = None  # 存储 自定义 基本变量
GB_DEPENDENT_VAR_REPLACE_DICT = None  # 存储 自定义 因变量

GB_SYMBOL_REPLACE_DICT = None  # 符号替换规则
GB_NOT_ALLOW_SYMBOL = None  # 删除带有 特定符号 的因变量（比如:）的元素
GB_IGNORE_IP_FORMAT = None  # 忽略IP格式的域名
############################################################
# 指定用户名变量字符串 # 在密码字典中用这个变量表示用户名
GB_USER_NAME_MARK = None
# 账号密码目录
GB_RULE_DICT_DIR = None
# 账号密码文件标记字符串
GB_NAME_FILE_STR = None
GB_PASS_FILE_STR = None
# 账号密码对文件命名格式
GB_PAIR_FILE_STR = None
# 实际调用的字典级别设置
GB_RULE_LEVEL_NAME = None
GB_RULE_LEVEL_PASS = None
GB_RULE_LEVEL_PAIR = None
GB_RULE_LEVEL_EXACT = None
# 账号密码对文件 连接符号
GB_PAIR_LINK_SYMBOL = None
# 使用账号:密码对文件进行爆破
GB_USE_PAIR_FILE = None
# 使用账号:密码对文件进行时,是否进行基本变量替换
GB_USE_PAIR_BASE_REPL = None
# 用户名中的中文转拼音处理
GB_CHINESE_TO_PINYIN = None  # 开启中文转拼音的操作
GB_STORE_CHINESE = None  # 保留原始的中文字符串
GB_IGNORE_SYMBOLS = None  # 忽略包含符号的字符串
# 中文转拼音处理时，通过长度对最后的（账号:密码）进行过滤的依据
GB_USER_NAME_MIN_LEN = None  # 用户名最小长度（含）
GB_USER_NAME_MAX_LEN = None  # 用户名最大长度（含）
GB_USER_PASS_MIN_LEN = None  # 密码最小长度（含）
GB_USER_PASS_MAX_LEN = None  # 密码最大长度（含）

# 中文处理方案
GB_CHINESE_OPTIONS_NAME = ""  # 对账号中依赖的中文处理方案
GB_CHINESE_OPTIONS_PASS = ""  # 对密码中依赖的中文处理方案
GB_CHINESE_OPTIONS_TUPLE = ""  # 对元组列表处理时的配置字典

# 对生成的账号|密码列表进行排除的选项配置
GB_IGNORE_EMPTY = ""  # 进行格式过滤时保留空值[""]

GB_FILTER_OPTIONS_NAME = ""  # 排除列表 排除姓名的配置
GB_FILTER_OPTIONS_PASS = ""  # 排除列表 排除密码的配置
GB_FILTER_TUPLE_OPTIONS = ""  # 排除列表 排除元组

GB_SOCIAL_USER_OPTIONS_DICT = ""  # 对密码中的用户名替换时候的一些选项
GB_SOCIAL_PASS_OPTIONS_DICT = ""  # 对密码中进行过滤的一些选项


############################################################


# 实现自动更新全局变量名和对应值
def update_global_vars(startswith="GB_", require_blank=True, debug=False):
    # 修改所有全局变量名的值为变量名字符串
    # 当前本函数必须放置到本目录内才行

    def get_var_string(variable):
        # 自动根据输入的变量,获取变量名的字符串
        # 获取全局变量字典
        global_vars = globals()

        # 遍历全局变量字典
        for name, value in global_vars.items():
            if value is variable:
                # print(f"[*] global_vars <--> {variable} <--> {name} <--> {value}")
                return name

        # 获取局部变量字典
        local_vars = locals()
        # 遍历局部变量字典
        for name, value in local_vars.items():
            if value is variable:
                # print(f"[*] local_vars <--> {variable} <--> {name} <--> {value}")
                return name

        return None  # 如果未找到对应的变量名，则返回 None

    def get_global_var_names():
        # 获取本文件所有全局变量名称, 排除函数名等
        global_var_names = list(globals().keys())
        # 获取当前文件中定义的所有函数列表
        current_module = inspect.getmodule(inspect.currentframe())
        functions = inspect.getmembers(current_module, inspect.isfunction)
        function_names = [f[0] for f in functions]
        # 在本文件所有全局变量排除函数列表
        global_var_names = [name for name in global_var_names
                            if name not in function_names  # 排除内置函数名
                            and name.count("__") < 2  # 排除内置__name__等变量
                            and name != "inspect"  # 排除内置inspect包的变量
                            ]

        # 仅处理以 startswith 开头的变量
        if startswith:
            global_var_names = [name for name in global_var_names if name.startswith(startswith)]

        return global_var_names

    for variable_name in get_global_var_names():
        # 仅处理空变量
        if require_blank and globals()[variable_name]:
            if debug:
                print(f"跳过 Name:{variable_name} <--> Value: {globals()[variable_name]}")
            continue

        globals()[variable_name] = "NONE"
        globals()[variable_name] = get_var_string(globals()[variable_name])
        if debug:
            print(f"更新 Name:{variable_name} <--> Value: {globals()[variable_name]}")


# 自动更新变量的值为变量名字符串 # 必须放在末尾
update_global_vars(startswith="GB_", require_blank=True, debug=False)
