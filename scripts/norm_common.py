# -*- coding: utf-8 -*-
"""
档案电子目录 · 字段规范化通用函数模板（可复用）

从「安福县总工会」项目的 _build_*.py 提炼，全宗号等参数化。
复制到目标项目后按需调整。依赖仅 openpyxl（本文件不依赖，仅提供字符串函数）。

用法示例：
    from norm_common import norm_dh, norm_wh, norm_tm, norm_zrz, norm_pg, norm_dt
    dh = norm_dh("1031-WS ·2006-Y-001")          # -> "1031-ws·2006-y-0001"
    wh = norm_wh("安工字【2013】1号")             # -> "安工字[2013]1号"
"""
import re

# 全宗号参数：按单位修改。总工会 1031 / 县委办 1001 / 统战部 1012
QUANZONG = "1031"


def clean(v):
    """去空值/换行/首尾空白。"""
    if v is None:
        return ""
    return str(v).replace("\n", " ").strip()


def norm_dh(s):
    """档号规范化：1031-WS ·2006-Y-001 → 1031-ws·2006-y-0001（小写、·无空格、件号4位）。"""
    if not s:
        return ""
    s = re.sub(r"[\s　]+", "", s)
    s = s.replace("·.", "·").replace("·。", "·")
    # OCR 单位误识修正
    s = s.replace("1012-s", "1012-ws").replace("1012-vs", "1012-ws")
    s = s.replace("1001-IS", "1001-WS").replace("-030-", "-D30-")
    s = s.replace("200S", "2006").replace("1996--", "1996-y-")
    # ws 后各种分隔符统一为 ·
    s = re.sub(r"ws[。，、＝→. ]", "ws·", s, flags=re.I)
    s = s.replace("ws-", "ws·").replace("ws_", "ws·")
    m = re.fullmatch(r"(\d{4})-([A-Za-z]+)·(\d{4})-([A-Za-z0-9]+)-(\d{1,4})", s)
    if m:
        qzh, ws, yr, code, no = m.groups()
        return f"{qzh}-{ws.lower()}·{yr}-{code.lower()}-{int(no):04d}"
    return s


def norm_wh(s):
    """文号规范化：方括号→半角[]；圆括号→全角（）；去空白；OCR 修正。"""
    if not s:
        return ""
    for a, b in (("【", "["), ("】", "]"), ("〔", "["), ("〕", "]"),
                 ("［", "["), ("］", "]"), ("「", "["), ("」", "]")):
        s = s.replace(a, b)
    s = s.replace("赣工宜", "赣工宣")
    s = re.sub(r"[\s　]+", "", s)
    s = s.replace("(", "（").replace(")", "）")
    s = s.replace(";", "；").replace(":", "：")
    s = s.replace("（[", "[")              # 去方括号前误入的左圆括号
    s = s.replace("].", "]")              # 去右方括号后误入的点
    s = re.sub(r"(\d)(?=[；])", r"\1号", s)  # 分号前数字缺「号」→ 补
    return s


def norm_tm(s):
    """题名规范化：去空格/标点；方括号→半角、圆括号→全角；书名号配对；OCR 修正。"""
    if not s:
        return ""
    for a, b in (("【", "["), ("】", "]"), ("〔", "["), ("〕", "]"),
                 ("［", "["), ("］", "]"), ("「", "["), ("」", "]")):
        s = s.replace(a, b)
    s = re.sub(r"[　]+", "", s)
    s = re.sub(r"[ ]+", "", s)
    s = s.replace("(", "（").replace(")", "）")
    s = s.lstrip("，,、。")
    # 明显 OCR 错误修正（可扩充）
    for a, b in (
        ("省计厅", "省审计厅"), ("全部推进", "全面推进"),
        ("三年茶规划", "三年规划"), ("注册会议师", "注册会计师"),
        ("企业民展", "企业发展"), ("全部财务部", "全总财务部"),
        ("奖励标准及法", "奖励标准及办法"), ("20110年度", "2011年度"),
        ("工次总额", "工资总额"), ("吉要市", "吉林市"),
        ("另星土建", "零星土建"), ("工令计算", "工龄计算"),
        ("地主建制", "地方建制"), ("苦命烈士", "革命烈士"),
        ("的通11", "的通知"), ("抓管理。增效益", "抓管理、增效益"),
        ("竞赛方案）的通知", "竞赛方案》的通知"), ("暂行办法）", "暂行办法＞"),
        ("赣工宜", "赣工宣"),
        ("印发《工会体育活动经费开支暂行规定", "印发《工会体育活动经费开支暂行规定》"),
    ):
        s = s.replace(a, b)
    s = re.sub(r"的通[0-9a-zA-Z]+$", "的通知", s)   # 结尾 OCR 乱码
    s = re.sub(r"(?<=\d),(?=\d)", "、", s)          # 数字间半角逗号→顿号
    # 书名号配对：开多于闭 → 末尾补闭号
    if s.count("《") > s.count("》"):
        if s.endswith("）"):
            s = s[:-1] + "》"
        else:
            s += "》"
    return s


