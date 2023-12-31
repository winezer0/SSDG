#!/usr/bin/env python
# encoding: utf-8


# 判断列表内的元素是否存在有包含在字符串内的
import copy
import json


def dict_dumps(dict_data={}):
    """
    将字典转为字符串
    :param dict_data:
    :return:
    """
    if isinstance(dict_data, dict):
        dict_data = json.dumps(dict_data, sort_keys=True)
    return dict_data


def dict_loads(json_data=""):
    """
    将字符串转为字典
    :param json_data:
    :return:
    """
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    return json_data


def copy_dict_remove_keys(resp_dict, remove_keys):
    # 移除响应字典中和URL相关的选项, 仅保留响应部分
    # {'HTTP_REQ_TARGET': 'https://www.baidu.com/home.rar',  # 需要排除
    # 'HTTP_CONST_SIGN': 'https://www.baidu.com/home.rar',  # 需要排除
    # 'HTTP_RESP_REDIRECT': 'RESP_REDIRECT_ORIGIN'}   # 可选排除
    # 保留原始dict数据
    copy_resp_dict = copy.copy(resp_dict)
    for remove_key in remove_keys:
        # copy_resp_dict[remove_key] = ""  # 清空指定键的值
        copy_resp_dict.pop(remove_key, "")  # 删除指定键并返回其对应的值 # 删除不存在的键时，指定默认值，不会引发异常
    # output(f"[*] 新的字典键数量:{len(copy_resp_dict.keys())}, 原始字典键数量:{len(data_dict.keys())}", level=LOG_DEBUG)
    return copy_resp_dict


def de_dup_dicts(dict_list):
    # 字典列表去重 保持原有顺序
    seen = set()
    unique_list = []
    for d in dict_list:
        # 将字典转换成元组，然后放入集合中
        dict_tuple = tuple(d.items())
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique_list.append(d)
    return unique_list


def dict_as_dict_value(data_dict, data_key):
    data_dict = [data_dict] if isinstance(data_dict, dict) else data_dict
    data_dict = {item[data_key]: item for item in data_dict}
    return data_dict
