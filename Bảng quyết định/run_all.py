# -*- coding: utf-8 -*-
"""
run_all.py - Chạy test driver cho nhiều bài.

    python run_all.py              # cả 10 bài (chi tiết)
    python run_all.py 3            # chỉ bài 3
    python run_all.py 1 5 9        # bài 1, 5, 9
    python run_all.py 1-5          # bài 1 đến bài 5
    python run_all.py -q           # dạng gọn, mỗi test một dòng
    python run_all.py 4-6 -q       # kết hợp

Mã thoát 0 nếu mọi bài PASS và bảng quyết định khớp, 1 nếu có lỗi.
"""
import importlib
import sys

import common

MODULES = {
    1: "bai01_phi_giao_hang",
    2: "bai02_xet_duyet_vay",
    3: "bai03_suc_khoe",
    4: "bai04_gia_ve",
    5: "bai05_phi_atm",
    6: "bai06_danh_hieu",
    7: "bai07_rui_ro",
    8: "bai08_khen_thuong",
    9: "bai09_phi_giao_hang",
    10: "bai10_phi_gui_xe",
}


def doc_tham_so(args):
    chon = []
    for a in args:
        if a.startswith("-"):
            continue
        if "-" in a:
            x, y = a.split("-", 1)
            chon.extend(range(int(x), int(y) + 1))
        else:
            chon.append(int(a))
    chon = chon or sorted(MODULES)
    sai = [n for n in chon if n not in MODULES]
    if sai:
        raise SystemExit(f"Không có bài {sai}. Chỉ có bài 1..10.")
    return chon


def main(argv):
    gon = "-q" in argv
    ket_qua = []
    for n in doc_tham_so(argv):
        m = importlib.import_module(MODULES[n])
        ket_qua.append(common.chay_bai(m, gon=gon))
        print()

    print("=" * 78)
    print("TỔNG KẾT")
    print("=" * 78)
    print(f"{'Bài':<5}{'PASS':<10}{'Khớp bảng':<12}{'Phủ luật':<10}Kết luận")
    t_pass = t_tong = 0
    for k in ket_qua:
        t_pass += k["pass"]
        t_tong += k["tong"]
        print(f"{k['bai']:<5}{str(k['pass']) + '/' + str(k['tong']):<10}"
              f"{str(k['bang']) + '/' + str(k['tong']):<12}"
              f"{str(k['phu']) + '/' + str(k['so_luat']):<10}"
              f"{'OK' if common.ok_het(k) else '<-- CÓ LỖI'}")
    print(f"Tổng: {t_pass}/{t_tong} test PASS")
    return 0 if all(common.ok_het(k) for k in ket_qua) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
