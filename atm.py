def withdraw_money(withdraw, balance, atmCash):
    if withdraw < 0 and balance < 0 or not (0 < atmCash < 50000000):
        return "invalid"


    if withdraw > balance:
        return "Số dư không đủ"


    if withdraw > atmCash:
        return "Số tiền vượt mức trong ATM"


    if withdraw <=  1000000:
        return "Mức phí 1"
    elif withdraw < 10000000:
        return "Mức phí 3" 
    else:
        return "Mức phí 1" 
