# -*- coding: utf-8 -*-
"""pytest 单测：norm_common 规范化函数与日期规则。运行：python -m pytest scripts/test_norm_common.py"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import norm_common as nc


# ---------- 档号 ----------
def test_norm_dh_standard():
    assert nc.norm_dh("1031-WS ·2006-Y-001") == "1031-ws·2006-y-0001"


def test_norm_dh_pad_no():
    assert nc.norm_dh("1031-ws·1980-y-11") == "1031-ws·1980-y-0011"


def test_norm_dh_ocr_ws():
    assert nc.norm_dh("1012-s·1980-Y-11") == "1012-ws·1980-y-0011"


def test_norm_dh_d30():
    assert nc.norm_dh("1031-WS ·2009-D30-0029") == "1031-ws·2009-d30-0029"


def test_norm_dh_1001():
    assert nc.norm_dh("1001-IS-2013-D30-1") == "1001-ws·2013-d30-0001"


# ---------- 文号 ----------
def test_norm_wh_brackets():
    assert nc.norm_wh("安工字【2013】1号") == "安工字[2013]1号"


def test_norm_wh_dot_after_bracket():
    assert nc.norm_wh("吉工民字[2010].2号") == "吉工民字[2010]2号"


def test_norm_wh_left_paren_before_bracket():
    assert nc.norm_wh("赣工（【2009】39号") == "赣工[2009]39号"


def test_norm_wh_semicolon_hao():
    assert nc.norm_wh("第22；") == "第22号；"


def test_norm_wh_blank():
    assert nc.norm_wh("") == ""


# ---------- 题名 ----------
def test_norm_tm_year_ocr():
    assert nc.norm_tm("关于20110年度考评的通知") == "关于2011年度考评的通知"


def test_norm_tm_close_guillemet():
    assert nc.norm_tm("关于印发《工会体育活动经费开支暂行规定") == "关于印发《工会体育活动经费开支暂行规定》"


def test_norm_tm_comma_to_dun():
    assert nc.norm_tm("第8-11,14-15期") == "第8-11、14-15期"


def test_norm_tm_blank():
    assert nc.norm_tm("") == ""


# ---------- 责任者 ----------
def test_norm_zrz_dept():
    assert nc.norm_zrz("吉安市总保障部") == "吉安市总工会保障部"


def test_norm_zrz_dot():
    assert nc.norm_zrz("地.区民宗局") == "地区民宗局"


def test_norm_zrz_separator():
    assert nc.norm_zrz("甲：乙") == "甲；乙"


# ---------- 页数 ----------
def test_norm_pg_single():
    assert nc.norm_pg("12") == "012"


def test_norm_pg_range():
    assert nc.norm_pg("12-24") == "012-024"


def test_norm_pg_range_old():
    assert nc.norm_pg("001-004") == "001-004"


# ---------- 日期规则 ----------
def test_date_ok_valid_year():
    ok, _ = nc.date_ok("20110000")
    assert ok


def test_date_ok_valid_month():
    ok, _ = nc.date_ok("20110300")
    assert ok


def test_date_ok_valid_day():
    ok, _ = nc.date_ok("20180927")
    assert ok


def test_date_ok_illegal_month():
    ok, why = nc.date_ok("20188927")
    assert not ok
    assert "89月" in why


def test_date_ok_short():
    ok, why = nc.date_ok("2019000")
    assert not ok
    assert "非8位" in why
