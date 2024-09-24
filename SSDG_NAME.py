#!/usr/bin/env python
# encoding: utf-8

import setting_com
import setting_dict
from libs.lib_args.input_basic import config_dict_add_args
from libs.lib_args.input_const import *
from libs.lib_args.input_parse import args_parser_name
from libs.lib_attribdict.config import CONFIG
from libs.lib_chinese_pinyin.chinese_list_to_alphabet_list import dict_chinese_value_to_alphabet
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str, remove_not_used_key
from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list
from libs.lib_dyna_rule.set_basic_var import set_base_var_dict
from libs.lib_dyna_rule.set_depend_var import set_dependent_var_dict
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_line
from libs.lib_filter_srting.filter_string_call import filter_string_list
from libs.lib_log_print.logger_printer import set_logger, output, LOG_INFO, LOG_ERROR, LOG_DEBUG
from libs.lib_tags_exec.tags_const import TAG_FUNC_DICT
from libs.lib_tags_exec.tags_exec import match_exec_repl_loop_batch
from libs.utils import select_files_by_level


# 分割写法 基于 用户名和密码规则生成 元组列表
def generate_social_dict_for_name(config_dict, name_rule_files):
    mode = "NAME"
    step = 0

    NAME_LIST = []
    output(f"[*] 读取账号规则文件: {name_rule_files}...", level=LOG_INFO)
    for index, name_file in enumerate(name_rule_files):
        output(f"[*] 读取账号规则文件: {index + 1}/{len(name_rule_files)} -> {name_rule_files}...", level=LOG_DEBUG)
        lines = read_file_to_list(name_file, encoding=file_encoding(name_file), de_strip=True, de_weight=True)
        NAME_LIST.extend(lines)

    if not NAME_LIST:
        output(f"[!] 未输入任何有效账号规则文件!!!", level=LOG_ERROR)
        return []

    # 保持原始顺序去重
    NAME_LIST = [x for i, x in enumerate(NAME_LIST) if x not in NAME_LIST[:i]]
    output(f"[*] 读取账号规则文件 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)

    # 动态规则解析
    if True:
        NAME_LIST, render_count, run_time = base_rule_render_list(NAME_LIST)
        output(f"[*] 账号规则 动态规则解析完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)

        # 进行账号规则格式化
        NAME_LIST = filter_string_list(string_list=NAME_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        output(f"[*] 账号规则 账号格式过滤完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.基本渲染.txt"), NAME_LIST)

    # 基本变量替换处理
    if True:
        # 获取基本变量字典
        base_var_replace_dict = set_base_var_dict(
            config_dict[GB_BASE_VAR_DIR],
            config_dict[GB_BASE_DICT_SUFFIX],
            config_dict[GB_BASE_VAR_REPLACE_DICT]
        )
        output(f"[*] 目录 GB_BASE_VAR_DIR 变量替换字典 加载完成:{len(str(base_var_replace_dict))}")

        # 获取动态变量字典
        base_var_replace_dict = set_base_var_dict(
            config_dict[GB_BASE_DYNA_DIR],
            config_dict[GB_BASE_DICT_SUFFIX],
            base_var_replace_dict
        )
        output(f"[*] 目录 GB_BASE_DYNA_DIR 变量替换字典 加载完成:{len(str(base_var_replace_dict))}...")

        # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
        NAME_REPLACE_DICT = set_base_var_dict(
            config_dict[GB_BASE_NAME_DIR],
            config_dict[GB_BASE_DICT_SUFFIX],
            base_var_replace_dict
        )
        output(f"[*] 目录 GB_BASE_NAME_DIR 变量替换字典 加载完成:{len(str(NAME_REPLACE_DICT))}")

        # 删除不会被用到规则用到的基本变量替换字典的键
        raw_size = len(NAME_REPLACE_DICT)
        NAME_REPLACE_DICT = remove_not_used_key(NAME_REPLACE_DICT, NAME_LIST)
        output(f"[*] 去除未被使用的替换变量 NAME_REPLACE_DICT:{raw_size} -> {len(str(NAME_REPLACE_DICT))}")

        # 对变量替换字典中的值【列表】进行中文处理 # 也可以通过在后面再进行替换,但是后面生成的结果太多,比较费内存
        if config_dict[GB_CHINESE_TO_PINYIN]:
            raw_size = len(NAME_REPLACE_DICT)
            NAME_REPLACE_DICT = dict_chinese_value_to_alphabet(
                replace_dict=NAME_REPLACE_DICT,
                options_dict=config_dict[GB_CHINESE_OPTIONS_NAME],
                store_chinese=config_dict[GB_STORE_CHINESE]
            )
            output(f"[*] 变量替换字典中文转换完成 NAME_REPLACE_DICT:{raw_size} -> {len(str(NAME_REPLACE_DICT))}", level=LOG_INFO)

        # 对字典规则进行变量替换
        NAME_LIST, replace_count, running_time = replace_list_has_key_str(NAME_LIST, NAME_REPLACE_DICT)
        output(f"[*] 字典规则变量替换完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)
        # 进行格式化
        NAME_LIST = filter_string_list(string_list=NAME_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        output(f"[*] 列表过滤格式化完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.变量替换.txt"), NAME_LIST)

    # 因变量替换处理
    if True:
        # 获取因变量
        DEPENDENT_REPLACE_DICT = set_dependent_var_dict(
            target_url=config_dict[GB_TARGET],
            base_dependent_dict=config_dict[GB_DEPENDENT_VAR_REPLACE_DICT],
            ignore_ip_format=config_dict[GB_IGNORE_IP_FORMAT],
            symbol_replace_dict=config_dict[GB_SYMBOL_REPLACE_DICT],
            not_allowed_symbol=config_dict[GB_NOT_ALLOW_SYMBOL]
        )
        output(f"[*] 加载因变量完成 DEPENDENT_REPLACE_DICT:{DEPENDENT_REPLACE_DICT}")

        # 清空没有被使用的键
        raw_size = len(DEPENDENT_REPLACE_DICT)
        DEPENDENT_REPLACE_DICT = remove_not_used_key(DEPENDENT_REPLACE_DICT, [NAME_LIST])
        output(f"[*] 去除未被使用的替换变量 DEPENDENT_REPLACE_DICT:{raw_size} -> {len(str(DEPENDENT_REPLACE_DICT))}")

        # 因变量替换
        NAME_LIST, _, _ = replace_list_has_key_str(NAME_LIST, DEPENDENT_REPLACE_DICT)
        output(f"[*] 因变量替换完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...")
        # 进行格式化
        NAME_LIST = filter_string_list(string_list=NAME_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        output(f"[*] 格式过滤完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.因变量替换.txt"), NAME_LIST)

    if True:
        # 调用tag exec来进行操作,实现字符串反序 实现1221等格式
        NAME_LIST = match_exec_repl_loop_batch(NAME_LIST, TAG_FUNC_DICT)
        output(f"[*] 标签处理完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)
        # 进行格式化
        NAME_LIST = filter_string_list(string_list=NAME_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        output(f"[*] 格式过滤完成 name_list:{len(NAME_LIST)} <--> {NAME_LIST[:10]} ...", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.标签处理.txt"), NAME_LIST)

    return NAME_LIST


def actions_controller(config_dict):
    # 根据level参数和GB_RULE_LEVEL_EXACT设置修改字典路径
    selected_name_rule_files = select_files_by_level(
        filen_path_format=config_dict[GB_NAME_FILE_STR],
        replace_value=config_dict[GB_RULE_LEVEL_NAME],
        rule_exact=config_dict[GB_RULE_LEVEL_EXACT]
    )
    output(f"[*] 本次调用的账号规则文件: {selected_name_rule_files}", level=LOG_INFO)

    name_dict = generate_social_dict_for_name(
        config_dict=config_dict,
        name_rule_files=selected_name_rule_files
    )
    output(f"[*] 最终生成账号数量: {len(name_dict)}", level=LOG_INFO)


if __name__ == '__main__':
    # 加载初始设置参数
    setting_com.init_common(CONFIG)
    setting_com.init_custom(CONFIG)
    setting_dict.init_custom(CONFIG)

    # 设置默认debug参数日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], True)

    # 输入参数解析
    args = args_parser_name(CONFIG)
    output(f"[*] 输入参数信息: {args}")

    # 将输入参数加入到全局CONFIG
    config_dict_add_args(CONFIG, args)

    # 根据用户输入的debug参数设置日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], CONFIG[GB_DEBUG_FLAG])

    # 输出所有参数信息
    output(f"[*] 最终配置信息: {CONFIG}", level=LOG_DEBUG)
    # show_config_dict(CONFIG)

    # 进行字典伸出
    actions_controller(CONFIG)
