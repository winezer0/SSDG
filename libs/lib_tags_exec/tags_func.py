import base64
import hashlib
import importlib.util
import inspect
import urllib.parse
import js2py

from libs.lib_file_operate.file_utils import file_is_exist
from libs.lib_file_operate.file_read import read_file_to_str
from libs.lib_log_print.logger_printer import output, LOG_ERROR

# 标签执行时调用的自定义js文件路径
TAG_EXEC_CUSTOM_JS_FILE = r"demo/custom.js"
# 标签执行时调用的自定义py文件路径
TAG_EXEC_CUSTOM_PY_FILE = r"demo/custom.py"


def none_encode(string=""):
    # 原样返回
    return string


def base64_encode(string=""):
    # base64编码
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def base64_safe_encode(string=""):
    # URL安全的Base64编码
    base64url = base64.urlsafe_b64encode(string.encode("utf-8"))
    base64url = base64url.rstrip(b'=')
    return base64url.decode("utf-8")


def md5_encode(string=""):
    # md5值计算
    return hashlib.md5(string.encode(encoding='utf-8')).hexdigest()


def url_encode(string=""):
    # url编码
    return urllib.parse.quote(string)


def str_upper(string=""):
    # 全部大写
    return str(string).upper()


def str_lower(string=""):
    # 全部小写
    return str(string).lower()


def str_capitalize(string=""):
    # 首字母大写
    return str(string).capitalize()


def str_split_4(string=""):
    # 截取前4个字符
    return string[:4]


def str_split_6(string=""):
    # 截取前6个字符
    return string[:6]


def str_split_8(string=""):
    # 截取前8个字符
    return string[:8]


def str_rsplit_4(string=""):
    # 截取后4个字符
    return string[-4:]


def str_rsplit_6(string=""):
    # 截取后6个字符
    return string[-6:]


def str_rsplit_8(string=""):
    # 截取后6个字符
    return string[-8:]


def str_reverse(string=""):
    # 字符串倒序
    return string[::-1]


def func_js2py(string="", js_file_path=None):
    # 动态调用js代码进行执行
    if not js_file_path:
        js_file_path = TAG_EXEC_CUSTOM_JS_FILE
    # 检查调用JS代码
    if js_file_path and file_is_exist(js_file_path):
        js_func_code = read_file_to_str(js_file_path, encoding=None, de_strip=False, de_unprintable=False)
        try:
            js2py_func = js2py.eval_js(js_func_code)
            return js2py_func(string)
        except Exception as error:
            output(f"[!]  JS FILE [{js_file_path}] EVAL ERROR!!! {str(error)}", level=LOG_ERROR)
            exit()
    else:
        output(f"[!] JS FILE [{js_file_path}] NOT FOUND !!!", level=LOG_ERROR)
        exit()


def func_mypy(string="", py_file_path=None):
    # 动态调用PY代码进行执行
    if not py_file_path:
        py_file_path = TAG_EXEC_CUSTOM_PY_FILE
    # 检查调用PY代码
    if py_file_path and file_is_exist(py_file_path):
        try:
            # 获取模块名称
            module_name = "my_module"
            # 使用 importlib 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, py_file_path)
            my_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(my_module)
            return my_module.run(string)
        except Exception as error:
            output(f"[!]  PY FILE [{py_file_path}] EVAL ERROR!!! {str(error)}", level=LOG_ERROR)
            exit()
    else:
        output(f"[!] PY FILE [{py_file_path}] NOT FOUND !!!", level=LOG_ERROR)
        exit()


def _function_names_():
    # 获取当前文件中定义的所有函数列表
    current_module = inspect.getmodule(inspect.currentframe())
    functions = inspect.getmembers(current_module, inspect.isfunction)
    # 需要被排除的函数
    exclude_list = ['_function_names_', 'file_is_exist', 'output', 'read_file_to_str']
    function_names = [f[0] for f in functions if f[0] not in exclude_list]
    return function_names


if __name__ == "__main__":
    print(_function_names_())
