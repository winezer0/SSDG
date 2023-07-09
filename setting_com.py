#!/usr/bin/env python
# encoding: utf-8
# 全局配置文件
# 输入原始报文路径

from libs.lib_file_operate.file_path import auto_make_dir
from setting_dict import *

##################################################################
# 版本号配置
GB_VERSION = "Ver 0.0.1 2023-07-09 23:30"
##################################################################
# 程序开始运行时间  %Y-%m-%d-%H-%M-%S
GB_RUN_TIME = time.strftime("%Y-%m-%d", time.localtime())
##################################################################
# 是否显示DEBUG级别信息,默认False
GB_DEBUG_FLAG = True
##################################################################
# 仅生成字典,不进行爆破
GB_ONLY_GENERATE_DICT = False
##################################################################
# 增加标签处理功能,便于对标记的数据自动进行（加密|编码）操作
# 目前支持功能请查看 libs/lib_tags_exec/tags_const.py 的 TAG_FUNC_DICT
# 标签执行时调用的自定义js文件路径
TAG_EXEC_CUSTOM_JS_FILE = r"libs/lib_tags_exec/demo/custom.js"
# 标签执行时调用的自定义py文件路径
TAG_EXEC_CUSTOM_PY_FILE = r"libs/lib_tags_exec/demo/custom.py"
##################################################################
# 设置日志输出文件路径 #目录不存在会自动创建
GB_LOG_FILE_DIR = GB_BASE_DIR.joinpath("runtime")
GB_INFO_LOG_FILE = GB_BASE_DIR.joinpath("runtime", 'runtime_info.log').as_posix()
GB_DBG_LOG_FILE = GB_BASE_DIR.joinpath("runtime", 'runtime_debug.log').as_posix()
GB_ERR_LOG_FILE = GB_BASE_DIR.joinpath("runtime", 'runtime_error.log').as_posix()
############################################################
# 一些创建目录的操作
auto_make_dir(GB_RESULT_DIR)
auto_make_dir(GB_TEMP_DICT_DIR)
############################################################
