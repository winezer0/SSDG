from libs.lib_dyna_rule.dyna_rule_tools import list_ele_in_str
from libs.lib_filter_srting.filter_func_char import analyse_string_per_char, format_rule_list, regex_is_matched


# 过滤（账号,密码）元组列表
def exclude_pair_tuples_by_length(tuple_list,
                                  min_len_name, max_len_name,
                                  min_len_pass, max_len_pass,
                                  ignore_empty, ignore_symbols):
    # 对(账号,密码)元组列表进行长度过滤

    # 处理max_len赋值错误的情况
    if max_len_name <= min_len_name:
        max_len_name = 99

    if max_len_pass <= min_len_pass:
        max_len_pass = 99

    tuple_list = [(name_, pass_) for name_, pass_ in tuple_list
                  if ((ignore_empty and name_ == "")
                      or (ignore_symbols and list_ele_in_str(ignore_symbols, name_, default=False))
                      or (min_len_name <= len(name_) <= max_len_name))
                  and ((ignore_empty and pass_ == "")
                       or (ignore_symbols and list_ele_in_str(ignore_symbols, pass_, default=False))
                       or (min_len_pass <= len(pass_) <= max_len_pass))]
    return tuple_list


# 对字符串列表进行长度过滤
def exclude_string_list_by_length(string_list, min_len_str, max_len_str, ignore_empty, ignore_symbols):
    # 对字符串列表进行长度过滤

    # 处理max_len赋值错误的情况
    if max_len_str <= min_len_str:
        max_len_str = 99

    string_list = [string for string in string_list
                   if (ignore_empty and string == "")
                   or (ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False))
                   or (min_len_str <= len(string) <= max_len_str)]
    return string_list


# 排除包含指定符号的字符串
def exclude_string_list_by_symbols(string_list, ban_symbols_str, ignore_empty, ignore_symbols):
    string_list = [string for string in string_list
                   if (ignore_empty and string == "")
                   or (ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False))
                   or (not list_ele_in_str(ban_symbols_str, string, default=False))]
    return string_list


# 排除包含指定符号的字符串
def exclude_tuple_list_by_symbols(tuple_list, ban_symbols_name, ban_symbols_pass, ignore_empty, ignore_symbols):
    tuple_list = [(name_, pass_) for name_, pass_ in tuple_list
                  if ((ignore_empty and name_ == "")
                      or (ignore_symbols and list_ele_in_str(ignore_symbols, name_, default=False))
                      or (not list_ele_in_str(ban_symbols_name, name_, default=False)))
                  and ((ignore_empty and pass_ == "")
                       or (ignore_symbols and list_ele_in_str(ignore_symbols, pass_, default=False))
                       or (not list_ele_in_str(ban_symbols_pass, pass_, default=False)))
                  ]
    return tuple_list


# 基于输入的规则列表判断字符是否被提取
def extract_string_list_by_char_type(string_list, expected_rules_str, ignore_empty, ignore_symbols):
    # 基于输入的规则列表判断字符是否被提取
    # has_digit, has_upper, has_lower, has_symbol
    expected_rules_str = format_rule_list(expected_rules_str)
    string_list = [string for string in string_list
                   if (ignore_empty and string == "")
                   or (ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False))
                   or (analyse_string_per_char(string) in expected_rules_str)]
    return string_list


# 基于输入的规则列表判断字符是否被提取
def extract_tuple_list_by_char_type(tuple_list, expected_rules_name, expected_rules_pass, ignore_empty, ignore_symbols):
    # 基于输入的规则列表判断字符是否被提取
    expected_rules_name = format_rule_list(expected_rules_name)
    expected_rules_pass = format_rule_list(expected_rules_pass)

    # has_digit, has_upper, has_lower, has_symbol
    tuple_list = [(name_, pass_) for name_, pass_ in tuple_list
                  if ((ignore_empty and name_ == "")
                      or (ignore_symbols and list_ele_in_str(ignore_symbols, name_, default=False))
                      or (analyse_string_per_char(name_) in expected_rules_name))
                  and ((ignore_empty and pass_ == "")
                       or (ignore_symbols and list_ele_in_str(ignore_symbols, pass_, default=False))
                       or (analyse_string_per_char(pass_) in expected_rules_pass))]

    return tuple_list


