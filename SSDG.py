#!/usr/bin/env python
# encoding: utf-8

import argparse

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
from libs.util_ssdg import gen_file_names
from setting_com import *


# 分割写法 基于 用户名和密码规则生成 元组列表
def social_rule_handle_in_steps_two_list(target_url, user_name_files, user_pass_files,
                                         default_name_list=None, default_pass_list=None, exclude_file=None):
    print(f"user_name_files:{user_name_files}")
    print(f"user_pass_files:{user_pass_files}")

    mode = "mode1"
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
        name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
        pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.render_base.name.txt"), name_list)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.render_base.pass.txt"), pass_list)

    # 基本变量替换处理
    if True:
        # 获取基本变量字典
        base_var_replace_dict = set_base_var_dict(GB_BASE_VAR_DIR, GB_BASE_DICT_SUFFIX, GB_BASE_VAR_REPLACE_DICT)
        output(f"[*] 基本变量字典获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        base_var_replace_dict = set_base_var_dict(GB_BASE_DYNA_DIR, GB_BASE_DICT_SUFFIX, base_var_replace_dict)
        output(f"[*] 动态基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
        name_base_var_replace_dict = set_base_var_dict(GB_BASE_NAME_DIR, GB_BASE_DICT_SUFFIX, base_var_replace_dict)
        output(f"[*] 账号基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        pass_base_var_replace_dict = set_base_var_dict(GB_BASE_PASS_DIR, GB_BASE_DICT_SUFFIX, base_var_replace_dict)
        output(f"[*] 密码基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")
        # 删除不会被用到规则用到的基本变量替换字典的键
        name_base_var_replace_dict = remove_not_used_key(name_base_var_replace_dict, name_list)
        pass_base_var_replace_dict = remove_not_used_key(pass_base_var_replace_dict, pass_list)

        # 进行基本变量字典替换 及 其中的中文词汇处理
        if GB_CHINESE_TO_PINYIN:
            # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
            name_base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=name_base_var_replace_dict,
                                                                       options_dict=GB_CHINESE_OPTIONS_NAME,
                                                                       store_chinese=GB_STORE_CHINESE)
            # 对密码列表依赖的 基本变量字典中的列表值进行中文处理
            pass_base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=pass_base_var_replace_dict,
                                                                       options_dict=GB_CHINESE_OPTIONS_PASS,
                                                                       store_chinese=GB_STORE_CHINESE)

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
        name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
        pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_base.name.txt"), name_list)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_base.pass.txt"), pass_list)

    # 因变量替换处理
    if True:
        # 获取因变量
        dependent_var_replace_dict = set_dependent_var_dict(target_url=target_url,
                                                            base_dependent_dict=GB_DEPENDENT_VAR_REPLACE_DICT,
                                                            ignore_ip_format=GB_IGNORE_IP_FORMAT,
                                                            symbol_replace_dict=GB_SYMBOL_REPLACE_DICT,
                                                            not_allowed_symbol=GB_NOT_ALLOW_SYMBOL)
        output(f"[*] 获取因变量完成 dependent_var_replace_dict:{dependent_var_replace_dict}")

        # 清空没有被使用的键
        dependent_var_replace_dict = remove_not_used_key(dependent_var_replace_dict, [name_list, pass_list])

        # 因变量替换
        name_list, _, _ = replace_list_has_key_str(name_list, dependent_var_replace_dict)
        pass_list, _, _ = replace_list_has_key_str(pass_list, dependent_var_replace_dict)
        output(f"[*] 因变量替换完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}")

        # 进行格式化
        name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
        pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_dependent.name.txt"), name_list)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_dependent.pass.txt"), pass_list)

    # 调用tag exec来进行操作,实现字符串反序 实现1221等格式
    if True:
        name_list = match_exec_repl_loop_batch(name_list, TAG_FUNC_DICT)
        pass_list = match_exec_repl_loop_batch(pass_list, TAG_FUNC_DICT)

        # 进行格式化
        name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
        pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
        output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.tag_exec.name.txt"), name_list)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.tag_exec.pass.txt"), pass_list)

    # 组合用户名列表和密码列表
    if True:
        name_pass_pair_list = cartesian_product_merging(name_list, pass_list)
        output(f"[*] 组合账号密码列表完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.cartesian.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK))

    # 对基于用户名变量的密码做替换处理
    if True:
        name_pass_pair_list = replace_mark_user_on_pass(name_pass_pair_list,
                                                        mark_string=GB_USER_NAME_MARK,
                                                        options_dict=GB_SOCIAL_USER_OPTIONS_DICT)
        output(f"[*] 用户名变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_mark.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK))

    # 对密码做动态处理
    if True:
        name_pass_pair_list = transfer_passwd(name_pass_pair_list,
                                              options_dict=GB_SOCIAL_PASS_OPTIONS_DICT)
        output(f"[*] 密码字符串修改完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.transfer_pass.pair.txt"), frozen_tuple_list_)

    # 对元组列表进行 中文编码处理
    if GB_CHINESE_ENCODE_CODING:
        name_pass_pair_list = tuple_list_chinese_encode_by_char(name_pass_pair_list,
                                                                coding_list=GB_CHINESE_ENCODE_CODING,
                                                                url_encode=GB_CHINESE_CHAR_URLENCODE,
                                                                de_strip=True,
                                                                only_chinese=GB_ONLY_CHINESE_URL_ENCODE)
        output(f"[*] 中文编码衍生完成 name_pass_pair_list:{len(name_pass_pair_list)}")
        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.chinese_encode.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK))

    # 排除历史文件内的账号密码对
    if GB_EXCLUDE_FLAG and not file_is_empty(exclude_file):
        output(f"[*] 历史爆破记录过滤开始, 原始元素数量 {len(name_pass_pair_list)}", level=LOG_INFO)
        history_user_pass_list = read_file_to_list(exclude_file, encoding='utf-8', de_strip=True, de_weight=True,
                                                   de_unprintable=True)
        # 移除已经被爆破过得账号密码
        history_tuple_list = unfrozen_tuple_list(history_user_pass_list, GB_CONST_LINK)
        name_pass_pair_list = reduce_str_str_tuple_list(name_pass_pair_list, history_tuple_list, GB_CONST_LINK)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.exclude_history.txt"), frozen_tuple_list_)
    return name_pass_pair_list


