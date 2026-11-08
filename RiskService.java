public class RiskService {
    public static String evaluateRisk(int credit_score, int term) {
        // Cấy lỗi từ < 300 thành <= 300 và từ > 850 thành >= 850
        if (credit_score <= 300 || credit_score >= 850 || term < 6 || term > 60) {
            return "Invalid";
        }

        if (credit_score < 580) {
            return "High Risk";
        }

        // Cấy lỗi từ < 700 thành < 800
        if (credit_score < 800) {
            if (term <= 24) {
                return "Low Risk";
            } else {
                return "High Risk";
            }
        }

        return "Low Risk";
    }
}
