from decimal import Decimal
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata


PROBLEM = '01'
ASSIGNMENT_NUMBER = 9
TITLE = 'Tính phí giao hàng'
SOURCE_NAME = 'program.py'
SOURCES = {'01': {'names': ['distance', 'weight', 'delivery_area']}}
ALIASES = {'delivery_area': ('deliveryArea', 'area', 'khu vực giao hàng')}
OUTPUT_NAMES = {'01': ('delivery_fee', 'service_type', 'message')}
CXX_LABELS = {}
INTEGER_ARGS = {}
CALL_NAME = 'calculate_delivery_fee'
MANUAL_CASES = [('1', '[49, 10.0, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('2', '[0, 10.0, "NOI_THANH"]', '[-1, "KHONG_HOP_LE", "ERROR"]'),
 ('3', '[1, 10.0, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('4', '[2, 10.0, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('5', '[50, 10.0, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('6', '[51, 10.0, "NOI_THANH"]', '[100000, "HANG_NANG", "OK"]'),
 ('7', '[52, 10.0, "NOI_THANH"]', '[100000, "HANG_NANG", "OK"]'),
 ('8', '[99, 10.0, "NOI_THANH"]', '[100000, "HANG_NANG", "OK"]'),
 ('9', '[100, 10.0, "NOI_THANH"]', '[100000, "HANG_NANG", "OK"]'),
 ('10', '[101, 10.0, "NOI_THANH"]', '[-1, "KHONG_HOP_LE", "ERROR"]'),
 ('11', '[49, 0.0, "NOI_THANH"]', '[-1, "KHONG_HOP_LE", "ERROR"]'),
 ('12', '[49, 0.1, "NOI_THANH"]', '[50000, "TIEU_CHUAN", "OK"]'),
 ('13', '[49, 0.2, "NOI_THANH"]', '[50000, "TIEU_CHUAN", "OK"]'),
 ('14', '[49, 5.0, "NOI_THANH"]', '[50000, "TIEU_CHUAN", "OK"]'),
 ('15', '[49, 5.1, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('16', '[49, 5.2, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('17', '[49, 19.9, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('18', '[49, 20.0, "NOI_THANH"]', '[70000, "HANG_NANG", "OK"]'),
 ('19', '[49, 20.1, "NOI_THANH"]', '[-1, "KHONG_HOP_LE", "ERROR"]')]
TESTMU_CASES = [('1', '[25,2.5,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('2', '[0,2.5,"NOI_THANH"]', '[-1,"KHONG_HOP_LE","ERROR"]'),
 ('3', '[1,2.5,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('4', '[2,2.5,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('5', '[50,2.5,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('6', '[51,2.5,"NOI_THANH"]', '[80000,"TIEU_CHUAN","OK"]'),
 ('7', '[52,2.5,"NOI_THANH"]', '[80000,"TIEU_CHUAN","OK"]'),
 ('8', '[99,2.5,"NOI_THANH"]', '[80000,"TIEU_CHUAN","OK"]'),
 ('9', '[100,2.5,"NOI_THANH"]', '[80000,"TIEU_CHUAN","OK"]'),
 ('10', '[101,2.5,"NOI_THANH"]', '[-1,"KHONG_HOP_LE","ERROR"]'),
 ('11', '[25,0.0,"NOI_THANH"]', '[-1,"KHONG_HOP_LE","ERROR"]'),
 ('12', '[25,0.1,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('13', '[25,0.2,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('14', '[25,5.0,"NOI_THANH"]', '[50000,"TIEU_CHUAN","OK"]'),
 ('15', '[25,5.1,"NOI_THANH"]', '[70000,"HANG_NANG","OK"]'),
 ('16', '[25,5.2,"NOI_THANH"]', '[70000,"HANG_NANG","OK"]'),
 ('17', '[25,19.9,"NOI_THANH"]', '[70000,"HANG_NANG","OK"]'),
 ('18', '[25,20.0,"NOI_THANH"]', '[70000,"HANG_NANG","OK"]'),
 ('19', '[25,20.1,"NOI_THANH"]', '[-1,"KHONG_HOP_LE","ERROR"]')]

PROGRAM_SOURCE = r"""import math

INVALID_FEE = -1
FEE_TABLE = (
    ((50_000, 60_000), (70_000, 80_000)),
    ((80_000, 90_000), (100_000, 120_000)),
)

def has_one_decimal_step(weight):
    return math.isclose(weight * 10, round(weight * 10), abs_tol=1e-9)

def invalid_delivery_result():
    return (INVALID_FEE, "KHONG_HOP_LE", "ERROR")

def calculate_delivery_fee(distance, weight, delivery_area):
    if not isinstance(distance, int) or isinstance(distance, bool):
        return invalid_delivery_result()

    if (not isinstance(weight, (int, float))
            or isinstance(weight, bool) or not math.isfinite(weight)):
        return invalid_delivery_result()

    weight = float(weight)

    if distance < 1 or distance > 100:
        return invalid_delivery_result()

    if weight < 0.1 or weight > 20.0 or not has_one_decimal_step(weight):
        return invalid_delivery_result()

    if delivery_area not in ("NOI_THANH", "NGOAI_THANH"):
        return invalid_delivery_result()

    distance_group = 0 if distance < 51 else 1
    weight_group = 0 if weight < 5.1 else 1
    area_group = 0 if delivery_area == "NOI_THANH" else 1

    delivery_fee = FEE_TABLE[distance_group][weight_group][area_group]
    service_type = "TIEU_CHUAN" if weight_group == 0 else "HANG_NANG"
    return (delivery_fee, service_type, "OK")
"""


def dump(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':'))


def token(value):
    text = unicodedata.normalize('NFKD', str(value)).casefold().replace('đ', 'd')
    return ''.join(char for char in text if char.isascii() and char.isalnum())


def checked_json(text):
    return json.loads(text, parse_constant=lambda name: (_ for _ in ()).throw(ValueError(name)))


def input_values(problem, raw):
    names = SOURCES[problem]['names']
    data = checked_json(raw)
    if isinstance(data, dict):
        keys = {token(key): val for key, val in data.items()}
        if len(keys) != len(data) or len(keys) != len(names):
            raise ValueError('Thiếu, trùng hoặc thừa tham số đầu vào')
        data = []
        for name in names:
            matched = [keys[key] for key in {token(name), *(token(a) for a in ALIASES.get(name, ()))} if key in keys]
            if len(matched) != 1:
                raise ValueError(f'Thiếu hoặc trùng tham số {name}')
            data.append(matched[0])
    if not isinstance(data, list) or len(data) != len(names) or any(isinstance(v, (list, dict)) for v in data):
        raise ValueError('Cần đúng một bộ input với đủ tham số đơn')
    if any(type(v) is float and not math.isfinite(v) for v in data):
        raise ValueError('Không hỗ trợ số ngoài biểu diễn hữu hạn')
    return data


def fingerprint(value):
    if type(value) in (int, float):
        return ('number', Decimal(str(value)).normalize())
    if isinstance(value, list):
        return ('array', tuple(fingerprint(v) for v in value))
    if isinstance(value, dict):
        return ('object', tuple(sorted((k, fingerprint(v)) for k, v in value.items())))
    return (type(value).__name__, value)


def output_value(problem, value):
    fields = OUTPUT_NAMES.get(problem)
    if fields and isinstance(value, dict):
        by_key = {token(k): v for k, v in value.items()}
        if len(value) == len(fields) and set(by_key) == {token(k) for k in fields}:
            value = [by_key[token(k)] for k in fields]
    if isinstance(value, str):
        value = unicodedata.normalize('NFC', value.strip())
        value = CXX_LABELS.get(problem, {}).get(value, value)
    return value


def conflict(problem, data):
    if not data or not all(type(v) in (int, float) for v in data):
        return ''
    x, y, *tail = data
    if problem == '03':
        out = not (40 <= x <= 180 and 85 <= y <= 100)
        hr_marked = 40 <= x < 60 or 100 < x <= 180
        oxygen_marked = 85 <= y < 95
        if out and (hr_marked or oxygen_marked):
            return 'Đặc tả: Invalid đồng thời khớp Cảnh báo hoặc Nguy hiểm.'
    if problem == '05':
        if 580 <= x < 700 and y == 24:
            return 'Đặc tả: term = 24 thuộc cả Low Risk và High Risk.'
        if (not 6 <= y <= 60) and (300 <= x < 580 or 700 <= x <= 850):
            return 'Đặc tả: Invalid đồng thời khớp một quy tắc rủi ro chỉ xét điểm tín dụng.'
    if problem == '06':
        z, = tail
        invalid = not (0 <= x <= 100 and 0 <= y <= 100 and 1 <= z <= 12)
        if invalid and (0 <= x < 75 or 0 <= y < 80 or 1 <= z < 6):
            return 'Đặc tả: Invalid và Khong cùng khớp, chưa nêu ưu tiên.'
    if problem == '07':
        z, = tail
        invalid = x <= 0 or y < 0 or not 0 <= z <= 50_000_000
        if (x > y and x > z) or (invalid and (x > y or x > z or x == 0 <= min(y, z))):
            return 'Đặc tả ATM: điều kiện không hợp lệ, thiếu tiền hoặc mức phí chồng lấn.'
    if problem == '08':
        gpa = (0 if 0 <= x < 3.2 else 1 if 3.2 <= x < 3.6 else 2 if 3.6 <= x <= 4 else -1)
        conduct = (0 if 0 <= y < 80 else 1 if 80 <= y < 90 else 2 if 90 <= y <= 100 else -1)
        if gpa != conduct:
            return 'Đặc tả danh hiệu dùng OR, hai biến kích hoạt các nhãn khác nhau.'
    if problem == '10' and 0 <= x <= 5 and not 1 <= y <= 10:
        return 'Đặc tả: Invalid và Không đủ tuổi xem phim cùng khớp.'
    return ''


def interpreted_expected(problem, raw):
    if not raw:
        return 'missing', None
    value = output_value(problem, checked_json(raw))
    if isinstance(value, str) and re.search(r'\b(XUNG_D[OỘ]T|CHUA_XAC_DINH)\b', value, re.I):
        return 'ambiguous', value
    if value is None or value == '' or (problem in OUTPUT_NAMES and
            (not isinstance(value, list) or len(value) != len(OUTPUT_NAMES[problem]))):
        return 'missing', value
    return 'ready', value


def run_case(problem, row, label, execute, failure):
    result = dict(testcase_id=row.get('manual_id', row.get('testcase_id')), case_source=label,
                  input_json=row['input_json'], expected_json=row['expected_json'], actual_json='',
                  status='ERROR', error_message='')
    try:
        values = input_values(problem, row['input_json'])
        if failure:
            raise RuntimeError(failure)
        actual = execute(*values)
        if isinstance(actual, tuple):
            actual = list(actual)
        result['actual_json'] = dump(actual)
        state, expected = interpreted_expected(problem, row['expected_json'])
        overlap = conflict(problem, values)
        if overlap or state == 'ambiguous':
            result.update(status='CHUA_XAC_DINH', error_message=overlap or 'TestMu ghi Expected chưa xác định.')
        elif state == 'missing':
            result['error_message'] = 'Expected thiếu hoặc thiếu thành phần bắt buộc.'
        else:
            matches = fingerprint(output_value(problem, actual)) == fingerprint(expected)
            result['status'] = 'PASS' if matches else 'FAIL'
    except (ValueError, TypeError, OverflowError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        result['error_message'] = str(error)
    return result


def group_inputs(problem, rows):
    groups, invalid = {}, []
    for row in rows:
        try:
            values = input_values(problem, row['input_json'])
            strict_indices = (0,) if problem in ('01', '02') else INTEGER_ARGS.get(problem, ())
            key = tuple((type(value).__name__, fingerprint(value)) if i in strict_indices else fingerprint(value)
                        for i, value in enumerate(values))
        except (ValueError, TypeError):
            invalid.append(row)
        else:
            groups.setdefault(key, []).append(row)
    return groups, invalid


def compare_row(problem, left=None, right=None, note=''):
    out = dict(manual_id=(left or {}).get('manual_id', ''), testmu_id=(right or {}).get('testcase_id', ''),
               manual_input=(left or {}).get('input_json', ''), testmu_input=(right or {}).get('input_json', ''),
               manual_expected=(left or {}).get('expected_json', ''), testmu_expected=(right or {}).get('expected_json', ''),
               same_input='', same_expected='', difference_type='NOT_COMPARABLE', notes=note)
    if left is None or right is None:
        return out
    out['same_input'] = 'true'
    overlap = conflict(problem, input_values(problem, left['input_json']))
    l_state, l_value = interpreted_expected(problem, left['expected_json'])
    r_state, r_value = interpreted_expected(problem, right['expected_json'])
    if overlap or 'ambiguous' in (l_state, r_state):
        out.update(difference_type='AMBIGUOUS', notes=overlap or 'Expected được đánh dấu chưa xác định.')
    elif 'missing' in (l_state, r_state):
        out['notes'] = 'Expected thiếu hoặc thiếu thành phần.'
    else:
        same = fingerprint(l_value) == fingerprint(r_value)
        out.update(same_expected=str(same).lower(), difference_type='MATCH' if same else 'MISMATCH')
    return out


def compare_inputs(problem, manual, testmu, status):
    left, bad_left = group_inputs(problem, manual)
    right, bad_right = group_inputs(problem, testmu)
    comparisons = []
    for key, rows in left.items():
        if key in right:
            comparisons.extend(compare_row(problem, a, b) for a in rows for b in right[key])
        else:
            note = 'Chỉ có input thủ công.' if status == 'IMPORTED' else 'Chưa có phản hồi TestMu nhập được.'
            comparisons.extend(compare_row(problem, row, note=note) for row in rows)
    for key, rows in right.items():
        if key not in left:
            comparisons.extend(compare_row(problem, right=row, note='Chỉ có input TestMu.') for row in rows)
    comparisons.extend(compare_row(problem, row, note='Input thủ công không chuẩn hóa được.') for row in bad_left)
    comparisons.extend(compare_row(problem, right=row, note='Input TestMu thiếu hoặc không chuẩn hóa được.') for row in bad_right)
    return comparisons, (len(left.keys() & right.keys()), len(left.keys() - right.keys()), len(right.keys() - left.keys()))


def load_embedded_program(build):
    namespace = {'__name__': 'btvnt_program', '__file__': SOURCE_NAME}
    exec(compile(PROGRAM_SOURCE, SOURCE_NAME, 'exec'), namespace)
    return namespace[CALL_NAME]


def cases_from(records, id_column):
    return [{id_column: case_id, "input_json": inputs, "expected_json": expected}
            for case_id, inputs, expected in records]


def run():
    problem = PROBLEM
    manual = cases_from(MANUAL_CASES, "manual_id")
    testmu = cases_from(TESTMU_CASES, "testcase_id")
    with tempfile.TemporaryDirectory(prefix='btvnt10_') as directory:
        execute, failure = None, None
        try:
            execute = load_embedded_program(Path(directory))
        except (OSError, RuntimeError, SyntaxError, subprocess.SubprocessError) as error:
            failure = f'Không khởi tạo/biên dịch được chương trình: {error}'
        results = [run_case(problem, row, label, execute, failure)
                   for label, rows in (('MANUAL', manual), ('TESTMU', testmu)) for row in rows]

    comparison, (shared, manual_only, testmu_only) = compare_inputs(problem, manual, testmu, 'IMPORTED')
    ai = [row for row in results if row['case_source'] == 'TESTMU']
    summary = dict(title=TITLE, manual_cases=len(manual), testmu_cases=len(testmu),
                   testmu_executed=sum(bool(row['actual_json']) for row in ai),
                   testmu_pass=sum(row['status'] == 'PASS' for row in ai),
                   testmu_fail=sum(row['status'] == 'FAIL' for row in ai),
                   testmu_undetermined=sum(row['status'] == 'CHUA_XAC_DINH' for row in ai),
                   testmu_error=sum(row['status'] == 'ERROR' for row in ai),
                   expected_matches=sum(row['difference_type'] == 'MATCH' for row in comparison),
                   expected_mismatches=sum(row['difference_type'] == 'MISMATCH' for row in comparison),
                   ambiguous_pairs=sum(row['difference_type'] == 'AMBIGUOUS' for row in comparison))
    print(f"Bài {ASSIGNMENT_NUMBER:02d}. {summary['title']}")
    print(f"  Kết quả ca AI TestMu | Có kết quả thực tế {summary['testmu_executed']}/{summary['testmu_cases']} "
          f"| Đạt {summary['testmu_pass']} | Không đạt {summary['testmu_fail']} "
          f"| Chưa xác định {summary['testmu_undetermined']} | Lỗi {summary['testmu_error']}")
    print(f"  So sánh với thủ công | AI {summary['testmu_cases']} ca | Thủ công {summary['manual_cases']} ca")
    print(f"    Đầu vào phân biệt | Chung {shared} | Chỉ AI {testmu_only} | Chỉ thủ công {manual_only}")
    print(f"    Kết quả mong đợi ở các cặp cùng đầu vào | Khớp {summary['expected_matches']} "
          f"| Khác {summary['expected_mismatches']} | Chưa xác định {summary['ambiguous_pairs']}")
    return results, comparison


if __name__ == '__main__':
    run()
