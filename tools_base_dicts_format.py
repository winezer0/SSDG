#!/usr/bin/env python
# encoding: utf-8
import re

import setting_com
import setting_dict
from libs.lib_args.input_const import *
from libs.lib_attribdict.config import CONFIG
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_utils import file_name_remove_ext
from libs.lib_file_operate.file_write import write_lines
from libs.lib_log_print.logger_printer import set_logger, output, LOG_INFO
from libs.lib_file_operate.file_path import get_dirs_file_info_dict


# 批量进行格式化 【全部小写、去重】

# 列表去重并保持原始顺序
def unique_list(string_list):
    unique_lst = []
    seen = set()
    for item in string_list:
        if item not in seen:
            seen.add(item)
            unique_lst.append(item)
    return unique_lst


# 进行小写处理
def lower_list(string_list):
    for index, string in enumerate(string_list):
        if str(string).count("%") < 2:
            string_list[index] = str(string).lower()
        else:
            # 需要保留替换变量
            # 按照(%\w+%)进行切割， 对符合（%\w+%）的部分进行保留
            raw_split = re.split(r'(%[\w]+%)', string)
            raw_split = [s for s in raw_split if s != '']  # 去除空字符串
            new_split = [item if bool(re.match(r'^%[\w]%$', item)) else item.lower() for item in raw_split]
            string_list[index] = "".join(new_split)
    return string_list


# 对目录下的文件进行小写和去重处理
def format_base_dict(dirs):
    """
    1、循环读取dirs包含的目录下的所有文件
    2、进行格式化 【全部小写、去重】
    """
    for base_var_dir, ext_list in dirs.items():
        file_info_dict = get_dirs_file_info_dict(base_var_dir, ext_list=ext_list)
        output(f"[*] DIR:{base_var_dir} -> SUFFIX: {ext_list}")
        output(f"[*] FILES : {list(file_info_dict.keys())}")

        for file_path, file_name in file_info_dict.items():
            pure_name = file_name_remove_ext(file_name, ext_list)
            # 读文件到列表
            file_content = read_file_to_list(file_path,
                                             encoding=file_encoding(file_path),
                                             de_strip=True,
                                             de_weight=True,
                                             de_unprintable=True)

            if file_content:
                new_content_list = lower_list(file_content)
                new_content_list = unique_list(new_content_list)
                if len(file_content) != len(new_content_list):
                    output(f"[*] 有效变量名: {f'%{pure_name}%'}")
                    output(f"[*] 变量名内容: {file_content}")
                    write_lines(file_path, new_content_list, encoding="utf-8", new_line=True, mode="w+")
                    output(f"[+] 成功格式化: {file_path}", level=LOG_INFO)
                else:
                    output(f"[*] 无需格式化: {file_path}", level=LOG_INFO)


if __name__ == '__main__':
    # 加载初始设置参数
    setting_com.init_common(CONFIG)
    setting_com.init_custom(CONFIG)
    setting_dict.init_custom(CONFIG)

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], False)

    base_dict_ext = [".min.txt", ".max.txt", ".man.txt"]
    base_dirs = {
        CONFIG[GB_BASE_VAR_DIR]: base_dict_ext,
        CONFIG[GB_BASE_DYNA_DIR]: base_dict_ext,
        CONFIG[GB_BASE_NAME_DIR]: base_dict_ext,
        CONFIG[GB_BASE_PASS_DIR]: base_dict_ext,
    }

    # 格式化所有基本字典文件 小写|去重
    format_base_dict(base_dirs)
