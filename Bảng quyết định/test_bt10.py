# -*- coding: utf-8 -*-
"""
test_bt10.py - Chạy bằng pytest:  pytest -v test_bt10.py
Chọn bài:                          pytest -v test_bt10.py -k bai03
"""
import importlib

import pytest

import common
from run_all import MODULES

_CASES = []
for _n, _name in MODULES.items():
    _m = importlib.import_module(_name)
    for _c in _m.CASES:
        _CASES.append(pytest.param(_m, _c, id=f"bai{_n:02d}-{_c[0]}-{_c[1]}"))


@pytest.mark.parametrize("m,case", _CASES)
def test_thuc_thi(m, case):
    """sut trả đúng Expected."""
    _, _, inp, expected, _ = case
    assert m.sut(*inp) == expected


@pytest.mark.parametrize("m,case", _CASES)
def test_khop_bang_quyet_dinh(m, case):
    """Input của test khớp đúng 1 luật và đúng luật đã khai báo."""
    _, rule, inp, _, _ = case
    vec = common.tinh_dieu_kien(m, inp)
    assert common.luat_khop(m, vec) == [rule]
