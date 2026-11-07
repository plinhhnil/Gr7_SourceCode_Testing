def classify_health(HR, SpO2):
    if HR < 40 or HR > 180 or SpO2 < 85 or SpO2 > 100:
        return "Invalid"
    if (40 <= HR < 50) or (120 < HR <= 180) or (85 <= SpO2 < 90):
        return "Nguy hiểm"
    if (50 <= HR < 60) or (100 < HR <= 120) or (90 <= SpO2 < 95):
        return "Cảnh báo"
    return "Bình thường"
