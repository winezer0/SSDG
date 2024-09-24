#!/usr/bin/env python
# encoding: utf-8

import setting_com
import setting_dict
from libs.lib_args.input_const import *
from libs.lib_args.input_parse_pass import args_parser, args_dict_handle, config_dict_handle
from libs.lib_args.input_basic import config_dict_add_args
from libs.lib_attribdict.config import CONFIG
from libs.lib_chinese_encode.chinese_encode import tuple_list_chinese_encode_by_char
from libs.lib_chinese_pinyin.chinese_list_to_alphabet_list import dict_chinese_value_to_alphabet
from libs.lib_collect_opera.list_operate import cartesian_product_merging
from libs.lib_collect_opera.tuple_operate import frozen_tuples, tuples_subtract, unfrozen_tuples
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str, remove_not_used_key
from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list
from libs.lib_dyna_rule.set_basic_var import set_base_var_dict
from libs.lib_dyna_rule.set_depend_var import set_dependent_var_dict
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_utils import file_is_empty
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_line
from libs.lib_filter_srting.filter_string_call import filter_string_list, filter_tuple_list
from libs.lib_log_print.logger_printer import set_logger, output, LOG_INFO, LOG_ERROR, LOG_DEBUG
from libs.lib_social_dict.repl_mark_user import replace_mark_user_on_pass
from libs.lib_social_dict.transfer_passwd import transfer_passwd
from libs.lib_tags_exec.tags_const import TAG_FUNC_DICT
from libs.lib_tags_exec.tags_exec import match_exec_repl_loop_batch
from libs.utils import select_files_by_level


