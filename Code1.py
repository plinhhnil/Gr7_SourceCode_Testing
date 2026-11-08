import string

def deliveryFee (price: float, distance: float, member: string):
    if price < 0.000 or distance < 0.00 or distance > 30.00 or member not in ['VIP', 'NORMAL']:
        # 1c1               1c2               1c3                  1c4
        return "Invalid"
        # 2

    if price >= 500000.000:
        # 3c1
        return "Freeship"
        # 4

    else:
        if member == 'VIP':
            # 5
            if distance <= 10.00:
                # 6
                return "10.000đ"
                # 7
            else:
                return "20.000đ"
                # 8
        
        else:
            if distance <= 10.00:
                # 9
                return "20.000đ"
                # 10
            else:
                return "30.000đ"
                # 11
            