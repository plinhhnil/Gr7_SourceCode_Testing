INVALID_FEE = -1
FEE_TABLE = (
    ((10_000, 15_000), (40_000, 55_000)),
    ((20_000, 30_000), (80_000, 100_000)),
)

def invalid_parking_result():
    return (INVALID_FEE, "KHONG_HOP_LE")

def calculate_parking_fee(hours, vehicle_type, parking_area):
    # 1. Kiểm tra đầu vào.
    if not isinstance(hours, int) or isinstance(hours, bool):
        return invalid_parking_result()

    if hours < 1 or hours > 24:
        return invalid_parking_result()

    if vehicle_type not in ("XE_MAY", "OTO"):
        return invalid_parking_result()

    if parking_area not in ("NGOAI_TROI", "CO_MAI"):
        return invalid_parking_result()

    # 2. Xác định nhóm và tra bảng phí.
    hour_group = 0 if hours < 9 else 1
    vehicle_group = 0 if vehicle_type == "XE_MAY" else 1
    area_group = 0 if parking_area == "NGOAI_TROI" else 1

    parking_fee = FEE_TABLE[hour_group][vehicle_group][area_group]
    parking_type = "NGAN_HAN" if hours < 9 else "DAI_HAN"
    return (parking_fee, parking_type)
