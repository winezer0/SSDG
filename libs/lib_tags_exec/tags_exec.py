import re

from libs.lib_log_print.logger_printer import output, LOG_ERROR
from libs.lib_tags_exec.tags_const import TAG_FUNC_DICT


# 动态调用函数处理参数
def dynamic_function_call(func_name, param, func_dict):
    if func_name in func_dict.keys():
        return func_dict[func_name](param)
    else:
        raise ValueError(f"Unknown function name: {func_name}")


# 提取函数名和参数
def extract_func_and_param(tag_string):
    pattern = r"<(\w+)>([^<>]+)</\w+>"
    match = re.match(pattern, tag_string)
    if match:
        func_name = match.group(1)
        param = match.group(2)
        return func_name, param
    else:
        return None, None


# 执行解析标签
def process_tag(tag_string, func_dict):
    func_name, param = extract_func_and_param(tag_string)
    if func_name:
        try:
            tag_string = dynamic_function_call(func_name, param, func_dict)
            return tag_string
        except Exception as error:
            if "object is not callable" in str(error):
                output(f"[!] 执行解析标签出错 [{tag_string}] func_name:[{func_name}] param:[{param}] "
                       f"error:[TAG_FUNC_DICT 格式错误]", level=LOG_ERROR)
            else:
                output(f"[!] 执行解析标签出错 [{tag_string}] func_name:[{func_name}] param:[{param}] "
                       f"error:[{str(error)}]", level=LOG_ERROR)
            exit()
    return tag_string


# 检查标签的表层错误
def find_tag_skin_error(string):
    pattern = r"<\w+>[^<>]+<\w+>"
    if re.findall(pattern, string):
        return True
    return False


# 检查标签的深层错误 一次只能检查一个标签
def find_tag_deep_error(tag_string, func_dict):
    pattern = r"<(\w+)>([^<>]+)</(\w+)>"
    match = re.match(pattern, tag_string)
    groups = match.groups()
    if len(groups) == 3 and match.group(1) == match.group(3) and match.group(1) in func_dict.keys():
        return False
    return True


# 获取字符串内的符合语法的的标签格式
def find_grammar_tags(string):
    pattern = r"<\w+>[^<>]+</\w+>"
    tags = re.findall(pattern, string)
    return tags


# 获取合法的标签
def get_legal_tags(string, func_dict):
    legal_tags = []
    grammar_tags = find_grammar_tags(string)
    for grammar_tag in grammar_tags:
        if not find_tag_deep_error(grammar_tag, func_dict):
            legal_tags.append(grammar_tag)
    return legal_tags


# 初步发现错误标签
def find_string_tag_error(string_list, func_dict):
    for string in string_list:
        if string and string.strip():
            if find_tag_skin_error(string):
                output(f"[!] 发现明显标签错误 {string}", level=LOG_ERROR)
                return True
            for grammar_tag in find_grammar_tags(string):
                if find_tag_deep_error(grammar_tag, func_dict):
                    output(f"[!] 发现深度标签错误 {string}", level=LOG_ERROR)
                    return True
    return False


# 循环提取和解析字符串内的标签
def match_exec_repl_loop(string, func_dict):
    if string and string.count("<") > 2 and string.count("</") >= 1:
        while True:
            legal_tags = get_legal_tags(string, func_dict)
            # 不存在合法标签时结束
            if not legal_tags:
                break
            # 循环处理标签
            for tag in legal_tags:
                string = str(string).replace(tag, process_tag(tag, func_dict))
        return string
    else:
        return string


def match_exec_repl_loop_batch(string_list, func_dict):
    """
    对字符串列表进行批量标签执行
    :param string_list:
    :param func_dict:
    :return: 返回新的字符串列表
    """
    new_string_list = []
    for string in string_list:
        new_string = match_exec_repl_loop(string, func_dict)
        new_string_list.append(new_string)
    return new_string_list


if __name__ == '__main__':
    raw_string = "user=<url><b64>admin</b64></url>&password=<md5>123456</md5>"
    processed_string = match_exec_repl_loop(raw_string, TAG_FUNC_DICT)
    print(processed_string)
