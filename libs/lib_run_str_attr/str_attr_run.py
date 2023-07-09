from libs.lib_log_print.logger_printer import output, LOG_ERROR
from libs.lib_run_str_attr.str_attr_const import *


def repair_shorthand_action_list(action_list, long_actions):
    # 对动作简写进行还原 # U -> upper | L -> lower | C -> cap | T ->title
    for index, short_action in enumerate(action_list):
        for long_action in long_actions:
            if long_action.startswith(str(short_action).lower()):
                action_list[index] = long_action
    return action_list


def is_allowed_action_list(action_list, allow_actions):
    # 检查规则的动作是否正确
    status = True
    for action in action_list:
        if action not in allow_actions:
            output(f"[!] 动作错误 {action_list} <--> {action} not in {allow_actions}", level=LOG_ERROR)
            status = False
    return status


def string_run_attr(string, action_list):
    """执行字符串的属性方法"""
    new_value = []
    allow_actions = [ATTR_UPPER, ATTR_LOWER, ATTR_TITLE, ATTR_CAPER]
    action_list = repair_shorthand_action_list(action_list, allow_actions)
    if is_allowed_action_list(action_list, allow_actions):
        for action in action_list:
            tmp_v = getattr(string, action)()
            new_value.append(tmp_v)
    return new_value
