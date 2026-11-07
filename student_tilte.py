
def xet_danh_hieu_sinh_vien(dht, drl, so_tin_chi, so_mon_duoi_C):
    # Local 1: Số tín chỉ đủ điều kiện xét
    tin_chi_thieu = max(0, 15 - so_tin_chi)

    # Local 2: Số môn dưới C tối đa
    so_mon_duoi_C_toi_da = 1

    # Local 3: Kết quả danh hiệu
    danh_hieu = ""

    if (not 0 <= dht <= 4.0
        or not 0 <= drl <= 100
        or not 0 <= so_tin_chi <= 26
        or not isinstance(so_mon_duoi_C, int)
        or so_mon_duoi_C < 0):
        danh_hieu = "Invalid input"

    elif tin_chi_thieu > 0:
        danh_hieu = "Không đạt danh hiệu"

    elif so_mon_duoi_C > so_mon_duoi_C_toi_da:
        danh_hieu = "Không đạt danh hiệu"

    elif dht < 3.2 or drl < 80:
        danh_hieu = "Không đạt danh hiệu"

    elif dht >= 3.6 and drl >= 90 and so_mon_duoi_C == 0:
        danh_hieu = "Sinh viên xuất sắc"

    else:
        danh_hieu = "Sinh viên giỏi"

    return danh_hieu
