#!/usr/bin/env python
# encoding: utf-8
import copy
import itertools
import re

from libs.lib_log_print.logger_printer import output, LOG_ERROR
from libs.lib_run_str_attr.str_attr_const import *
from libs.lib_social_dict.repl_const import SO_PASS_KEEP, SO_PASS_SEGMENT, SO_PASS_INDEXED, SO_PASS_REPL


# 对字符串进行进行指定字符替换
def replace_symbol_by_dict(raw_string, action_dict_list):
    str_list = []
    for replace_dict in action_dict_list:
        copy_string = copy.copy(raw_string)
        for old_symbol, new_symbol in replace_dict.items():
            if old_symbol in str(copy_string):
                copy_string = str(copy_string).replace(old_symbol, new_symbol)
        str_list.append(copy_string)
    return str_list


# 对动作简写进行还原 # U -> upper | L -> lower | C -> cap | T ->title
def repair_shorthand_action_dict(action_dict):
    # 对动作简写进行还原 # U -> upper | L -> lower | C -> cap | T ->title
    long_actions = [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],
    for seg, short_action in action_dict.items():
        for long_action in long_actions:
            if long_action.startswith(str(short_action).lower()):
                action_dict[seg] = long_action
    return action_dict


# 检查规则的动作是否正确
def is_allowed_action_dict(action_dict):
    # 检查规则的动作是否正确
    status = True
    allow_actions = [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER],
    for action in list(action_dict.values()):
        if action not in allow_actions:
            output(f"[!] 动作错误 {action_dict} <--> {action} not in {allow_actions}", level=LOG_ERROR)
            status = False
    return status


# 对字符串进行指定段的字母大小写处理
def handle_alpha_by_seg(base_pass, action_dict_list):
    str_list = []

    # 仅处理存在英文的情况
    if not re.search(r'[a-zA-Z]', base_pass):
        return str_list

    # 仅获取其中字母元素,用于按字母段定位
    raw_split = re.split(r'([a-zA-Z]+)', base_pass)
    raw_split = [s for s in raw_split if s != '']  # 去除空字符串

    raw_split = split_keyboard_string(raw_split)

    raw_alphas = [item for item in raw_split if bool(re.match(r'^[a-zA-Z]+$', item))]  # 不能用 isalpha()
    if raw_alphas:
        for action_dict in action_dict_list:
            # 还原简写规则
            action_dict = repair_shorthand_action_dict(action_dict)
            # 判断规则动作是否合法
            if is_allowed_action_dict(action_dict):
                # 保留原始元素
                copy_split = copy.copy(raw_split)
                # 当存在*的情况要求将所有元素先进行小写处理
                if "*" in list(action_dict.keys()):
                    action = action_dict["*"]
                    copy_split = [getattr(x, action)() for x in copy_split]
                for seg, action in action_dict.items():
                    if isinstance(seg, int) and seg < len(copy_split):
                        # getattr 函数可以根据传入的对象和属性名获取属性值，而字符串的内置方法 upper 可以将字符串转换为大写。
                        copy_split[seg] = getattr(copy_split[seg], action)()
                str_list.append("".join(copy_split))
    return str_list


def split_keyboard_string(raw_split):
    # 切割类似 qaz wsx的键盘字符串
    def list_to_re_str(replace_list, bracket=True):
        # 将列表转换为正则规则
        if replace_list:
            # 使用列表推导式和re.escape()自动转义为正则表达式中的文字字符
            regexp = '|'.join(re.escape(item) for item in replace_list)
        else:
            regexp = ""

        if bracket:
            replace_str = f'({regexp})'
        else:
            replace_str = f'{regexp}'
        return replace_str

    regex_list = ['qaz', 'wsx', 'edc', 'qwe', 'asd', 'zxc', 'qwer', 'asdf', 'zxcv', ]
    min_len = len(min(regex_list, key=len))

    # 按照长度从长到短排序
    regex_list = sorted(regex_list, key=lambda x: len(x), reverse=True)
    regex_str = list_to_re_str(regex_list, bracket=True)

    new_split = []
    for string in raw_split:
        if len(string) > min_len * 2 and bool(re.match(r'^[a-zA-Z]+$', string)):
            tmp_split = re.split(r'{}'.format(regex_str), string)
            tmp_split = [s for s in tmp_split if s != '']  # 去除空字符串
            new_split.extend(tmp_split)
        else:
            new_split.append(string)
    return new_split