# 基于输入的规则列表判断字符是否被排除
def exclude_string_list_by_char_type(string_list, expected_rules_str, ignore_empty, ignore_symbols):
    # 基于输入的规则列表判断字符是否被排除
    expected_rules_str = format_rule_list(expected_rules_str)
    # has_digit, has_upper, has_lower, has_symbol
    string_list = [string for string in string_list
                   if (ignore_empty and string == "")
                   or (ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False))
                   or (analyse_string_per_char(string) not in expected_rules_str)]
    return string_list


# 基于输入的规则列表判断字符是否被排除
def exclude_tuple_list_by_char_type(tuple_list, expected_rules_name, expected_rules_pass, ignore_empty, ignore_symbols):
    expected_rules_name = format_rule_list(expected_rules_name)
    expected_rules_pass = format_rule_list(expected_rules_pass)

    # has_digit, has_upper, has_lower, has_symbol, has_chinese
    tuple_list = [(name_, pass_) for name_, pass_ in tuple_list
                  if ((ignore_empty and name_ == "")
                      or (ignore_symbols and list_ele_in_str(ignore_symbols, name_, default=False))
                      or (analyse_string_per_char(name_) not in expected_rules_name))
                  and ((ignore_empty and pass_ == "")
                       or (ignore_symbols and list_ele_in_str(ignore_symbols, pass_, default=False))
                       or (analyse_string_per_char(pass_) not in expected_rules_pass))]
    return tuple_list


# 基于输入的正则列表判断字符是否被提取
def extract_string_list_by_regex(string_list, expected_regex_str, ignore_empty, ignore_symbols):
    # 基于输入的正则列表判断字符是否被提取
    string_list = [string for string in string_list
                   if (ignore_empty and string == "")
                   or (ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False))
                   or regex_is_matched(expected_regex_str, string)
                   ]
    return string_list


# 基于输入的正则列表判断字符是否被提取
def extract_tuple_list_by_regex(tuple_list, expected_regex_name, expected_regex_pass, ignore_empty, ignore_symbols):
    # 基于输入的正则列表判断字符是否被提取
    tuple_list = [(name_, pass_) for name_, pass_ in tuple_list
                  if ((ignore_empty and name_ == "")
                      or (ignore_symbols and list_ele_in_str(ignore_symbols, name_, default=False))
                      or regex_is_matched(expected_regex_name, name_)
                      )
                  and ((ignore_empty and pass_ == "")
                       or (ignore_symbols and list_ele_in_str(ignore_symbols, pass_, default=False))
                       or regex_is_matched(expected_regex_pass, pass_)
                       )]

    return tuple_list


# 基于输入的正则列表判断字符是否被排除
def exclude_string_list_by_regex(string_list, expected_regex_str, ignore_empty, ignore_symbols):
    # 基于输入的正则列表判断字符是否被排除
    string_list = [string for string in string_list
                   if (ignore_empty and string == "")
                   or (ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False))
                   or not regex_is_matched(expected_regex_str, string)
                   ]
    return string_list


# 基于输入的正则列表判断字符是否被排除
def exclude_tuple_list_by_regex(tuple_list, expected_regex_name, expected_regex_pass, ignore_empty, ignore_symbols):
    tuple_list = [(name_, pass_) for name_, pass_ in tuple_list
                  if ((ignore_empty and name_ == "")
                      or (ignore_symbols and list_ele_in_str(ignore_symbols, name_, default=False))
                      or not regex_is_matched(expected_regex_name, name_)
                      )
                  and ((ignore_empty and pass_ == "")
                       or (ignore_symbols and list_ele_in_str(ignore_symbols, pass_, default=False))
                       or not regex_is_matched(expected_regex_pass, pass_)
                       )]
    return tuple_list


