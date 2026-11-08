# -*- coding: utf-8 -*-
"""
common.py - Bộ chạy test driver dùng chung cho 10 bài.

Mỗi file bàiXX_*.py khai báo:
    SO_BAI, TEN, DAC_TA          : thông tin đề
    DIEU_KIEN  = [(Cid, text, f)] : điều kiện C1..Cn, f(*input) -> bool
    HANH_DONG  = [(Aid, text)]    : hành động / đầu ra A1..Am
    LUAT       = {Rk: (pattern, Aid)}  pattern gồm T / F / - theo thứ tự điều kiện
    sut(*input)                   : hàm cần kiểm thử
    CASES = [(TestID, Rule, input, expected, ghi_chu)]

Driver làm 3 việc cho mỗi bài:
  1. In bảng quyết định.
  2. KIỂM TRA BẢNG: với từng test, tính giá trị các điều kiện rồi xem input
     khớp ĐÚNG MỘT luật và đúng luật đã khai báo (loại trừ nhau + phủ đủ).
  3. THỰC THI: gọi sut(*input), so với Expected -> PASS / FAIL.
"""
import sys

try:  # Windows PowerShell: ép UTF-8 để hiện đúng tiếng Việt
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ----------------------------------------------------------------- tiện ích
def _khop(pattern, vec):
    """Pattern (T/F/-) có khớp vector điều kiện không."""
    return all(p == "-" or (p == "T") == v for p, v in zip(pattern, vec))


def tinh_dieu_kien(m, inp):
    return [bool(f(*inp)) for _, _, f in m.DIEU_KIEN]


def luat_khop(m, vec):
    return [r for r, (pat, _) in m.LUAT.items() if _khop(pat, vec)]


def in_bang_quyet_dinh(m):
    luat = list(m.LUAT)
    nhan_c = [f"{c}: {t}" for c, t, _ in m.DIEU_KIEN]
    nhan_a = [f"{a}: {t}" for a, t in m.HANH_DONG]
    rong = max(len(s) for s in nhan_c + nhan_a)
    cot = max(len(r) for r in luat)
    print(" " * rong + " | " + " ".join(r.rjust(cot) for r in luat))
    print("-" * rong + "-+-" + "-" * ((cot + 1) * len(luat) - 1))
    for i, lab in enumerate(nhan_c):
        cells = [m.LUAT[r][0][i].rjust(cot) for r in luat]
        print(lab.ljust(rong) + " | " + " ".join(cells))
    print("-" * rong + "-+-" + "-" * ((cot + 1) * len(luat) - 1))
    for (a, _), lab in zip(m.HANH_DONG, nhan_a):
        cells = [("X" if m.LUAT[r][1] == a else " ").rjust(cot) for r in luat]
        print(lab.ljust(rong) + " | " + " ".join(cells))


# --------------------------------------------------------------- chạy 1 bài
def chay_bai(m, gon=False):
    """Chạy một bài. Trả về dict kết quả."""
    cases = m.CASES
    ten_c = {c: t for c, t, _ in m.DIEU_KIEN}
    print("=" * 78)
    print(f"BÀI {m.SO_BAI}: {m.TEN}")
    print("=" * 78)
    if not gon:
        print("ĐẶC TẢ:")
        for dong in m.DAC_TA.strip("\n").split("\n"):
            print("  " + dong)
        print("\nBẢNG QUYẾT ĐỊNH:")
        in_bang_quyet_dinh(m)
        print("\nCHI TIẾT TỪNG TEST (1 test = 1 luật):")
    else:
        print(f"{'ID':<5}{'Rule':<5}{'Bảng':<6}{'Kết quả':<8}Input -> Expected")

    n_pass = n_bang = 0
    da_phu = {}
    for tid, rule, inp, expected, ghi_chu in cases:
        vec = tinh_dieu_kien(m, inp)
        khop = luat_khop(m, vec)
        bang_ok = khop == [rule]
        n_bang += bang_ok
        da_phu.setdefault(rule, []).append(tid)

        try:
            actual, loi = m.sut(*inp), None
        except Exception as e:           # sut ném lỗi -> FAIL
            actual, loi = None, f"{type(e).__name__}: {e}"
        ok = loi is None and actual == expected
        n_pass += ok

        if gon:
            print(f"{tid:<5}{rule:<5}{'OK' if bang_ok else 'LỆCH':<6}"
                  f"{'PASS' if ok else 'FAIL':<8}{inp} -> {expected!r}"
                  + ("" if ok else f" | Actual: {loi or repr(actual)}"))
            continue

        dung = [cid for (cid, _, _), v in zip(m.DIEU_KIEN, vec) if v]
        print(f"\n[{tid}] Luật {rule}   Input = {inp}")
        print(f"   Ghi chú        : {ghi_chu}")
        print(f"   Điều kiện đúng : {', '.join(dung) if dung else '(không có)'}")
        if bang_ok:
            print(f"   Đối chiếu bảng : khớp đúng 1 luật = {rule}  [OK]")
        else:
            print(f"   Đối chiếu bảng : khớp {khop or 'không luật nào'}, "
                  f"cần {rule}  [LỆCH - test chưa đúng luật]")
        print(f"   Expected       : {expected!r}")
        print(f"   Actual         : {loi or repr(actual)}")
        print(f"   Kết quả        : {'PASS' if ok else 'FAIL'}")

    tong = len(cases)
    phu = [r for r in m.LUAT if len(da_phu.get(r, [])) == 1]
    print("\n" + "-" * 78)
    print(f"Bài {m.SO_BAI} | PASS {n_pass}/{tong} | "
          f"Khớp bảng {n_bang}/{tong} | "
          f"Luật có đúng 1 test {len(phu)}/{len(m.LUAT)}")
    return {"bai": m.SO_BAI, "pass": n_pass, "tong": tong,
            "bang": n_bang, "phu": len(phu), "so_luat": len(m.LUAT)}


def ok_het(kq):
    return (kq["pass"] == kq["tong"] and kq["bang"] == kq["tong"]
            and kq["phu"] == kq["so_luat"] and kq["tong"] == kq["so_luat"])


def main(m, argv):
    """Điểm vào cho từng file bài: python baiXX_*.py [-q]"""
    kq = chay_bai(m, gon="-q" in argv)
    return 0 if ok_het(kq) else 1
