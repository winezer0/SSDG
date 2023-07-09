# -*- coding: utf-8 -*-
from libs.lib_chinese_pinyin.chinese_const import PY_OPTIMIZED

TRANSLATE_DICT = {
    "管理员": ["gly", "admin", "adm", "manager"],
    "超级": ["super"],
    "认证": ["auth"],
    "系统": ["sys", "system", "xi", "xitong"],
    "测试": ["ceshi", "cs", "test"],
    "用户": ["user", "man"],
    "日志": ["log", "logger"],
    "开发": ["dev"],
    "安全": ["sec", "security"],
    "审计": ["audit"],
    "运维": ["operator","yunwei"],
    "支持": ["support"],
    "反馈": ["fankui"],
    "备份": ["backup"],
    "普通": ["base"],
    "文章": ["article"],
    "发布员": ["publisher"],
    "发布者": ["publisher"],

    # "管理员": ["admin", "administrator", "manager", "supervisor", "overseer", "director", "executive", "coordinator",
    #         "controller", "superintendent", "chief", "head", "leader", "boss", "adm", "mgr", "exec"],
    # "用户名": ["username", "user", "login name"],
    # "账号": ["account", "user account", "login account", "user profile", "user credential"],
    # "密码": ["password", "passphrase", "access code", "secret key", "PIN", "passcode", "login code"],
    # "认证": ["authentication", "verification", "validation", "user identity confirmation", "user proofing"],
    # "操作管理员": ["operational administrator", "operational manager", "operational support", "operational staff", "operations team"],
    # "审计管理员": ["audit administrator", "audit manager", "audit support", "audit staff", "audit team", "compliance team"],
    # "权限": ["permission", "access rights", "privilege", "authority", "entitlement", "clearance"],
    # "角色": ["role", "user role", "access role", "permission role"],
    # "口令": ["passphrase", "password", "secret code", "login code", "access code", "security token"],
    # "鉴权": ["authorization", "authentication and authorization", "access control", "permission control"],
    # "令牌": ["token", "security token", "access token", "authentication token", "verification token", "one-time password (OTP)"],
    # "会话": ["session", "login session", "user session", "authentication session", "secure session"],
    # "注册": ["register", "user registration", "account registration", "signup"],
    # "登录": ["login", "user login", "sign in", "logon"],
    # "注销": ["logout", "user logout", "sign out"],
    # "安全问题": ["security question", "account recovery question", "challenge question", "verification question"],
    # "多因素认证": ["multi-factor authentication", "MFA", "two-factor authentication", "2FA", "three-factor authentication", "3FA"],
    # "双重认证": ["dual authentication", "dual-factor authentication", "two-step verification", "2SV", "two-step authentication", "2SA"],
    # "短信验证": ["SMS verification", "text message verification", "mobile verification", "phone verification"]
}
XIN_NAMES_DICT = {
    1: ['张', '王', '李', '刘', '陈', '杨', '黄', '孙', '周', '吴', '徐', '赵', '朱', '马', '胡', '郭', '林', '何', '高', '梁',
        '郑', '罗', '宋', '谢', '唐', '韩', '曹', '许', '邓', '萧', '冯', '曾', '程', '蔡', '彭', '潘', '袁', '于', '董', '余', '苏',
        '叶', '吕', '魏', '蒋', '田', '杜', '丁', '沈', '姜', '范', '江', '傅', '钟', '卢', '汪', '戴', '崔', '任', '陆', '廖', '姚',
        '方', '金', '邱', '夏', '谭', '韦', '贾', '邹', '石', '熊', '孟', '秦', '阎', '薛', '侯', '雷', '白', '龙', '段', '郝', '孔',
        '邵', '史', '毛', '常', '万', '顾', '赖', '武', '康', '贺', '严', '尹', '钱', '施', '牛', '洪', '龚', '汤', '陶', '黎', '温',
        '莫', '易', '樊', '乔', '文', '安', '殷', '颜', '庄', '章', '鲁', '倪', '庞', '邢', '俞', '翟', '蓝', '聂', '齐', '向', '申',
        '葛', '柴', '伍', '覃', '骆', '关', '焦', '柳', '欧', '祝', '纪', '尚', '毕', '耿', '芦', '左', '季', '管', '符', '辛', '苗',
        '詹', '曲', '靳', '祁', '路', '涂', '兰', '甘', '裴', '梅', '童', '翁', '霍', '游', '阮', '尤', '岳', '柯', '牟', '滕',
        '谷', '舒', '卜', '成', '饶', '宁', '凌', '盛', '查', '单', '冉', '鲍', '华', '包', '屈', '房', '喻', '解', '蒲', '卫', '简',
        '时', '连', '车', '项', '闵', '邬', '吉', '党', '阳', '司', '费', '蒙', '席', '晏', '隋', '古', '强', '穆', '姬', '宫', '景',
        '米', '麦', '谈', '柏', '瞿', '艾', '沙', '鄢', '桂', '窦', '郁', '缪', '畅', '巩', '卓', '褚', '栾', '戚', '全', '娄', '甄',
        '郎', '池', '丛', '边', '岑', '农', '苟', '迟', '保', '商', '臧', '佘', '卞', '虞', '刁', '冷', '应', '匡', '栗', '仇', '练',
        '楚', '揭', '师', '官', '佟', '封', '燕', '桑', '巫', '敖', '原', '植', '邝', '仲', '荆', '储', '宗', '楼', '干', '苑', '寇',
        '盖', '南', '屠', '鞠', '荣', '井', '乐', '银', '奚', '明', '麻', '雍', '花', '闻', '冼', '木', '郜', '廉', '衣', '蔺', '和',
        '冀', '占', '公', '门', '慕容'],
    2: ['欧阳', '端木', '上官', '慕容', '东方', '司马', '独孤', '夏侯', '诸葛', '公孙'],
    # 3: ['阿伏干', '阿勒根', '阿史德', '阿史那', '阿逸多', '拔列兰', '白杨提', '孛术鲁', '布叔满', '步大汗', '步六孤', '步鹿根'],
    # 4: ['叶赫那拉', '西林觉罗', '乌珠穆沁', '敖陶格图', '鄂齐卓他', '敖勒多尔', '果尔勒斯', '克里叶特', '罕吉拉锦']
}


