public class RiskServiceTest {
    private static int passed;
    private static int failed;

    private static void check(String id, int creditScore, int term, String expected) {
        String actual = RiskService.evaluateRisk(creditScore, term);
        if (expected.equals(actual)) {
            passed++;
            System.out.printf("  PASS %s: (%d, %d) -> %s%n",
                    id, creditScore, term, actual);
        } else {
            failed++;
            System.out.printf("  FAIL %s: (%d, %d), expected=%s, actual=%s%n",
                    id, creditScore, term, expected, actual);
        }
    }

    public static void main(String[] args) {
        check("TC1", 250, 12, "Invalid");
        check("TC2", 500, 12, "High Risk");
        check("TC3", 820, 12, "Low Risk");
        check("TC4", 650, 12, "Low Risk");
        check("TC5", 650, 36, "High Risk");
        System.out.printf("RiskService: %d passed, %d failed%n", passed, failed);
        if (failed > 0) {
            System.exit(1);
        }
    }
}