# 对字符串进行指定索引的字母大小写处理
def handle_alpha_by_index(base_pass, action_dict_list):
    str_list = []
    # 仅处理存在英文的情况
    if not re.search(r'[a-zA-Z]', base_pass):
        return str_list

    for action_dict in action_dict_list:
        # 还原简写规则
        action_dict = repair_shorthand_action_dict(action_dict)
        # 判断规则动作是否合法
        if is_allowed_action_dict(action_dict):
            # 保留原始元素
            copy_pass = copy.copy(base_pass)
            # 当存在*的情况要求将所有元素先进行小写处理
            if "*" in list(action_dict.keys()):
                action = action_dict["*"]
                copy_pass = getattr(copy_pass, action)()
            for seg, action in action_dict.items():
                if isinstance(seg, int) and seg < len(copy_pass):
                    copy_split = list(copy_pass)
                    # getattr 函数可以根据传入的对象和属性名获取属性值，而字符串的内置方法 upper 可以将字符串转换为大写。
                    copy_split[seg] = getattr(copy_split[seg], action)()
                    str_list.append("".join(copy_split))
            str_list.append("".join(copy_pass))
    return str_list


# 变形 [(user:pass)] 中的pass为其他格式
def transfer_passwd(user_pass_pair_list, options_dict):
    new_user_pass_pair_list = []

    for base_name, base_pass in user_pass_pair_list:
        # 生成其他账号密码
        user_name_list = [base_name]
        user_pass_list = []

        # 保留原始密码|同时进行原始用户名的替换
        if options_dict[SO_PASS_KEEP]:
            user_pass_list.append(base_pass)

        # 进行 自定义的 字符替换
        if options_dict[SO_PASS_REPL]:
            new_str_list = replace_symbol_by_dict(base_pass, options_dict[SO_PASS_REPL])
            user_pass_list.extend(new_str_list)

        # 对密码中的英文进行大小写处理
        # 对第N段字符进行全部大小写
        if options_dict[SO_PASS_SEGMENT]:
            new_str_list = handle_alpha_by_seg(base_pass, options_dict[SO_PASS_SEGMENT])
            user_pass_list.extend(new_str_list)

        # 对前N个字符进行大小写
        if options_dict[SO_PASS_INDEXED]:
            new_str_list = handle_alpha_by_index(base_pass, options_dict[SO_PASS_INDEXED])
            user_pass_list.extend(new_str_list)

        # 去重和填充用户名密码元素
        user_pass_list = list(set(user_pass_list)) if len(user_pass_list) > 1 else [base_pass]
        # 组合账户密码 并存入
        product_list = list(itertools.product(user_name_list, user_pass_list))
        new_user_pass_pair_list.extend(product_list)
    return new_user_pass_pair_list


if __name__ == '__main__':
    pair_list = [("admin", "password密码")]
    options = {
        SO_PASS_KEEP: True,

        SO_PASS_REPL: [{"o": "0"},
                       {"o": "@"},
                       ],

        SO_PASS_SEGMENT: [
            {0: "upper"},
            {1: "upper"},
            {0: "upper", 1: "upper"},
            {0: "upper", 2: "upper"},
            {0: "upper", "*": "lower"},
        ],

        SO_PASS_INDEXED: [
            # {1:"upper","*":"lower"},
            # {0: "upper", "*": "lower"},
            # {-1: "lower", "*": "u"},
        ]
    }

    print(transfer_passwd(pair_list, options))
    # [('admin', 'passw@rd'), ('admin', 'passw0rd'), ('admin', 'password')]
