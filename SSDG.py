#!/usr/bin/env python
# encoding: utf-8

import argparse

import setting_com
import setting_dict
from libs.input_const import *
from libs.input_parse import args_parser, args_dict_handle, config_dict_add_args, config_dict_handle, show_config_dict
from libs.lib_attribdict.config import CONFIG
from libs.lib_chinese_encode.chinese_encode import tuple_list_chinese_encode_by_char
from libs.lib_chinese_pinyin.chinese_list_to_alphabet_list import dict_chinese_to_dict_alphabet
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str, remove_not_used_key
from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list
from libs.lib_dyna_rule.dyna_rule_tools import cartesian_product_merging, unfrozen_tuple_list, reduce_str_str_tuple_list
from libs.lib_dyna_rule.dyna_rule_tools import frozen_tuple_list
from libs.lib_dyna_rule.set_basic_var import set_base_var_dict
from libs.lib_dyna_rule.set_depend_var import set_dependent_var_dict
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_path import file_is_empty
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_lines
from libs.lib_filter_srting.filter_string_call import format_string_list, format_tuple_list
from libs.lib_log_print.logger_printer import set_logger, output, LOG_INFO, LOG_ERROR
from libs.lib_social_dict.repl_mark_user import replace_mark_user_on_pass
from libs.lib_social_dict.transfer_passwd import transfer_passwd
from libs.lib_tags_exec.tags_const import TAG_FUNC_DICT
from libs.lib_tags_exec.tags_exec import match_exec_repl_loop_batch
from libs.utils import gen_file_names