# 对姓氏字典进行优化
def optimize_xin_names_dict(xin_names_dict={}):
    # 对姓氏字典进行优化

    # 判断字典是否包含optimized记录
    if PY_OPTIMIZED in xin_names_dict:
        return xin_names_dict

    # 检查姓氏字典格式是否正确
    fixed = "$$$"
    for key in list(xin_names_dict.keys()):
        for index, xin in enumerate(xin_names_dict[key]):
            if len(xin) != key:
                # print(f"发现分类不正确的姓氏 {key} <--> {xin}")
                # 将该姓氏移动到指定长度的位置
                if len(xin) in xin_names_dict.keys():
                    xin_names_dict[key][index] = fixed
                    xin_names_dict[len(xin)].append(xin)
                else:
                    xin_names_dict[len(xin)] = [xin]
        # 去掉标记的fix字符
        xin_names_dict[key] = [xin for xin in xin_names_dict[key] if xin != fixed]

    # 优化完成记录
    xin_names_dict[PY_OPTIMIZED] = PY_OPTIMIZED

    return xin_names_dict


# 返回 内置 姓氏 字典的 键值对
def gen_xin_names_dict_and_key_list(xin_names_dict):
    # 返回 内置 姓氏 字典的 键值对
    optimize_xin_names = optimize_xin_names_dict(xin_names_dict)
    optimize_xin_names_key = [key for key in list(optimize_xin_names.keys()) if isinstance(key, int)]
    optimize_xin_names_key.sort(reverse=True)  # 使用sort()方法按数字大小倒序排列
    return optimize_xin_names, optimize_xin_names_key
