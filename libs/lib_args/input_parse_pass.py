#!/usr/bin/env python
# encoding: utf-8

# 解析输入参数
import argparse
from pyfiglet import Figlet

from libs.lib_args.input_basic import extract_heads
from libs.lib_args.input_const import *
from libs.lib_log_print.logger_printer import LOG_ERROR, output


def args_parser(config_dict):
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = Figlet().renderText("SSDG")

    # 动态实现重复参数设置代码  # 可提取到函数外正常使用
    # 规则示例: { "param": "", "dest": "","name": "", "default": "", "nargs": "","action": "",  "choices": "", "type": "","help": ""}
    args_options = [
        # 指定扫描URL或文件
        {"param": GB_TARGET, "help": f"URL目标 用于提取部分域名信息"},

        # 指定 生成 账号密码对的账号字典
        {"param": GB_BASE_NAME_FILE, "help": f"账号字典 用于编写账号密码对字典"},

        # 指定字典后缀名列表
        {"param": GB_BASE_DICT_SUFFIX, "nargs": "+", "help": "需要调用的密码规则元素文件后缀"},

        {"param": GB_RULE_LEVEL_PASS, "type": int, "help": "指定密码规则文件的级别"},

        {"param": GB_RULE_LEVEL_EXACT, "action": "store_true", "default": False, "help": "是否精确选择字典文件 默认选择小于等于指定级别的规则"},

        {"param": GB_EXCLUDE_FLAG, "action": "store_true", "help": "过滤已经爆破过的账号密码对文件 开关"},
        {"param": GB_EXCLUDE_FILE, "help": "过滤已经爆破过的账号密码对文件 名称"},
        {"param": GB_CONST_LINK, "help": "过滤已经爆破过的账号密码对文件 连接符"},

        # 开启调试功能
        {"param": GB_DEBUG_FLAG, "action": "store_true", "help": "显示调试信息"},
    ]

    param_dict = {}  # 存储所有长-短 参数对应关系,用于自动处理重复的短参数名
    options_to_argument(args_options, argument_parser, config_dict, param_dict)

    # 其他输出信息
    shell_name = argument_parser.prog
    argument_parser.epilog = f"""Examples:
             \r  Version: {config_dict[GB_VERSION]}"""

    args = argument_parser.parse_args()
    return args


def args_dict_handle(args):
    # 记录已经更新过的数据
    update_dict = {}
    # # 格式化输入的Proxy参数 如果输入了代理参数就会变为字符串
    # if args.proxies and isinstance(args.proxies, str):
    #     if "socks" in args.proxies or "http" in args.proxies:
    #         args.proxies = {
    #             'http': args.proxies.replace('https://', 'http://'),
    #             'https': args.proxies.replace('https://', 'http://')
    #         }
    #         update_dict["proxies"] = args.proxies
    #     else:
    #         output(f"[!] 输入的代理地址[{args.proxies}]不正确,正确格式:Proto://IP:PORT", level=LOG_ERROR)
    return update_dict


def config_dict_handle(config_dict):
    # 记录已经更新过的数据
    update_dict = {}
    # # 格式化输入的规则目录
    # if not config_dict[GB_DICT_RULE_SCAN]:
    #     config_dict[GB_DICT_RULE_SCAN] = get_sub_dirs(config_dict[GB_DICT_RULE_PATH])
    #     update_dict[GB_DICT_RULE_SCAN] = config_dict[GB_DICT_RULE_SCAN]
    #
    # # HTTP 头设置
    # config_dict[GB_REQ_HEADERS] = {
    #     'User-Agent': random_useragent(HTTP_USER_AGENTS, config_dict[GB_RANDOM_UA]),
    #     'X_FORWARDED_FOR': random_x_forwarded_for(config_dict[GB_RANDOM_XFF]),
    #     'Accept-Encoding': ''
    # }
    # update_dict[GB_REQ_HEADERS] = config_dict[GB_REQ_HEADERS]
    return update_dict


def options_to_argument(args_options, argument_parser, config_dict, param_dict):
    """
    将参数字典转换为参数选项
    :param args_options:
    :param argument_parser:
    :param config_dict:
    :param param_dict: 全局变量<-->短参数对应关系字典
    :return:
    """
    support_list = ["param", "dest", "name", "default", "nargs", "action", "choices", "type", "help"]
    for option in args_options:
        # 跳过空字典
        if not option:
            continue

        try:
            # 使用 issubset() 方法判断字典的所有键是否都是列表 support_list 的子集
            if not set(option.keys()).issubset(support_list):
                not_allowed_keys = set(option.keys()) - set(support_list)
                output(f"[!] 参数选项:[{option}]存在非预期参数[{not_allowed_keys}]!!!", level=LOG_ERROR)
            else:
                gb_param = option["param"]
                tmp_dest = vars_to_param(gb_param) if "dest" not in option.keys() else option["dest"]
                tmp_name = extract_heads(tmp_dest, param_dict) if "name" not in option.keys() else option["name"]
                tmp_default = config_dict[gb_param] if "default" not in option.keys() else option["default"]
                tmp_nargs = None if "nargs" not in option.keys() else option["nargs"]
                tmp_action = None if "action" not in option.keys() else option["action"]
                tmp_help = f"Specify the {vars_to_param(gb_param)}" if "help" not in option.keys() else option["help"]
                tmp_type = None if "type" not in option.keys() else option["type"]
                tmp_choices = None if "choices" not in option.keys() else option["choices"]

                # 存储长短参数对应关系
                param_dict[gb_param] = tmp_name

                if tmp_action:
                    argument_parser.add_argument(f"-{tmp_name.strip('-')}",
                                                 f"--{tmp_dest.strip('-')}",
                                                 default=tmp_default,
                                                 action=tmp_action,
                                                 # type=tmp_type,  # type 互斥 action
                                                 # nargs=tmp_nargs,  # type 互斥 action
                                                 # choices=tmp_choices,
                                                 help=f"{tmp_help}. Default Is [{tmp_default}]. Action Is {tmp_action}.",
                                                 )
                else:
                    # 当设置nargs参数时, 不能设置action, 需要分别设置
                    argument_parser.add_argument(f"-{tmp_name.strip('-')}",
                                                 f"--{tmp_dest.strip('-')}",
                                                 default=tmp_default,
                                                 nargs=tmp_nargs,
                                                 type=tmp_type,
                                                 choices=tmp_choices,
                                                 help=f"{tmp_help}. Default Is [{tmp_default}].",
                                                 )
        except Exception as error:
            output(f"[!] 参数选项 {option} 解析发生错误, ERROR:{error}", level=LOG_ERROR)
            exit()


def vars_to_param(var_name):
    # 实现全局变量到参数名的自动转换,和 config_dict_add_args中的修改过程相反
    # 基于变量的值实现，要求 变量="变量", 如:GB_PROXIES="GB_PROXIES"
    # param_name = str(var_name).replace("GB_", "").lower()
    # 基于变量名的更通用的实现, 要求变量是全局变量.
    param_name = str(globals()[var_name]).replace("GB_", "").lower()
    return param_name



