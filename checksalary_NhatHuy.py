
def check_salary (hour:float, salary:float):
    if hour < 0.00 or salary <= 30.00 or hour > 60.00 or salary >= 200.00: 
        #sửa < 30.00 thành <= 30.00 và > 200.00 thành >= 200.00
        return "Invalid"

    if salary >= 30.00 and salary <= 200.00:
        if hour >= 0.00 and hour <= 20.00: # đổi giá trị 40.00 thành 20.00
            return "Lương bình thường"
        elif hour > 40.00 or hour <= 60.00: # đổi and thành or
            return "Lương tăng ca"
        else:
            return "Invalid"

