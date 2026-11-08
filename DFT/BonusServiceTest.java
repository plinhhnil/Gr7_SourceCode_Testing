public class BonusServiceTest {
    private static int passed;
    private static int failed;

    private static void check(
            String id, double kpi, int td, int month, String expected) {
        String actual = BonusService.evaluateBonus(kpi, td, month);
        if (expected.equals(actual)) {
            passed++;
            System.out.printf("  PASS %s: (%.1f, %d, %d) -> %s%n",
                    id, kpi, td, month, actual);
        } else {
            failed++;
            System.out.printf("  FAIL %s: (%.1f, %d, %d), expected=%s, actual=%s%n",
                    id, kpi, td, month, expected, actual);
        }
    }

    public static void main(String[] args) {
        check("TC1", 105.0, 50, 8, "Invalid");
        check("TC2", 80.0, 85, 3, "Khong");
        check("TC3", 95.0, 90, 8, "Xuat sac");
        check("TC4", 80.0, 85, 8, "Tieu chuan");
        check("TC5", 50.0, 50, 8, "Khong");
        System.out.printf("BonusService: %d passed, %d failed%n", passed, failed);
        if (failed > 0) {
            System.exit(1);
        }
    }
}
