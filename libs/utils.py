#!/usr/bin/env python
# encoding: utf-8

from libs.lib_file_operate.file_utils import file_is_exist
from libs.lib_log_print.logger_printer import output, LOG_ERROR


def select_files_by_level(filename_format, replace_value, rule_exact=False, replace_marks="{LEVEL}"):
    file_names = []
    if rule_exact:
        rule_file = filename_format.replace(replace_marks, f"{replace_value}")
        if file_is_exist(rule_file):
            file_names.append(rule_file)
        else:
            output(f"[*] 目标文件不存在 {rule_file}", level=LOG_ERROR)
    else:
        for level in range(replace_value + 1):
            rule_file = filename_format.replace(replace_marks, f"{level}")
            if file_is_exist(rule_file):
                file_names.append(rule_file)
    return file_names
