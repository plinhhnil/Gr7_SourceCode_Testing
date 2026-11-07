def classify_ticket(age, day):
    if age < 0 or age > 150 or day < 0 or day > 6:
        return "Invalid"
    if (age >= 0 and age < 18) or (age > 60 and age <= 150):
        if day >= 0 and day <= 4:
            return "Ve uu dai ngay thuong - 50000d"
        if day >= 5 and day <= 6:
            return "Ve uu dai cuoi tuan - 70000d"
    if age >= 18 and age <= 60:
        if day >= 0 and day <= 4:
            return "Ve tieu chuan ngay thuong - 80000d"
        if day >= 5 and day <= 6:
            return "Ve tieu chuan cuoi tuan - 100000d"
    return "Khong xac dinh"
