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


def gen_num_10(length_list, number_list):
    """
    生成10 100 100 这样的数据
    :param length_list:
    :param number_list:
    :return:
    """
    result = []
    for x in length_list:
        base_num = pow(10, x - 1) if x - 1 > 0 else 0
        for add_num in number_list:
            result.append(base_num + add_num)
    return result


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    base_dict = {
        f"{script_name}.max.gen.txt": {
            "lengths": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "numbers": [0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        f"{script_name}.min.gen.txt": {
            "lengths": [1, 2, 3, 4],
            "numbers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
    }
    for file_path, options in base_dict.items():
        data_list = gen_num_10(options["lengths"], options["numbers"])
        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