# 分割写法 基于 用户名和密码规则生成 元组列表
def generate_social_dict_for_pass(config_dict, name_files, pass_rule_files):
    mode = "PASS"  # 与字典文件命名相关, 不建议修改
    step = 0

    # 读取账号文件
    name_list = []
    if name_files:
        output(f"[*] 读取账号字典文件 {name_files}...", level=LOG_INFO)
        if isinstance(name_files, str):
            name_files = [name_files]
        for name_file in name_files:
            lines = read_file_to_list(name_file, encoding=file_encoding(name_file), de_strip=True, de_weight=True)
            name_list.extend(lines)

    # 保持原始顺序去重
    name_list = [x for i, x in enumerate(name_list) if x not in name_list[:i]]
    output(f"[*] 读取账号文件完成 name_list:{len(name_list)} <--> {name_list[:10]}", level=LOG_INFO)

    # 读取密码规则文件
    PASS_LIST = []
    output(f"[*] 读取密码字典文件 {pass_rule_files}...", level=LOG_INFO)
    for pass_file in pass_rule_files:
        lines = read_file_to_list(pass_file, encoding=file_encoding(pass_file), de_strip=True, de_weight=True)
        PASS_LIST.extend(lines)

    # 保持原始顺序去重
    if not PASS_LIST:
        output(f"[!] 未输入任何有效密码字典文件!!!", level=LOG_ERROR)
        return []

    PASS_LIST = [x for i, x in enumerate(PASS_LIST) if x not in PASS_LIST[:i]]
    output(f"[*] 读取密码文件完成 pass_list:{len(PASS_LIST)} <--> {PASS_LIST[:10]}", level=LOG_INFO)

    if True:
        # 动态规则解析
        PASS_LIST, render_count, run_time = base_rule_render_list(PASS_LIST)
        output(f"[*] 密码规则 动态规则解析完成 pass_list:{len(PASS_LIST)}", level=LOG_INFO)

        # 进行格式化
        PASS_LIST = filter_string_list(string_list=PASS_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 密码规则 密码格式过滤完成  pass_list:{len(PASS_LIST)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.基本渲染.txt"), PASS_LIST)

    # 基本变量替换处理
    if True:
        # 获取基本变量字典
        base_var_replace_dict = set_base_var_dict(
            config_dict[GB_BASE_VAR_DIR],
            config_dict[GB_BASE_DICT_SUFFIX],
            config_dict[GB_BASE_VAR_REPLACE_DICT]
        )
        output(f"[*] 目录 GB_BASE_VAR_DIR 变量替换字典 加载完成:{len(str(base_var_replace_dict))}")

        base_var_replace_dict = set_base_var_dict(
            config_dict[GB_BASE_DYNA_DIR],
            config_dict[GB_BASE_DICT_SUFFIX],
            base_var_replace_dict
        )
        output(f"[*] 目录 GB_BASE_DYNA_DIR 变量替换字典 加载完成:{len(str(base_var_replace_dict))}...")

        PASS_REPLACE_DICT = set_base_var_dict(
            config_dict[GB_BASE_PASS_DIR],
            config_dict[GB_BASE_DICT_SUFFIX],
            base_var_replace_dict
        )
        output(f"[*] 目录 GB_BASE_PASS_DIR 变量替换字典 加载完成:{len(str(PASS_REPLACE_DICT))}")

        # 删除不会被用到规则用到的基本变量替换字典的键
        raw_size = len(PASS_REPLACE_DICT)
        PASS_REPLACE_DICT = remove_not_used_key(PASS_REPLACE_DICT, PASS_LIST)
        output(f"[*] 去除未被使用的替换变量 NAME_REPLACE_DICT:{raw_size} -> {len(str(PASS_REPLACE_DICT))}")

        # 对变量替换字典中的值【列表】进行中文处理 # 也可以通过在后面再进行替换,但是后面生成的结果太多,比较费内存
        if config_dict[GB_CHINESE_TO_PINYIN]:
            PASS_REPLACE_DICT = dict_chinese_value_to_alphabet(
                replace_dict=PASS_REPLACE_DICT,
                options_dict=config_dict[GB_CHINESE_OPTIONS_PASS],
                store_chinese=config_dict[GB_STORE_CHINESE]
            )
            output(f"[*] 变量替换字典中文转换完成 PASS_REPLACE_DICT:{raw_size} -> {len(str(PASS_REPLACE_DICT))}", level=LOG_INFO)

        # 对字典规则进行变量替换
        PASS_LIST, replace_count, running_time = replace_list_has_key_str(PASS_LIST, PASS_REPLACE_DICT)
        output(f"[*] 基本变量替换完成 pass_list:{len(PASS_LIST)}", level=LOG_INFO)
        # 进行格式化
        PASS_LIST = filter_string_list(string_list=PASS_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 列表过滤格式化完成 pass_list:{len(PASS_LIST)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.变量替换.txt"), PASS_LIST)

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
        DEPENDENT_REPLACE_DICT = remove_not_used_key(DEPENDENT_REPLACE_DICT, [PASS_LIST])
        output(f"[*] 去除未被使用的替换变量 DEPENDENT_REPLACE_DICT:{raw_size} -> {len(str(DEPENDENT_REPLACE_DICT))}")

        # 因变量替换
        PASS_LIST, _, _ = replace_list_has_key_str(PASS_LIST, DEPENDENT_REPLACE_DICT)
        output(f"[*] 因变量替换完成 pass_list:{len(PASS_LIST)}")
        # 进行格式化
        PASS_LIST = filter_string_list(string_list=PASS_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 格式过滤完成 pass_list:{len(PASS_LIST)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.因变量替换.txt"), PASS_LIST)

    if True:
        # 调用tag exec来进行操作,实现字符串反序 实现1221等格式
        PASS_LIST = match_exec_repl_loop_batch(PASS_LIST, TAG_FUNC_DICT)
        output(f"[*] 标签处理完成 name_list:{len(PASS_LIST)} <--> {PASS_LIST[:10]} ...", level=LOG_INFO)
        # 进行格式化
        PASS_LIST = filter_string_list(string_list=PASS_LIST, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 列表过滤格式化完成 pass_list:{len(PASS_LIST)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.标签处理.txt"), PASS_LIST)

    # 未输入用户名字典,直接返回密码列表
    if not name_list:
        return PASS_LIST

    # 组合用户名列表和密码列表
    if True:
        PAIR_LIST = cartesian_product_merging(name_list, PASS_LIST)
        output(f"[*] 账号密码组合完成 :{len(PAIR_LIST)}", level=LOG_INFO)
        # 进行格式化
        PAIR_LIST = filter_tuple_list(
            tuple_list=PAIR_LIST,
            options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS]
        )
        output(f"[*] 元组格式过滤完成 PAIR_LIST:{len(PAIR_LIST)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.笛卡尔积.txt"),
                   frozen_tuples(PAIR_LIST, link_symbol=config_dict[GB_CONST_LINK]))

    # 对基于用户名变量的密码做替换处理
    if True:
        PAIR_LIST = replace_mark_user_on_pass(
            PAIR_LIST,
            mark_string=config_dict[GB_USER_NAME_MARK],
            options_dict=config_dict[GB_SOCIAL_USER_OPTIONS_DICT]
        )
        output(f"[*] 账号变量替换完成 PAIR_LIST:{len(PAIR_LIST)}", level=LOG_INFO)

        # 进行格式化
        PAIR_LIST = filter_tuple_list(
            tuple_list=PAIR_LIST,
            options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS]
        )
        output(f"[*] 元组格式过滤完成 PAIR_LIST:{len(PAIR_LIST)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.账号替换.txt"),
                   frozen_tuples(PAIR_LIST, link_symbol=config_dict[GB_CONST_LINK]))

    # 对密码做动态处理
    if True:
        PAIR_LIST = transfer_passwd(
            PAIR_LIST,
            options_dict=config_dict[GB_SOCIAL_PASS_OPTIONS_DICT]
        )
        output(f"[*] 密码字符串修改完成 PAIR_LIST:{len(PAIR_LIST)}", level=LOG_INFO)

        # 进行格式化
        PAIR_LIST = filter_tuple_list(
            tuple_list=PAIR_LIST,
            options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS]
        )
        output(f"[*] 元组格式过滤完成 PAIR_LIST:{len(PAIR_LIST)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuples(PAIR_LIST, link_symbol=config_dict[GB_CONST_LINK])
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.密码转换.txt"),
                   frozen_tuple_list_)

    # 对元组列表进行 中文编码处理
    if config_dict[GB_CHINESE_ENCODE_CODING]:
        PAIR_LIST = tuple_list_chinese_encode_by_char(
            PAIR_LIST,
            coding_list=config_dict[GB_CHINESE_ENCODE_CODING],
            url_encode=config_dict[GB_CHINESE_CHAR_URLENCODE],
            de_strip=True,
            only_chinese=config_dict[GB_ONLY_CHINESE_URL_ENCODE]
        )
        output(f"[*] 中文编码衍生完成 PAIR_LIST:{len(PAIR_LIST)}")
        # 进行格式化
        PAIR_LIST = filter_tuple_list(
            tuple_list=PAIR_LIST,
            options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS]
        )
        output(f"[*] 元组格式过滤完成 PAIR_LIST:{len(PAIR_LIST)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.中文衍生.txt"),
                   frozen_tuples(PAIR_LIST, link_symbol=config_dict[GB_CONST_LINK]))

    # 排除历史文件内的账号密码对
    if config_dict[GB_EXCLUDE_FLAG] and not file_is_empty(config_dict[GB_EXCLUDE_FILE]):
        output(f"[*] 历史爆破记录过滤开始, 原始元素数量 {len(PAIR_LIST)}", level=LOG_INFO)
        history_user_pass_list = read_file_to_list(
            config_dict[GB_EXCLUDE_FILE],
            encoding='utf-8',
            de_strip=True,
            de_weight=True,
            de_unprintable=True
        )
        # 移除已经被爆破过得账号密码
        history_tuple_list = unfrozen_tuples(history_user_pass_list, config_dict[GB_CONST_LINK])
        PAIR_LIST = tuples_subtract(PAIR_LIST, history_tuple_list, config_dict[GB_CONST_LINK])

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuples(PAIR_LIST, link_symbol=config_dict[GB_CONST_LINK])
        write_line(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.排除历史.txt"), frozen_tuple_list_)

    return PAIR_LIST


def actions_controller(config_dict):
    # 　用户输入的账号字典
    selected_name_files = config_dict[GB_BASE_NAME_FILE]
    output(f"[*] 本次调用的基本账号文件: {selected_name_files}", level=LOG_INFO)

    # 根据 level参数 和 GB_RULE_LEVEL_EXACT 设置修改字典路径
    selected_pass_files = select_files_by_level(filen_path_format=config_dict[GB_PASS_FILE_STR],
                                                replace_value=config_dict[GB_RULE_LEVEL_PASS],
                                                rule_exact=config_dict[GB_RULE_LEVEL_EXACT])
    output(f"[*] 本次调用的密码规则文件: {selected_pass_files}", level=LOG_INFO)

    user_pass_dict = generate_social_dict_for_pass(config_dict=config_dict,
                                                   name_files=selected_name_files,
                                                   pass_rule_files=selected_pass_files,
                                                   )
    output(f"[*] 最终生成账号密码对数量: {len(user_pass_dict)}", level=LOG_INFO)


if __name__ == '__main__':
    # 加载初始设置参数
    setting_com.init_common(CONFIG)
    setting_com.init_custom(CONFIG)
    setting_dict.init_custom(CONFIG)

    # 设置默认debug参数日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], True)

    # 输入参数解析
    args = args_parser(CONFIG)
    output(f"[*] 输入参数信息: {args}")

    # 处理输入参数
    updates = args_dict_handle(args)
    output(f"[*] 输入参数更新: {updates}")

    # 将输入参数加入到全局CONFIG
    config_dict_add_args(CONFIG, args)

    # 更新全局CONFIG
    updates = config_dict_handle(CONFIG)
    output(f"[*] 配置参数更新: {updates}")

    # 根据用户输入的debug参数设置日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], CONFIG[GB_DEBUG_FLAG])

    # 输出所有参数信息
    output(f"[*] 最终配置信息: {CONFIG}", level=LOG_DEBUG)
    # show_config_dict(CONFIG)

    # 进行字典伸出
    actions_controller(CONFIG)
