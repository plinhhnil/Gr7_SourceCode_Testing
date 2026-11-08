def check_ticket(age:int, slot:int):
    if age < 0 or age >= 100 or slot <= 1 or slot > 10: 
        #sửa < 1 thành <= 1 và > thành >= 100
        return "Invalid"

    if slot >= 1 and slot <= 10:
        if age >= 0 and age <= 11: # đổi giá trị 5 thành 11
            return "Không đủ tuổi xem phim"
        elif age > 11 and age <= 16: 
            return "Vé trẻ em"
        elif age > 16 or age <= 100: # đổi and thành or
            return "Vé người lớn"     