def norm_zrz(s):
    """责任者规范化：去空白；多机构分隔统一；OCR 修正。"""
    if not s:
        return ""
    s = re.sub(r"[\s　]+", "", s)
    for a, b in (
        ("办公宝", "办公室"), ("人事斤", "人事厅"),
        ("经审查委员会", "经费审查委员会"),
        ("吉安市总保障部", "吉安市总工会保障部"),
        ("总工会人バ", "总工会"), ("地.区民宗局", "地区民宗局"),
    ):
        s = s.replace(a, b)
    s = re.sub(r"[゠-ヿ]+$", "", s)   # 去尾部片假名残留
    s = s.replace("：", "；")         # 多机构分隔统一全角分号
    return s


def norm_pg(s):
    """页数规范化：数字补 3 位；区间两端各补 3 位。"""
    if not s:
        return ""
    s = s.strip()
    if not s:
        return ""
    parts = re.split(r"[-—~]", s)
    if len(parts) >= 2:
        a, b = parts[0], parts[-1]
        if a.isdigit() and b.isdigit():
            return f"{int(a):03d}-{int(b):03d}"
    if s.isdigit():
        return f"{int(s):03d}"
    return s


def norm_dt(s):
    """日期规范化：保留原 8 位字符串（仅到年/月合法：YYYY0000 / YYYYMM00）。"""
    s = s.strip()
    return s if re.fullmatch(r"\d{8}", s) else s


def date_ok(dt):
    """日期合法性判断：8 位；月 00 或 01-12；日 00-31。返回 (是否合法, 异常说明)。"""
    if not dt:
        return True, ""
    if not re.fullmatch(r"\d{8}", dt):
        return False, f"非8位({dt})"
    mm, dd = int(dt[4:6]), int(dt[6:8])
    if not ((mm == 0 and dd == 0) or (1 <= mm <= 12 and 0 <= dd <= 31)):
        return False, f"月份/日期非法({dt}: {mm}月{dd}日)"
    return True, ""


if __name__ == "__main__":
    # 自测
    tests = [
        norm_dh("1031-WS ·2006-Y-001"), "1031-ws·2006-y-0001",
        norm_dh("1012-s·1980-Y-11"), "1012-ws·1980-y-0011",
        norm_wh("安工字【2013】1号"), "安工字[2013]1号",
        norm_wh("吉工民字[2010].2号"), "吉工民字[2010]2号",
        norm_tm("关于20110年度考评的通知"), "关于2011年度考评的通知",
        norm_tm("关于印发《工会体育活动经费开支暂行规定"), "关于印发《工会体育活动经费开支暂行规定》",
        norm_zrz("吉安市总保障部"), "吉安市总工会保障部",
        norm_pg("12"), "012", norm_pg("12-24"), "012-024",
        norm_dt("20110300"), "20110300",
    ]
    for i in range(0, len(tests), 2):
        got, want = tests[i], tests[i + 1]
        mark = "OK" if got == want else "!!"
        print(f"[{mark}] {got!r} 期望 {want!r}")
    print("date_ok('20188927') ->", date_ok("20188927"))
    print("date_ok('20110000') ->", date_ok("20110000"))
