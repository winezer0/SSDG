#!/usr/bin/env python
# encoding: utf-8

import os
import string
import sys


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


def get_base_ele(start_symbol=0, end_symbol=26):
    # 生成一个包含 a-z 的所有小写字母的列表
    letter_list = list(string.ascii_lowercase)

    # 判断是字符定位还是数字定位标记
    start = letter_list.index(start_symbol) if isinstance(start_symbol, str) else start_symbol
    end = letter_list.index(end_symbol) if isinstance(end_symbol, str) else end_symbol
    return letter_list[start:end]


def gen_overlap_ele(letter_list, count):
    # 基于基本元素列表，生成迭代字符列表
    return [str(letter) * count for letter in letter_list]


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    # 定义基本元素
    base_dict = {
        f"{script_name}.max.gen.txt": {
            "letters": range(10),  # 基本字符
            "repeats": [2, 3, 4],  # 重复次数
        },
        f"{script_name}.min.gen.txt": {
            "letters": [0, 1, 2, 6, 8, 9],  # 基本字符
            "repeats": [2, 3, 4],  # 重复次数
        },
    }

    for file_path, options in base_dict.items():
        data_list = []
        # 生成列表
        for times in options["repeats"]:
            letters = gen_overlap_ele(options["letters"], times)
            data_list.extend(letters)

        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
