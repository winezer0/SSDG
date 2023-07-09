#!/usr/bin/env python
# encoding: utf-8

from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_log_print.logger_printer import output, LOG_ERROR


def gen_file_names(format_str, replace, rule_exact=False, marks="{LEVEL}"):
    file_names = []
    if rule_exact:
        a_file = format_str.replace(marks, f"{replace}")
        if file_is_exist(a_file):
            file_names.append(a_file)
        else:
            output(f"[*] 目标文件不存在 {a_file}", level=LOG_ERROR)
    else:
        for level in range(replace + 1):
            a_file = format_str.replace(marks, f"{replace}")
            if file_is_exist(a_file):
                file_names.append(a_file)
    return file_names
