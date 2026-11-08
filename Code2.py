def homeCredit(income: float, credit: float, loan: str) -> str:
    if income < 0 or credit < 0 or loan not in ("TRUE", "FALSE"):
        # 1c1       1c2             1c3
        return "Invalid"
        # 2

    if credit < 200:
        # 3c1    
        if loan == "TRUE":
            # 4
            return "Từ chối khoản vay - hồ sơ xấu"
            # 5
        return "Từ chối khoản vay - điểm tín dụng thấp"
        # 6

    if loan == "TRUE":
        # 7
        return "Từ chối khoản vay - có nợ xấu"
        # 8

    if income >= 10:
        # 9
        return "Duyệt khoản vay"
        # 10
    return "Yêu cầu bổ sung hồ sơ"
    # 11