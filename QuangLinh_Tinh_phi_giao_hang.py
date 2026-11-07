import math

INVALID_FEE = -1
FEE_TABLE = (
    ((50_000, 60_000), (70_000, 80_000)),
    ((80_000, 90_000), (100_000, 120_000)),
)

def has_one_decimal_step(weight):
    # Kiểm tra khối lượng theo bước 0,1 kg.
    return math.isclose(weight * 10, round(weight * 10), abs_tol=1e-9)

def invalid_delivery_result():
    return (INVALID_FEE, "KHONG_HOP_LE", "ERROR")

def calculate_delivery_fee(distance, weight, delivery_area):
    # 1. Kiểm tra đầu vào.
    if not isinstance(distance, int) or isinstance(distance, bool):
        return invalid_delivery_result()

    if (not isinstance(weight, (int, float))
            or isinstance(weight, bool) or not math.isfinite(weight)):
        return invalid_delivery_result()

    weight = float(weight)

    if distance < 1 or distance > 100:
        return invalid_delivery_result()

    if weight < 0.1 or weight > 20.0 or not has_one_decimal_step(weight):
        return invalid_delivery_result()

    if delivery_area not in ("NOI_THANH", "NGOAI_THANH"):
        return invalid_delivery_result()

    # 2. Xác định nhóm và tra bảng phí.
    distance_group = 0 if distance < 51 else 1
    weight_group = 0 if weight < 5.1 else 1
    area_group = 0 if delivery_area == "NOI_THANH" else 1

    delivery_fee = FEE_TABLE[distance_group][weight_group][area_group]
    service_type = "TIEU_CHUAN" if weight_group == 0 else "HANG_NANG"
    return (delivery_fee, service_type, "OK")