# 分割写法 基于 用户名:密码对 规则生成 元组列表
def social_rule_handle_in_steps_one_pairs(target_url, pair_file_names, pair_link_symbol,
                                          default_name_list=None, default_pass_list=None, exclude_file=None):
    mode = "mode2"
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
    if GB_USE_PAIR_BASE_REPL:
        # 动态规则解析
        if True:
            name_pass_pair_list, _, _ = base_rule_render_list(name_pass_pair_list)
            output(f"[*] 元组动态规则解析完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
            # 写入当前结果
            step += 1
            write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.base_render.pair.txt"), name_pass_pair_list)

        # 基本变量处理
        if True:
            # 获取基本变量字典
            base_var_replace_dict = set_base_var_dict(GB_BASE_VAR_DIR, GB_BASE_DICT_SUFFIX, GB_BASE_VAR_REPLACE_DICT)
            output(f"[*] 基本变量字典获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            base_var_replace_dict = set_base_var_dict(GB_BASE_DYNA_DIR, GB_BASE_DICT_SUFFIX, base_var_replace_dict)
            output(f"[*] 动态基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            base_var_replace_dict = set_base_var_dict(GB_BASE_NAME_DIR, GB_BASE_DICT_SUFFIX, base_var_replace_dict)
            output(f"[*] 姓名基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            base_var_replace_dict = set_base_var_dict(GB_BASE_PASS_DIR, GB_BASE_DICT_SUFFIX, base_var_replace_dict)
            output(f"[*] 密码基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

            # 清空不被需要的字典键
            base_var_replace_dict = remove_not_used_key(base_var_replace_dict, name_pass_pair_list)

            # 对基本变量字典中的列表值进行中文处理
            if GB_CHINESE_TO_PINYIN:
                output(f"[*] 中文列表处理转换开始 base_var_replace_dict:{len(str(base_var_replace_dict))}", level=LOG_INFO)
                base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=base_var_replace_dict,
                                                                      options_dict=GB_CHINESE_OPTIONS_TUPLE,
                                                                      store_chinese=GB_STORE_CHINESE)
                output(f"[*] 中文列表处理转换完成 base_var_replace_dict:{len(str(base_var_replace_dict))}", level=LOG_INFO)

            # 基本变量替换
            name_pass_pair_list, _, _ = replace_list_has_key_str(name_pass_pair_list, base_var_replace_dict)
            output(f"[*] 元组基本变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
            # 写入当前结果
            step += 1
            write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_base.pair.txt"), name_pass_pair_list)

        # 因变量处理
        if True:
            # 获取因变量
            dependent_var_replace_dict = set_dependent_var_dict(target_url=target_url,
                                                                base_dependent_dict=GB_DEPENDENT_VAR_REPLACE_DICT,
                                                                ignore_ip_format=GB_IGNORE_IP_FORMAT,
                                                                symbol_replace_dict=GB_SYMBOL_REPLACE_DICT,
                                                                not_allowed_symbol=GB_NOT_ALLOW_SYMBOL)

            # 清空没有被使用的键
            dependent_var_replace_dict = remove_not_used_key(dependent_var_replace_dict, name_pass_pair_list)

            # 因变量替换
            name_pass_pair_list, _, _ = replace_list_has_key_str(name_pass_pair_list, dependent_var_replace_dict)
            output(f"[*] 元组因变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

            # 写入当前结果
            step += 1
            write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_dependent.pair.txt"),
                        name_pass_pair_list)

        # 调用tag exec来进行操作,实现字符串反序 实现1221等格式
        if True:
            name_pass_pair_list = match_exec_repl_loop_batch(name_pass_pair_list, TAG_FUNC_DICT)

            # 写入当前结果
            step += 1
            write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.tag_exec.pair.txt"), name_pass_pair_list)

    # 拆分出账号 密码对 元祖
    name_pass_pair_list = unfrozen_tuple_list(name_pass_pair_list, pair_link_symbol)

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
                                                        mark_string=GB_USER_NAME_MARK,
                                                        options_dict=GB_SOCIAL_USER_OPTIONS_DICT)
        output(f"[*] 用户名变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.replace_mark.pair.txt"), frozen_tuple_list_)

    # 对密码做动态处理
    if True:
        name_pass_pair_list = transfer_passwd(name_pass_pair_list,
                                              options_dict=GB_SOCIAL_PASS_OPTIONS_DICT)
        output(f"[*] 密码字符串修改完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.transfer_pass.pair.txt"), frozen_tuple_list_)

    # 对元组列表进行 中文编码处理
    if GB_CHINESE_ENCODE_CODING:
        name_pass_pair_list = tuple_list_chinese_encode_by_char(name_pass_pair_list,
                                                                coding_list=GB_CHINESE_ENCODE_CODING,
                                                                url_encode=GB_CHINESE_CHAR_URLENCODE,
                                                                de_strip=True,
                                                                only_chinese=GB_ONLY_CHINESE_URL_ENCODE)
        output(f"[*] 中文编码衍生完成 name_pass_pair_list:{len(name_pass_pair_list)}")
        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.chinese_encode.pair.txt"), frozen_tuple_list_)

    # 排除历史文件内的账号密码对
    if GB_EXCLUDE_FLAG and not file_is_empty(exclude_file):
        output(f"[*] 历史爆破记录过滤开始, 原始元素数量 {len(name_pass_pair_list)}", level=LOG_INFO)
        history_user_pass_list = read_file_to_list(exclude_file, encoding='utf-8', de_strip=True, de_weight=True,
                                                   de_unprintable=True)
        # 移除已经被爆破过得账号密码
        history_tuple_list = unfrozen_tuple_list(history_user_pass_list, GB_CONST_LINK)
        name_pass_pair_list = reduce_str_str_tuple_list(name_pass_pair_list, history_tuple_list, GB_CONST_LINK)

        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=GB_CONST_LINK)
        write_lines(GB_TEMP_DICT_DIR.joinpath(f"{mode}.{step}.exclude_history.txt"), frozen_tuple_list_)
    return name_pass_pair_list


def parse_input():
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
    # description 程序描述信息
    argument_parser.description = "Based HTTP Packet Login Auto Blasting, And Social Account Password Generation Tool"

    argument_parser.add_argument("-t", "--target_url", default=GB_TARGET_URL,
                                 help=f"Specify the blasting Target url, Default is {GB_TARGET_URL}", )

    argument_parser.add_argument("-b", "--base_dict_suffix", default=GB_BASE_DICT_SUFFIX, nargs="+",
                                 help=f"Specifies the base var file suffix, Default is {GB_BASE_DICT_SUFFIX}")

    argument_parser.add_argument("-ln", "--rule_level_name", default=GB_RULE_LEVEL_NAME, type=int,
                                 help=f"Specifies the name rule file level or prefix, Default is {GB_RULE_LEVEL_NAME}")

    argument_parser.add_argument("-lp", "--rule_level_pass", default=GB_RULE_LEVEL_PASS, type=int,
                                 help=f"Specifies the pass rule file level or prefix, Default is {GB_RULE_LEVEL_PASS}")

    argument_parser.add_argument("-ll", "--rule_level_pair", default=GB_RULE_LEVEL_PAIR, type=int,
                                 help=f"Specifies the pair rule file level or prefix, Default is {GB_RULE_LEVEL_PAIR}")

    argument_parser.add_argument("-lf", "--rule_level_exact", default=GB_RULE_LEVEL_EXACT, action="store_false",
                                 help=f"Specifies Exact call level dictionary, Default is [{GB_RULE_LEVEL_EXACT}]", )

    argument_parser.add_argument("-af", "--pair_file_flag", default=GB_PAIR_FILE_FLAG, action="store_false",
                                 help=f"Specifies Display Debug Info, Default is [{GB_PAIR_FILE_FLAG}]", )

    argument_parser.add_argument("-s", "--pair_link_symbol", default=GB_PAIR_LINK_SYMBOL,
                                 help=f"Specifies Name Pass Link Symbol in history file, Default is {GB_PAIR_LINK_SYMBOL}", )

    argument_parser.add_argument("-ef", "--exclude_flag", default=GB_EXCLUDE_FLAG, action="store_true",
                                 help=f"Specifies exclude history file flag, Default is {GB_EXCLUDE_FLAG}", )

    argument_parser.add_argument("-e", "--exclude_file", default=GB_EXCLUDE_FILE,
                                 help=f"Specifies exclude history file name, Default is {GB_EXCLUDE_FILE}", )

    argument_parser.add_argument("-c", "--const_link", default=GB_CONST_LINK,
                                 help=f"Specifies Name Pass Link Symbol in history file, Default is {GB_CONST_LINK}", )

    argument_parser.add_argument("-d", "--debug_flag", default=GB_DEBUG_FLAG, action="store_true",
                                 help=f"Specifies Display Debug Info, Default is {GB_DEBUG_FLAG}", )

    # epilog 程序额外信息
    argument_parser.epilog = f"""Version: {GB_VERSION}\n\n更多参数可通过[setting.py]进行配置"""
    return argument_parser


if __name__ == '__main__':
    # 输入参数解析
    parser = parse_input()

    # 输出所有参数
    args = parser.parse_args()
    output(f"[*] 所有输入参数信息: {args}")

    # 使用字典解压将参数直接赋值给相应的全局变量
    for param_name, param_value in vars(args).items():
        globals_var_name = f"GB_{str(param_name).upper()}"
        try:
            globals()[globals_var_name] = param_value
            # output(f"[*] INPUT:{globals_var_name} -> {param_value}", level=SHOW_DEBUG)
        except Exception as error:
            output(f"[!] 输入参数信息: {param_name} {param_value} 未对应其全局变量!!!", level=LOG_ERROR)
            exit()

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_FILE, GB_ERR_LOG_FILE, GB_DBG_LOG_FILE, GB_DEBUG_FLAG)

    # 根据level参数和GB_RULE_LEVEL_EXACT设置修改字典路径
    NAME_FILES = gen_file_names(format_str=GB_NAME_FILE_STR, replace=GB_RULE_LEVEL_NAME, rule_exact=GB_RULE_LEVEL_EXACT)
    PASS_FILES = gen_file_names(format_str=GB_PASS_FILE_STR, replace=GB_RULE_LEVEL_PASS, rule_exact=GB_RULE_LEVEL_EXACT)
    PAIR_FILES = gen_file_names(format_str=GB_PAIR_FILE_STR, replace=GB_RULE_LEVEL_PAIR, rule_exact=GB_RULE_LEVEL_EXACT)

    # GB_TARGET_URL = "http://www.baidu.com"  # 336
    if not GB_PAIR_FILE_FLAG:
        user_pass_dict = social_rule_handle_in_steps_two_list(GB_TARGET_URL,
                                                              user_name_files=NAME_FILES,
                                                              user_pass_files=PASS_FILES,
                                                              exclude_file=GB_EXCLUDE_FILE)
    else:
        user_pass_dict = social_rule_handle_in_steps_one_pairs(GB_TARGET_URL,
                                                               pair_file_names=PAIR_FILES,
                                                               pair_link_symbol=GB_PAIR_LINK_SYMBOL,
                                                               exclude_file=GB_EXCLUDE_FILE)

    output(f"[*] 最终生成账号密码对数量: {len(user_pass_dict)}", level=LOG_INFO)