# 分割写法 基于 用户名和密码规则生成 元组列表
def social_rule_handle_in_steps_two_list(config_dict,
                                         user_name_files,
                                         user_pass_files,
                                         default_name_list=None,
                                         default_pass_list=None,
                                         ):
    print(f"user_name_files:{user_name_files}")
    print(f"user_pass_files:{user_pass_files}")

    mode = "files"
    step = 0

    # 读取账号文件
    if default_name_list:
        name_list = default_name_list
        output(f"[*] 已输入默认账号列表 {default_name_list} 忽略读取账号字典文件", level=LOG_INFO)
    else:
        name_list = []
        output(f"[*] 读取账号字典文件 {user_name_files}...", level=LOG_INFO)
        for name_file in user_name_files:
            lines = read_file_to_list(name_file, encoding=file_encoding(name_file), de_strip=True, de_weight=True)
            name_list.extend(lines)
        if name_list:
            # 保持原始顺序去重
            name_list = [x for i, x in enumerate(name_list) if x not in name_list[:i]]
        else:
            output(f"[!] 未输入任何有效账号字典文件!!!", level=LOG_ERROR)
            return []

    # 读取密码文件
    if default_pass_list:
        pass_list = default_pass_list
        output(f"[*] 已输入默认密码列表 {default_pass_list} 忽略读取密码字典文件", level=LOG_INFO)
    else:
        pass_list = []
        output(f"[*] 读取密码字典文件 {user_pass_files}...", level=LOG_INFO)
        for pass_file in user_pass_files:
            lines = read_file_to_list(pass_file, encoding=file_encoding(pass_file), de_strip=True, de_weight=True)
            pass_list.extend(lines)
        if pass_list:
            # 保持原始顺序去重
            pass_list = [x for i, x in enumerate(pass_list) if x not in pass_list[:i]]
        else:
            output(f"[!] 未输入任何有效密码字典文件!!!", level=LOG_ERROR)
            return []

    output(f"[*] 读取账号文件完成 name_list:{len(name_list)} <--> {name_list[:10]}", level=LOG_INFO)
    output(f"[*] 读取密码文件完成 pass_list:{len(pass_list)} <--> {pass_list[:10]}", level=LOG_INFO)

    # 动态规则解析
    if True:
        name_list, _, _ = base_rule_render_list(name_list)
        pass_list, _, _ = base_rule_render_list(pass_list)
        output(f"[*] 动态规则解析完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

        # 进行格式化
        name_list = format_string_list(string_list=name_list, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        pass_list = format_string_list(string_list=pass_list, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.render_base.name.txt"), name_list)
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.render_base.pass.txt"), pass_list)

    # 基本变量替换处理
    if True:
        # 获取基本变量字典
        base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_VAR_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                  config_dict[GB_BASE_VAR_REPLACE_DICT])
        output(f"[*] 基本变量字典获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_DYNA_DIR],
                                                  config_dict[GB_BASE_DICT_SUFFIX],
                                                  base_var_replace_dict)
        output(f"[*] 动态基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
        name_base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_NAME_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                       base_var_replace_dict)
        output(f"[*] 账号基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        pass_base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_PASS_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                       base_var_replace_dict)
        output(f"[*] 密码基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")
        # 删除不会被用到规则用到的基本变量替换字典的键
        name_base_var_replace_dict = remove_not_used_key(name_base_var_replace_dict, name_list)
        pass_base_var_replace_dict = remove_not_used_key(pass_base_var_replace_dict, pass_list)

        # 进行基本变量字典替换 及 其中的中文词汇处理
        if config_dict[GB_CHINESE_TO_PINYIN]:
            # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
            name_base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=name_base_var_replace_dict,
                                                                       options_dict=config_dict[
                                                                           GB_CHINESE_OPTIONS_NAME],
                                                                       store_chinese=config_dict[GB_STORE_CHINESE])
            # 对密码列表依赖的 基本变量字典中的列表值进行中文处理
            pass_base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=pass_base_var_replace_dict,
                                                                       options_dict=config_dict[
                                                                           GB_CHINESE_OPTIONS_PASS],
                                                                       store_chinese=config_dict[GB_STORE_CHINESE])

            output(f"[*] 中文列表处理转换完成 name_base_var_replace_dict:{len(str(name_base_var_replace_dict))}", level=LOG_INFO)
            output(f"[*] 中文列表处理转换完成 pass_base_var_replace_dict:{len(str(pass_base_var_replace_dict))}", level=LOG_INFO)

            # 基本变量替换
            name_list, _, _ = replace_list_has_key_str(name_list, name_base_var_replace_dict)
            pass_list, _, _ = replace_list_has_key_str(pass_list, pass_base_var_replace_dict)
        else:
            # 基本变量替换
            name_list, _, _ = replace_list_has_key_str(name_list, name_base_var_replace_dict)
            pass_list, _, _ = replace_list_has_key_str(pass_list, pass_base_var_replace_dict)
        output(f"[*] 基本变量替换完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

        # 进行格式化
        name_list = format_string_list(string_list=name_list, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        pass_list = format_string_list(string_list=pass_list, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_base.name.txt"), name_list)
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_base.pass.txt"), pass_list)

    # 因变量替换处理
    if True:
        # 获取因变量
        dependent_var_replace_dict = set_dependent_var_dict(target_url=config_dict[GB_TARGET],
                                                            base_dependent_dict=config_dict[
                                                                GB_DEPENDENT_VAR_REPLACE_DICT],
                                                            ignore_ip_format=config_dict[GB_IGNORE_IP_FORMAT],
                                                            symbol_replace_dict=config_dict[GB_SYMBOL_REPLACE_DICT],
                                                            not_allowed_symbol=config_dict[GB_NOT_ALLOW_SYMBOL])
        output(f"[*] 获取因变量完成 dependent_var_replace_dict:{dependent_var_replace_dict}")

        # 清空没有被使用的键
        dependent_var_replace_dict = remove_not_used_key(dependent_var_replace_dict, [name_list, pass_list])

        # 因变量替换
        name_list, _, _ = replace_list_has_key_str(name_list, dependent_var_replace_dict)
        pass_list, _, _ = replace_list_has_key_str(pass_list, dependent_var_replace_dict)
        output(f"[*] 因变量替换完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}")

        # 进行格式化
        name_list = format_string_list(string_list=name_list, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        pass_list = format_string_list(string_list=pass_list, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_dependent.name.txt"), name_list)
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_dependent.pass.txt"), pass_list)

    # 调用tag exec来进行操作,实现字符串反序 实现1221等格式
    if True:
        name_list = match_exec_repl_loop_batch(name_list, TAG_FUNC_DICT)
        pass_list = match_exec_repl_loop_batch(pass_list, TAG_FUNC_DICT)

        # 进行格式化
        name_list = format_string_list(string_list=name_list, options_dict=config_dict[GB_FILTER_OPTIONS_NAME])
        pass_list = format_string_list(string_list=pass_list, options_dict=config_dict[GB_FILTER_OPTIONS_PASS])
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.tag_exec.name.txt"), name_list)
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.tag_exec.pass.txt"), pass_list)

    # 组合用户名列表和密码列表
    if True:
        name_pass_pair_list = cartesian_product_merging(name_list, pass_list)
        output(f"[*] 组合账号密码列表完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.cartesian.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK]))

    # 对基于用户名变量的密码做替换处理
    if True:
        name_pass_pair_list = replace_mark_user_on_pass(name_pass_pair_list,
                                                        mark_string=config_dict[GB_USER_NAME_MARK],
                                                        options_dict=config_dict[GB_SOCIAL_USER_OPTIONS_DICT])
        output(f"[*] 用户名变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_mark.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK]))

    # 对密码做动态处理
    if True:
        name_pass_pair_list = transfer_passwd(name_pass_pair_list,
                                              options_dict=config_dict[GB_SOCIAL_PASS_OPTIONS_DICT])
        output(f"[*] 密码字符串修改完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK])
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.transfer_pass.pair.txt"), frozen_tuple_list_)

    # 对元组列表进行 中文编码处理
    if config_dict[GB_CHINESE_ENCODE_CODING]:
        name_pass_pair_list = tuple_list_chinese_encode_by_char(name_pass_pair_list,
                                                                coding_list=config_dict[GB_CHINESE_ENCODE_CODING],
                                                                url_encode=config_dict[GB_CHINESE_CHAR_URLENCODE],
                                                                de_strip=True,
                                                                only_chinese=config_dict[GB_ONLY_CHINESE_URL_ENCODE])
        output(f"[*] 中文编码衍生完成 name_pass_pair_list:{len(name_pass_pair_list)}")
        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.chinese_encode.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK]))

    # 排除历史文件内的账号密码对
    if config_dict[GB_EXCLUDE_FLAG] and not file_is_empty(config_dict[GB_EXCLUDE_FILE]):
        output(f"[*] 历史爆破记录过滤开始, 原始元素数量 {len(name_pass_pair_list)}", level=LOG_INFO)
        history_user_pass_list = read_file_to_list(config_dict[GB_EXCLUDE_FILE],
                                                   encoding='utf-8',
                                                   de_strip=True,
                                                   de_weight=True,
                                                   de_unprintable=True)
        # 移除已经被爆破过得账号密码
        history_tuple_list = unfrozen_tuple_list(history_user_pass_list, config_dict[GB_CONST_LINK])
        name_pass_pair_list = reduce_str_str_tuple_list(name_pass_pair_list, history_tuple_list,
                                                        config_dict[GB_CONST_LINK])

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK])
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.exclude_history.txt"), frozen_tuple_list_)
    return name_pass_pair_list


# 分割写法 基于 用户名:密码对 规则生成 元组列表
def social_rule_handle_in_steps_one_pairs(config_dict,
                                          pair_file_names,
                                          default_name_list=None,
                                          default_pass_list=None,
                                          ):
    mode = "pairs"
    step = 0

    # 读取用户账号文件
    name_pass_pair_list = []
    for pair_file in pair_file_names:
        lines = read_file_to_list(pair_file, encoding=file_encoding(pair_file), de_strip=True, de_weight=True)
        name_pass_pair_list.extend(lines)
    if name_pass_pair_list:
        # 保持原始顺序去重
        name_pass_pair_list = [x for i, x in enumerate(name_pass_pair_list) if x not in name_pass_pair_list[:i]]
    else:
        output(f"[!] 未输入任何有效密码字典文件!!!", level=LOG_ERROR)
        return []

    output(f"[*] 读取账号密码文件完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 动态规则解析和基本变量替换过程 默认取消
    if config_dict[GB_USE_PAIR_BASE_REPL]:
        # 动态规则解析
        if True:
            name_pass_pair_list, _, _ = base_rule_render_list(name_pass_pair_list)
            output(f"[*] 元组动态规则解析完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
            # 写入当前结果
            step += 1
            write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.base_render.pair.txt"),
                        name_pass_pair_list)

        # 基本变量处理
        if True:
            # 获取基本变量字典
            base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_VAR_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                      config_dict[GB_BASE_VAR_REPLACE_DICT])
            output(f"[*] 基本变量字典获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_DYNA_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                      base_var_replace_dict)
            output(f"[*] 动态基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_NAME_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                      base_var_replace_dict)
            output(f"[*] 姓名基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            base_var_replace_dict = set_base_var_dict(config_dict[GB_BASE_PASS_DIR], config_dict[GB_BASE_DICT_SUFFIX],
                                                      base_var_replace_dict)
            output(f"[*] 密码基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            # 清空不被需要的字典键
            base_var_replace_dict = remove_not_used_key(base_var_replace_dict, name_pass_pair_list)

            # 对基本变量字典中的列表值进行中文处理
            if config_dict[GB_CHINESE_TO_PINYIN]:
                output(f"[*] 中文列表处理转换开始 base_var_replace_dict:{len(str(base_var_replace_dict))}", level=LOG_INFO)
                base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=base_var_replace_dict,
                                                                      options_dict=config_dict[
                                                                          GB_CHINESE_OPTIONS_TUPLE],
                                                                      store_chinese=config_dict[GB_STORE_CHINESE])
                output(f"[*] 中文列表处理转换完成 base_var_replace_dict:{len(str(base_var_replace_dict))}", level=LOG_INFO)

            # 基本变量替换
            name_pass_pair_list, _, _ = replace_list_has_key_str(name_pass_pair_list, base_var_replace_dict)
            output(f"[*] 元组基本变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
            # 写入当前结果
            step += 1
            write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_base.pair.txt"),
                        name_pass_pair_list)

        # 因变量处理
        if True:
            # 获取因变量
            dependent_var_replace_dict = set_dependent_var_dict(
                target_url=config_dict[GB_TARGET],
                base_dependent_dict=config_dict[GB_DEPENDENT_VAR_REPLACE_DICT],
                ignore_ip_format=config_dict[GB_IGNORE_IP_FORMAT],
                symbol_replace_dict=config_dict[GB_SYMBOL_REPLACE_DICT],
                not_allowed_symbol=config_dict[GB_NOT_ALLOW_SYMBOL]
            )

            # 清空没有被使用的键
            dependent_var_replace_dict = remove_not_used_key(dependent_var_replace_dict, name_pass_pair_list)

            # 因变量替换
            name_pass_pair_list, _, _ = replace_list_has_key_str(name_pass_pair_list, dependent_var_replace_dict)
            output(f"[*] 元组因变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

            # 写入当前结果
            step += 1
            write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_dependent.pair.txt"),
                        name_pass_pair_list)

        # 调用tag exec来进行操作,实现字符串反序 实现1221等格式
        if True:
            name_pass_pair_list = match_exec_repl_loop_batch(name_pass_pair_list, TAG_FUNC_DICT)

            # 写入当前结果
            step += 1
            write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.tag_exec.pair.txt"), name_pass_pair_list)

    # 拆分出账号 密码对 元祖
    name_pass_pair_list = unfrozen_tuple_list(name_pass_pair_list, config_dict[GB_PAIR_LINK_SYMBOL])

    # 如果输入了默认值列表,就组合更新的账号 列表
    if default_name_list or default_pass_list:
        output(f"[*] 已输入默认账号列表 {default_name_list} 需要更新账号密码列表")
        if default_name_list:
            pass_list = [name_pass_pair[1] for name_pass_pair in name_pass_pair_list]
            name_pass_pair_list = cartesian_product_merging(default_name_list, pass_list)
        if default_pass_list:
            name_list = [name_pass_pair[0] for name_pass_pair in name_pass_pair_list]
            name_pass_pair_list = cartesian_product_merging(name_list, default_pass_list)
        output(f"[*] 重组账号密码列表完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 对基于用户名变量的密码做综合处理
    if True:
        name_pass_pair_list = replace_mark_user_on_pass(name_pass_pair_list,
                                                        mark_string=config_dict[GB_USER_NAME_MARK],
                                                        options_dict=config_dict[GB_SOCIAL_USER_OPTIONS_DICT])
        output(f"[*] 用户名变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK])
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.replace_mark.pair.txt"), frozen_tuple_list_)

    # 对密码做动态处理
    if True:
        name_pass_pair_list = transfer_passwd(name_pass_pair_list,
                                              options_dict=config_dict[GB_SOCIAL_PASS_OPTIONS_DICT])
        output(f"[*] 密码字符串修改完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK])
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.transfer_pass.pair.txt"), frozen_tuple_list_)

    # 对元组列表进行 中文编码处理
    if config_dict[GB_CHINESE_ENCODE_CODING]:
        name_pass_pair_list = tuple_list_chinese_encode_by_char(name_pass_pair_list,
                                                                coding_list=config_dict[GB_CHINESE_ENCODE_CODING],
                                                                url_encode=config_dict[GB_CHINESE_CHAR_URLENCODE],
                                                                de_strip=True,
                                                                only_chinese=config_dict[GB_ONLY_CHINESE_URL_ENCODE])
        output(f"[*] 中文编码衍生完成 name_pass_pair_list:{len(name_pass_pair_list)}")
        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list,
                                                options_dict=config_dict[GB_FILTER_TUPLE_OPTIONS])
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK])
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.chinese_encode.pair.txt"),
                    frozen_tuple_list_)

    # 排除历史文件内的账号密码对
    if config_dict[GB_EXCLUDE_FLAG] and not file_is_empty(config_dict[GB_EXCLUDE_FILE]):
        output(f"[*] 历史爆破记录过滤开始, 原始元素数量 {len(name_pass_pair_list)}", level=LOG_INFO)
        history_user_pass_list = read_file_to_list(config_dict[GB_EXCLUDE_FILE],
                                                   encoding='utf-8',
                                                   de_strip=True,
                                                   de_weight=True,
                                                   de_unprintable=True)
        # 移除已经被爆破过得账号密码
        history_tuple_list = unfrozen_tuple_list(history_user_pass_list, config_dict[GB_CONST_LINK])
        name_pass_pair_list = reduce_str_str_tuple_list(name_pass_pair_list, history_tuple_list,
                                                        config_dict[GB_CONST_LINK])

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=config_dict[GB_CONST_LINK])
        write_lines(config_dict[GB_TEMP_DICT_DIR].joinpath(f"{mode}.{step}.exclude_history.txt"), frozen_tuple_list_)
    return name_pass_pair_list


def actions_controller(config_dict):
    # 根据level参数和GB_RULE_LEVEL_EXACT设置修改字典路径
    selected_name_files = gen_file_names(format_str=config_dict[GB_NAME_FILE_STR],
                                         replace=config_dict[GB_RULE_LEVEL_NAME],
                                         rule_exact=config_dict[GB_RULE_LEVEL_EXACT])

    selected_pass_files = gen_file_names(format_str=config_dict[GB_PASS_FILE_STR],
                                         replace=config_dict[GB_RULE_LEVEL_PASS],
                                         rule_exact=config_dict[GB_RULE_LEVEL_EXACT])

    selected_pair_files = gen_file_names(format_str=config_dict[GB_PAIR_FILE_STR],
                                         replace=config_dict[GB_RULE_LEVEL_PAIR],
                                         rule_exact=config_dict[GB_RULE_LEVEL_EXACT])

    if config_dict[GB_PAIR_FILE_FLAG]:
        user_pass_dict = social_rule_handle_in_steps_one_pairs(config_dict=config_dict,
                                                               pair_file_names=selected_pair_files,
                                                               default_name_list=None,
                                                               default_pass_list=None,
                                                               )
    else:
        user_pass_dict = social_rule_handle_in_steps_two_list(config_dict=config_dict,
                                                              user_name_files=selected_name_files,
                                                              user_pass_files=selected_pass_files,
                                                              default_name_list=None,
                                                              default_pass_list=None,
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
    output(f"[*] 最终配置信息: {CONFIG}", level=LOG_INFO)
    show_config_dict(CONFIG)

    # 进行字典伸出
    actions_controller(CONFIG)
