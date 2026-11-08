def assert_cases(test_case, target, cases):
    test_name = test_case.id()
    print(test_name, flush=True)
    for case_id, inputs, expected in cases:
        with test_case.subTest(case=case_id):
            actual = target(*inputs)
            try:
                test_case.assertEqual(actual, expected)
            except AssertionError:
                print(
                    f"  FAIL {case_id}: input={inputs}, "
                    f"expected={expected!r}, actual={actual!r}",
                    flush=True,
                )
                raise
            print(
                f"  PASS {case_id}: {inputs} -> {actual!r}",
                flush=True,
            )
