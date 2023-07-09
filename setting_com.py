#!/usr/bin/env python
# encoding: utf-8
# 全局配置文件
# 输入原始报文路径
import time
from pathlib import Path
from libs.input_const import *
from libs.lib_file_operate.file_path import auto_make_dir


def init_common(config):
    """
    初始化本程序的通用参数
    :param config:
    :return:
    """
    ##################################################################
    # 获取setting.py脚本所在路径作为的基本路径
    config[GB_BASE_DIR] = Path(__file__).parent.resolve()
    ##################################################################
    # 程序开始运行时间
    config[GB_RUN_TIME] = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    ##################################################################
    # 版本号配置
    config[GB_VERSION] = "Ver 0.0.2 2023-07-09 01:30"
    ##################################################################
    # 是否显示DEBUG级别信息,默认False
    config[GB_DEBUG_FLAG] = False
    ##################################################################
    # 设置日志输出文件路径 #目录不存在会自动创建
    config[GB_LOG_INFO_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_info.log").as_posix()
    config[GB_LOG_DEBUG_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_debug.log").as_posix()
    config[GB_LOG_ERROR_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_error.log").as_posix()


def init_custom(config):
    ##################################################################
    # 设置输出结果文件目录
    config[GB_RESULT_DIR] = config[GB_BASE_DIR].joinpath("result")
    auto_make_dir(config[GB_RESULT_DIR])
    # 指定记录字典文件的目录
    config[GB_TEMP_DICT_DIR] = config[GB_RESULT_DIR].joinpath(f"dict.{config[GB_RUN_TIME]}")
    auto_make_dir(config[GB_TEMP_DICT_DIR])
    ##################################################################
    # 增加标签处理功能,便于对标记的数据自动进行（加密|编码）操作
    # 目前支持功能请查看 libs/lib_tags_exec/tags_const.py 的 TAG_FUNC_DICT
    # 标签执行时调用的自定义js文件路径
    config[TAG_EXEC_CUSTOM_JS_FILE] = r"libs/lib_tags_exec/demo/custom.js"
    # 标签执行时调用的自定义py文件路径
    config[AG_EXEC_CUSTOM_PY_FILE] = r"libs/lib_tags_exec/demo/custom.py"
    ##################################################################
    # 最后对中文账号密码进行进行中文编码
    config[GB_CHINESE_ENCODE_CODING] = ["utf-8"]  # 可选 ["utf-8","gb2312","unicode_escape"]
    config[GB_CHINESE_CHAR_URLENCODE] = True  # 对中文编码时操作、同时进行URL编码
    config[GB_ONLY_CHINESE_URL_ENCODE] = True  # 仅对包含中文的字符串进行中文及URL编码操作
    ############################################################
