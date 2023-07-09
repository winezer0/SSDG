#!/usr/bin/env python
# encoding: utf-8
import os
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


def get_keyboard_x2d(keyboard_rule):
    keyboard_rules_x2d = [list(s) for s in keyboard_rule]
    return keyboard_rules_x2d


def gen_key_list(keyboard_x2d, len_list=[], counts=[3]):
    # 1、生成 qwer 这样的键盘字符串
    line_result = []
    for length in len_list:
        for index, lst in enumerate(keyboard_x2d):
            if len(keyboard_x2d) > index + 1:
                # a1 = keyboard_x2d[index][:length]
                # a2 = keyboard_x2d[index + 1][:length]
                # string = "".join(a1) + "".join(a2)
                for count in counts:
                    string = ""
                    if index + count<= len(keyboard_x2d):
                        for i in range(count):
                            string += "".join(keyboard_x2d[index+i][:length])
                        line_result.append(string)
    line_result = list(set(line_result))
    return line_result


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    # 定义键盘规则
    keyboard_rules = [
        '123',
        '456',
        '789',
        '-0-'
    ]

    # 0、生成 二维 键盘列表
    keyboard_x2d = get_keyboard_x2d(keyboard_rules)
    # print(keyboard_x2d)

    # 1、生成 qwerty 这样的键盘字符串
    base_dict = {
        f"{script_name}.max.gen.txt": {
            "length": [2, 3, 4, 5],
            "counts": [2, 3],
        },
        f"{script_name}.min.gen.txt": {
            "length": [3],
            "counts": [2,3],
        },
    }

    for file_path, options in base_dict.items():
        data_list = gen_key_list(keyboard_x2d, options["length"],options["counts"])
        # 仅包含纯字母选项
        data_list = [data for data in data_list if '-' not in str(data)]
        print(data_list)
        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
