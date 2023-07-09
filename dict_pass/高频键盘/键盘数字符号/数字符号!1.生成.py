#!/usr/bin/env python
# encoding: utf-8
import os
import re
import sys


def contains_two_of_three(string):
    has_letter = re.search(r'[a-zA-Z]', string)  # 包含字母
    has_digit = re.search(r'\d', string)  # 包含数字
    has_symbol = re.search(r'[^a-zA-Z\d\s]', string)  # 包含符号

    if (has_letter and has_digit) or (has_letter and has_symbol) or (has_digit and has_symbol):
        return True
    else:
        return False


def write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+"):
    """
    文本文件列表写入数据
    :param file_path:
    :param data_list:
    :param encoding:
    :param new_line:
    :param mode:
    :return:
    """
    with open(file_path, mode=mode, encoding=encoding) as f_open:
        if new_line:  # 换行输出
            data_list = [f"{data}\n" for data in data_list]
        f_open.writelines(data_list)
        f_open.close()


def get_keyboard_x2d(keyboard_rule):
    keyboard_rules_x2d = [list(s) for s in keyboard_rule]
    return keyboard_rules_x2d


def gen_key_list(keyboard_x2d, len_list=[]):
    # 1、生成 qwer 这样的键盘字符串
    ele_result = []

    # 获取最短字符串的长度
    min_len = len(min(keyboard_x2d, key=len))
    # 获取所有元素数量
    ele_num = len(keyboard_x2d)
    for han in range(min_len):
        tmp = []
        for lie in range(ele_num):
            ele = keyboard_x2d[lie][han]
            tmp.append(ele)
        ele_result.append("".join(tmp))

    ele_result = list(set(ele_result))
    # print(ele_result)  # ['6yhn', '5tgb', '4rfv', '1qaz', '2wsx', '7ujm', '3edc']
    line_result = []
    for length in len_list:
        for line in ele_result:
            for i in range(ele_num):
                if i + length <= ele_num:
                    line_result.append(line[i:i + length])
                    # print(line[i:i+length])
    # print(line_result)
    return line_result


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    # 定义键盘规则
    keyboard_rules = [
        '!@#$%^&*()_+',
        '1234567890',
    ]
    # 0、生成 二维 键盘列表
    keyboard_x2d = get_keyboard_x2d(keyboard_rules)
    # print(keyboard_x2d)

    # 1、生成 qwerty 这样的键盘字符串
    base_dict = {
        f"{script_name}.max.gen.txt": {
            "length": [2],
            "starts": [],
        },
        f"{script_name}.min.gen.txt": {
            "length": [2],
            "starts": ["!","@","#"],
        },
    }

    for file_path, options in base_dict.items():
        data_list = gen_key_list(keyboard_x2d, options["length"])

        # 仅已指定字符开头的元素
        if options["starts"]:
            data_list = [string for string in data_list if any(string.startswith(str(start)) for start in options["starts"])]
        # 同时包含 字母、数字、符号中的任意两项
        data_list = [data for data in data_list if contains_two_of_three(data)]
        print(data_list)

        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
