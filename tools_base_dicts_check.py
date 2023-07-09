#!/usr/bin/env python
# encoding: utf-8
from libs.lib_file_operate.file_path import get_dir_path_info_dict, get_dir_path_dir_info_dict, \
    file_name_remove_ext_list
from libs.lib_log_print.logger_printer import set_logger, output, LOG_ERROR, LOG_INFO
from setting_com import *


# 判断是否存在重复的属性名称,不能够存在重复【文件名|目录名】的
# 如果存在目录和文件名相同也需要警告

# 查找重复元素
def find_duplicates(string_list):
    # 使用一个集合来保存已经出现过的元素
    seen = set()
    # 使用一个列表来保存重复的元素
    duplicates = []
    for item in string_list:
        # 如果元素已经在集合中出现过，说明是重复元素
        if item in seen:
            # 将重复元素添加到列表中
            duplicates.append(item)
        else:
            # 将元素添加到集合中
            seen.add(item)
    return duplicates


# 检查基本变量是否重复
def check_base_var_duplicates(dirs):
    """
    判断是否存在重复的属性名称,不能够存在重复【文件名|目录名】的
    如果存在目录和文件名相同也需要警告
    :param dirs: 所有目录:字典后缀
    :return:
    """
    name_dirs = copy.copy(dirs)
    del name_dirs[GB_BASE_PASS_DIR]

    pass_dirs = copy.copy(dirs)
    del pass_dirs[GB_BASE_NAME_DIR]

    dirs_list = [name_dirs, pass_dirs]

    for temp_dirs in dirs_list:
        # 获取所有文件名和目录名
        all_path_dict = {}
        for base_var_dir, ext_list in temp_dirs.items():
            path_info_dict = get_dir_path_info_dict(base_var_dir, ext_list=ext_list)
            all_path_dict.update(path_info_dict)

        # 组装 [基本变量名]
        all_base_vars = []
        for path_name in list(all_path_dict.values()):
            base_var_name = f'%{file_name_remove_ext_list(path_name, ext_list)}%'
            all_base_vars.append(base_var_name)
        output(f"[*] all_base_vars: len:{len(all_base_vars)} {all_base_vars}", level=LOG_INFO)

        # 判断是否存在重复文件名或目录名
        duplicates_file_list = find_duplicates(all_base_vars)
        if duplicates_file_list:
            output(f"[-] 发现 重复基本变量 建议修改名称: {duplicates_file_list}", level=LOG_ERROR)
            # 反向查找文件所在目录
            for duplicates_file in duplicates_file_list:
                for k, v in all_path_dict.items():
                    if duplicates_file.strip("%") in str(k):
                        output(f"[-] 重复基本变量 [{duplicates_file}] 位于 {k}", level=LOG_ERROR)
        else:
            output(f"[*] 未发现 重复基本变量...{list(temp_dirs.keys())}", level=LOG_INFO)


if __name__ == '__main__':
    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_FILE, GB_ERR_LOG_FILE, GB_DBG_LOG_FILE, False)

    # 检查max文件变量
    base_dict_ext = [".man.txt", ".max.txt"]
    base_dirs = {
        GB_BASE_VAR_DIR: base_dict_ext,
        GB_BASE_DYNA_DIR: base_dict_ext,
        GB_BASE_NAME_DIR: base_dict_ext,
        GB_BASE_PASS_DIR: base_dict_ext,
    }
    # 检查基本变量是否重复
    check_base_var_duplicates(base_dirs)
