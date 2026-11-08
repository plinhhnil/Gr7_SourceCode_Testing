public class BonusService {
    public static String evaluateBonus(double kpi, int td, int thang) {
        if (kpi < 0.0 || kpi > 100.0 || td < 0 || td > 100 || thang < 1 || thang > 12) {
            return "Invalid";
        }

        if (thang < 6) {
            return "Khong";
        }

        if (kpi >= 90.0 && td >= 80) {
            return "Xuat sac";
        }

        // Cấy lỗi: dùng dấu || thay vì &&
        if (kpi >= 75.0 || td >= 80) {
            return "Tieu chuan";
        }

        return "Khong";
    }
}