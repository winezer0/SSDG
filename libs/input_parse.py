# 解析输入参数
import argparse
from pyfiglet import Figlet
from libs.input_const import *
from libs.lib_log_print.logger_printer import LOG_ERROR, LOG_INFO, output


def args_parser(config_dict):
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = Figlet().renderText("SSDG")

    # 动态实现重复参数设置代码  # 可提取到函数外正常使用
    # 规则示例: { "param": "", "dest": "","name": "", "default": "", "nargs": "","action": "",  "choices": "", "type": "","help": ""}
    args_options = [
        # 指定扫描URL或文件
        {"param": GB_TARGET, "help": f"Specify the blasting Target url"},

        # 指定字典后缀名列表
        {"param": GB_BASE_DICT_SUFFIX, "nargs": "+", "help": "Specifies Base Var File Suffix"},

        {"param": GB_RULE_LEVEL_NAME, "type": int, "help": "Specifies the name rule file level or prefix"},
        {"param": GB_RULE_LEVEL_PASS, "type": int, "help": "Specifies the pass rule file level or prefix"},
        {"param": GB_RULE_LEVEL_PAIR, "type": int, "help": "Specifies the pair rule file level or prefix"},

        {"param": GB_RULE_LEVEL_EXACT, "action": "store_false", "help": "Specifies Exact call level dictionary"},

        {"param": GB_PAIR_FILE_FLAG, "action": "store_false", "help": "Specifies Use Piar File"},
        {"param": GB_PAIR_LINK_SYMBOL, "help": "Specifies Name Pass Link Symbol in history file"},

        {"param": GB_EXCLUDE_FLAG, "action": "store_true", "help": "Specifies exclude history file flag"},
        {"param": GB_EXCLUDE_FILE, "help": "Specifies exclude history file name"},
        {"param": GB_CONST_LINK, "help": "Specifies Name Pass Link Symbol in history file"},

        # 开启调试功能
        {"param": GB_DEBUG_FLAG, "action": "store_true", "help": "Specifies Display Debug Info"},
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
                tmp_param = option["param"]
                tmp_dest = vars_to_param(tmp_param) if "dest" not in option.keys() else option["dest"]
                tmp_name = extract_heads(tmp_dest, param_dict) if "name" not in option.keys() else option["name"]
                tmp_default = config_dict[tmp_param] if "default" not in option.keys() else option["default"]
                tmp_nargs = None if "nargs" not in option.keys() else option["nargs"]
                tmp_action = None if "action" not in option.keys() else option["action"]
                tmp_help = f"Specify the {vars_to_param(tmp_param)}" if "help" not in option.keys() else option["help"]
                tmp_type = None if "type" not in option.keys() else option["type"]
                tmp_choices = None if "choices" not in option.keys() else option["choices"]

                # 存储长短参数对应关系
                param_dict[tmp_param] = tmp_name

                # 开始添加参数信息
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


def extract_heads(param_len, param_dict):
    # 实现提取字符串首字母的函数,作为参数名, 需要考虑重复问题
    initials = [word[0] for word in param_len.split("_")]  # 提取每个单词的首字母
    initials = "".join(initials)  # 将所有首字母拼接成一个字符串

    # 需要 param_dict 字典的值是短参数名
    if initials not in param_dict.values():
        return initials
    else:
        # 处理重复项问题
        i = 0
        while True:
            i += 1
            new_initials = f"{initials}{i}"
            if new_initials not in param_dict.values():
                break
        return new_initials


def vars_to_param(var_name):
    # 实现全局变量到参数名的自动转换,和 config_dict_add_args中的修改过程相反
    # 基于变量的值实现，要求 变量="变量", 如:GB_PROXIES="GB_PROXIES"
    # param_name = str(var_name).replace("GB_", "").lower()
    # 基于变量名的更通用的实现, 要求变量是全局变量.
    param_name = str(globals()[var_name]).replace("GB_", "").lower()
    return param_name


def config_dict_add_args(config_dict, args):
    # 使用字典解压将参数 直接赋值给相应的全局变量
    # 要求args参数命名要和字典的键 统一（完全相同或可以变为完全相同）
    for param_name, param_value in vars(args).items():
        var_name = f"GB_{param_name.upper()}"
        try:
            # globals()[var_name] = param_value # 赋值全局变量,仅本文件可用
            # output(f"[*] INPUT:{var_name} -> {param_value}", level=LOG_ERROR)
            config_dict[var_name] = param_value  # 赋值全局字典,所有文件可用
            if var_name not in config_dict.keys():
                output(f"[-] 非预期参数将被赋值: {var_name} <--> {param_value}", level=LOG_ERROR)
        except Exception as error:
            output(f"[!] 更新参数发生错误: {error}", level=LOG_ERROR)
            exit()
    return


def show_config_dict(config_dict):
    # 输出 config_dict 字典
    for index, param_name in enumerate(config_dict.keys()):
        param_val = config_dict[param_name]
        output(f"[*] Param_{index} {param_name} <--> {param_val}", level=LOG_INFO)
