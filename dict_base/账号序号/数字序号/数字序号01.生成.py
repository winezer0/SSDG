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


def gen_num_01(length_list, number_list):
    """
    生成01 001 0001 这样的数据
    :param length_list:
    :param number_list:
    :return:
    """
    result = []
    for i in number_list:
        for length in length_list:
            fmt = "{:0$$d}".replace("$$", str(length))
            result.append(fmt.format(i))
    return result


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    base_dict = {
        f"{script_name}.max.gen.txt": {
            "lengths": [2, 3, 4, 5, 6, 7, 8, 9],
            "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        f"{script_name}.min.gen.txt": {
            "lengths": [2, 3, 4, 5, 6, 7, 8],
            "numbers": [1, 2, 3],
        },
    }
    for file_path, options in base_dict.items():
        data_list = gen_num_01(options["lengths"], options["numbers"])
        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
