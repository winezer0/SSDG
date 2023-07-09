from libs.lib_tags_exec.tags_func import *

##################################
# 支持的标签和字符串常量对应关系
TAG_B64 = "b64"
TAG_B64S = "b64s"
TAG_MD5 = "md5"
TAG_URL = "url"
TAG_NONE = "none"
TAG_UPPER = "upper"
TAG_LOWER = "lower"
TAG_CAPER = "caper"
TAG_JS2PY = "js2py"
TAG_MYPY = "mypy"

TAG_SP_4 = "sp4"
TAG_SP_6 = "sp6"
TAG_SP_8 = "sp8"

TAG_RSP_4 = "rsp4"
TAG_RSP_6 = "rsp6"
TAG_RSP_8 = "rsp8"

TAG_REVERSE = "revs"
##################################
# # 标签执行时调用的自定义js文件路径
# TAG_EXEC_CUSTOM_JS_FILE = r"demo/custom.js"
# # 标签执行时调用的自定义py文件路径
# TAG_EXEC_CUSTOM_PY_FILE = r"demo/custom.py"
##################################
# 支持的字符串常量和实际调用的函数的对应关系
# key=在报文中使用的名字,  value=被调用的函数名 不要带括号,会报错
TAG_FUNC_DICT = {
    TAG_B64: base64_encode,
    TAG_B64S: base64_safe_encode,
    TAG_MD5: md5_encode,
    TAG_URL: url_encode,
    TAG_NONE: none_encode,
    TAG_UPPER: str_upper,
    TAG_LOWER: str_lower,
    TAG_CAPER: str_capitalize,
    TAG_JS2PY: func_js2py,
    TAG_MYPY: func_mypy,

    TAG_SP_4: str_split_4,
    TAG_SP_6: str_split_6,
    TAG_SP_8: str_split_8,
    TAG_RSP_4: str_split_4,
    TAG_RSP_6: str_split_6,
    TAG_RSP_8: str_split_8,

    TAG_REVERSE: str_reverse,
}
##################################
