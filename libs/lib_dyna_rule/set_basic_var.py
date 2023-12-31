#!/usr/bin/env python
# encoding: utf-8

# 获取基本变量 替换字典
import copy

from libs.lib_dyna_rule.dyna_rule_tools import dict_content_base_rule_render, get_key_list_with_freq
from libs.lib_file_operate.file_path import get_dirs_file_info_dict, get_dirs_dir_info_dict
from libs.lib_file_operate.file_utils import file_name_remove_ext
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.rw_freq_file import read_file_to_freq_dict


def set_base_var_dict(base_var_dir,
                      ext_list,
                      base_replace_dict):
    # 保留原有字典
    base_var_replace_dict = copy.copy(base_replace_dict)

    # 获取目录下的文件名信息字典
    base_var_file_info_dict = get_dirs_file_info_dict(base_var_dir, ext_list=ext_list)

    # 生成文件名对应基本变量
    for base_var_file_path, base_var_file_name in base_var_file_info_dict.items():
        # 读文件到列表
        base_var_file_content = read_file_to_list(base_var_file_path,
                                                  encoding=None,
                                                  de_strip=True,
                                                  de_weight=True,
                                                  de_unprintable=True)

        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_var_pure_name = file_name_remove_ext(base_var_file_name, ext_list)
        base_var_replace_dict[f'%{base_var_pure_name}%'] = base_var_file_content

    # 对 内容列表 中的规则进行 进行 动态解析
    base_var_replace_dict = dict_content_base_rule_render(base_var_replace_dict)

    # 获取目录下的目录名信息字典
    base_var_dir_info_dict = get_dirs_dir_info_dict(base_var_dir)

    # 生成目录名对应基本变量
    for base_var_dir_path, base_var_dir_name in base_var_dir_info_dict.items():
        # 获取目录下符合条件的文件名
        temp_file_info_dict = get_dirs_file_info_dict(base_var_dir_path, ext_list=ext_list)

        # # 读多个文件到内容列表  #函数使用更加灵活,但会增加读写,还需要渲染一次
        # base_var_files_content = read_files_to_list(list(temp_file_info_dict.values()),
        #                                             encoding=None,
        #                                             de_strip=True,
        #                                             de_weight=True,
        #                                             de_unprintable=True)

        # 从已有的字典列表内获取内容  #可以放在后面可以省去渲染过程
        base_var_files_content = []
        for base_var_file_name in list(temp_file_info_dict.values()):
            base_var_pure_name = file_name_remove_ext(base_var_file_name, ext_list)
            base_var_files_content.extend(base_var_replace_dict[f'%{base_var_pure_name}%'])

        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_var_replace_dict[f'%{base_var_dir_name}%'] = base_var_files_content

    return base_var_replace_dict


# 获取基本变量替换字典
def set_base_var_dict_with_freq(base_var_dir, ext_list, base_replace_dict, freq_symbol, anno_symbol, freq_min):
    """
    # 1 读取 所有基本替换变量字典 到频率字典
    # 2 按频率筛选 并加入到 基本变量替换字典
    # 3 对 基本变量替换字典 进行规则解析
    """
    base_var_replace_dict = copy.copy(base_replace_dict)

    # 获取目录下的文件名信息字典
    base_var_file_info_dict = get_dirs_file_info_dict(base_var_dir, ext_list=ext_list)

    # 生成文件名对应基本变量
    for base_var_file_path, base_var_file_name in base_var_file_info_dict.items():
        # 获取频率字典
        file_content_freq_dict = read_file_to_freq_dict(base_var_file_path,
                                                        encoding=None,
                                                        freq_symbol=freq_symbol,
                                                        anno_symbol=anno_symbol)
        # 筛选频率字典
        file_content_freq_list = get_key_list_with_freq(file_content_freq_dict, freq_min)

        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_file_pure_name = file_name_remove_ext(base_var_file_name, ext_list)
        base_var_replace_dict[f'%{base_file_pure_name}%'] = file_content_freq_list

    # 对 内容列表 中的规则进行 进行 动态解析
    base_var_replace_dict = dict_content_base_rule_render(base_var_replace_dict)

    # 获取目录下的目录名信息字典
    base_var_dir_info_dict = get_dirs_dir_info_dict(base_var_dir)

    # 生成目录名对应基本变量
    for base_var_dir_path, base_var_dir_name in base_var_dir_info_dict.items():
        # 获取目录下符合条件的文件名
        temp_file_info_dict = get_dirs_file_info_dict(base_var_dir_path, ext_list=ext_list)

        # # 获取频率字典  #函数使用更加灵活,但会增加读写,还需要渲染一次
        # files_content_freq_dict = read_files_to_freq_dict(list(temp_file_info_dict.values()),
        #                                                            encoding=None,
        #                                                            freq_symbol=freq_symbol,
        #                                                            anno_symbol=anno_symbol)
        # # 筛选频率字典
        # files_content_freq_list = get_key_list_with_freq(files_content_freq_dict, freq_min)

        # 从已有的字典列表内获取内容  #可以放在后面可以省去渲染过程
        files_content_freq_list = []
        for base_var_file_name in list(temp_file_info_dict.values()):
            base_var_pure_name = file_name_remove_ext(base_var_file_name, ext_list)
            files_content_freq_list.extend(base_var_replace_dict[f'%{base_var_pure_name}%'])

        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_var_replace_dict[f'%{base_var_dir_name}%'] = files_content_freq_list

    return base_var_replace_dict
