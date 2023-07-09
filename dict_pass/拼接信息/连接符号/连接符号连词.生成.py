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


def consecutive_letters(letter_list, length, starts=[]):
    # 创造一个用来接收n个字母组合的空列表
    result = []
    # 用zip与列表解析创建连续的字母组合
    for letter_group in zip(*[letter_list[i:] for i in range(length)]):
        result.append(''.join(letter_group))

    # 进行过滤 判断是否以列表内的字符开头
    if len(starts) > 0:
        result = [string for string in result if any(string.startswith(str(start)) for start in starts)]
    return result


if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0]).split(".", 1)[0]

    base_dict = {
        f"{script_name}.max.gen.txt": {
            "letters": list("~!@#$%^&*()_+"),
            "length": [2, 3, 4, 5, 6, 7],  # 生成的长度需求
            "starts": ["!", "@"],  # 过滤 需要以指定字符开头
        },
        f"{script_name}.min.gen.txt": {
            "letters": list("~!@#$%^&*()_+"),
            "length": [3, ],  # 生成的长度需求
            "starts": ["!", "@"],  # 过滤 需要以指定字符开头
        },
    }
    for file_path, options in base_dict.items():
        data_list = []
        for length in options["length"]:
            base_letters = options["letters"]
            results = consecutive_letters(base_letters, length, options["starts"])
            data_list.extend(results)
        # 写入文件
        write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[*] gen file {file_path}")
