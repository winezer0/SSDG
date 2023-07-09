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


def remove_duplicates(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def gen_key_list(keyboard_x2d,add_row=True):
    line_result = []
    for lll in [1, 2]:
        index_dict = {0: 1, -1: -1}
        row_result = []
        for index, step in index_dict.items():
            tmp_list = []
            for lst in keyboard_x2d[:3]:
                tmp_list.append(lst[index])
                index += step
            if add_row: line_result.append("".join(tmp_list))
            row_result.append("".join(tmp_list))
        line_result.append("".join(row_result))
    return remove_duplicates(line_result)


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    # 定义键盘规则
    keyboard_rules = [
        '789',
        '456',
        '123',
    ]
    # 0、生成 二维 键盘列表
    keyboard_x2d = get_keyboard_x2d(keyboard_rules)
    # print(keyboard_x2d)

    # 1、生成 qwerty 这样的键盘字符串
    base_dict = {
        f"{script_name}.max.gen.txt": {
            "starts": [],
            "add_row":True,
        },
        f"{script_name}.min.gen.txt": {
            "starts": [],
            "add_row": False,
        },
    }

    for file_path, options in base_dict.items():
        data_list = gen_key_list(keyboard_x2d,add_row=options["add_row"])

        # 仅已指定字符开头的元素
        starts = options["starts"]
        if len(starts) > 0:
            data_list = [string for string in data_list if any(string.startswith(str(start)) for start in starts)]
        print(data_list)
        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
