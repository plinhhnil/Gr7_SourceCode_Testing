from decimal import Decimal
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata


PROBLEM = '03'
ASSIGNMENT_NUMBER = 3
TITLE = 'Phân loại sức khỏe theo HR và SpO2'
SOURCE_NAME = 'main.cpp'
SOURCES = {'03': {'names': ['HR', 'SpO2']}}
ALIASES = {'HR': ('nhịp tim', 'heart rate'), 'SpO2': ('SpO₂',)}
OUTPUT_NAMES = {}
CXX_LABELS = {'03': {'Nguy hiem': 'Nguy hiểm', 'Canh bao': 'Cảnh báo', 'Binh thuong': 'Bình thường'}}
INTEGER_ARGS = {'03': (0, 1)}
MANUAL_CASES = [('1', '[80, 98]', '"Bình thường"'),
 ('2', '[39, 98]', '"Invalid"'),
 ('3', '[40, 98]', '"Nguy hiểm"'),
 ('4', '[41, 98]', '"Nguy hiểm"'),
 ('5', '[49, 98]', '"Nguy hiểm"'),
 ('6', '[50, 98]', '"Cảnh báo"'),
 ('7', '[51, 98]', '"Cảnh báo"'),
 ('8', '[59, 98]', '"Cảnh báo"'),
 ('9', '[60, 98]', '"Bình thường"'),
 ('10', '[61, 98]', '"Bình thường"'),
 ('11', '[99, 98]', '"Bình thường"'),
 ('12', '[100, 98]', '"Bình thường"'),
 ('13', '[101, 98]', '"Cảnh báo"'),
 ('14', '[119, 98]', '"Cảnh báo"'),
 ('15', '[120, 98]', '"Cảnh báo"'),
 ('16', '[121, 98]', '"Nguy hiểm"'),
 ('17', '[179, 98]', '"Nguy hiểm"'),
 ('18', '[180, 98]', '"Nguy hiểm"'),
 ('19', '[181, 98]', '"Invalid"'),
 ('20', '[80, 84]', '"Invalid"'),
 ('21', '[80, 85]', '"Nguy hiểm"'),
 ('22', '[80, 86]', '"Nguy hiểm"'),
 ('23', '[80, 89]', '"Nguy hiểm"'),
 ('24', '[80, 90]', '"Cảnh báo"'),
 ('25', '[80, 91]', '"Cảnh báo"'),
 ('26', '[80, 94]', '"Cảnh báo"'),
 ('27', '[80, 95]', '"Bình thường"'),
 ('28', '[80, 96]', '"Bình thường"'),
 ('29', '[80, 99]', '"Bình thường"'),
 ('30', '[80, 100]', '"Bình thường"'),
 ('31', '[80, 101]', '"Invalid"')]
TESTMU_CASES = [('TC01', '[80,97]', '"Bình thường"'),
 ('TC02', '[80,84]', '"Invalid"'),
 ('TC03', '[80,85]', '"Nguy hiểm"'),
 ('TC04', '[80,86]', '"Nguy hiểm"'),
 ('TC05', '[80,89]', '"Nguy hiểm"'),
 ('TC06', '[80,90]', '"Cảnh báo"'),
 ('TC07', '[80,91]', '"Cảnh báo"'),
 ('TC08', '[80,94]', '"Cảnh báo"'),
 ('TC09', '[80,95]', '"Bình thường"'),
 ('TC10', '[80,96]', '"Bình thường"'),
 ('TC11', '[80,99]', '"Bình thường"'),
 ('TC12', '[80,100]', '"Bình thường"'),
 ('TC13', '[80,101]', '"Invalid"'),
 ('TC14', '[39,97]', '"Invalid"'),
 ('TC15', '[40,97]', '"Nguy hiểm"'),
 ('TC16', '[41,97]', '"Nguy hiểm"'),
 ('TC17', '[49,97]', '"Nguy hiểm"'),
 ('TC18', '[50,97]', '"Cảnh báo"'),
 ('TC19', '[51,97]', '"Cảnh báo"'),
 ('TC20', '[59,97]', '"Cảnh báo"'),
 ('TC21', '[60,97]', '"Bình thường"'),
 ('TC22', '[61,97]', '"Bình thường"'),
 ('TC23', '[99,97]', '"Bình thường"'),
 ('TC24', '[100,97]', '"Bình thường"'),
 ('TC25', '[101,97]', '"Cảnh báo"'),
 ('TC26', '[119,97]', '"Cảnh báo"'),
 ('TC27', '[120,97]', '"Cảnh báo"'),
 ('TC28', '[121,97]', '"Nguy hiểm"'),
 ('TC29', '[179,97]', '"Nguy hiểm"'),
 ('TC30', '[180,97]', '"Nguy hiểm"'),
 ('TC31', '[181,97]', '"Invalid"')]

PROGRAM_SOURCE = r"""#include <iostream>
#include <string>
using namespace std;
string classifyHealth(int HR, int SpO2) {
    if (HR < 40 || HR > 180 || SpO2 < 85 || SpO2 > 100) return "Invalid";
    if ((HR >= 40 && HR < 50) || (HR > 120 && HR <= 180) ||
        (SpO2 >= 85 && SpO2 < 90)) return "Nguy hiem";
    if ((HR >= 50 && HR < 60) || (HR > 100 && HR <= 120) ||
        (SpO2 >= 90 && SpO2 < 95)) return "Canh bao";
    if (HR >= 60 && HR <= 100 && SpO2 >= 95 && SpO2 <= 100)
        return "Binh thuong";
    return "Invalid";
}
int main(int argc, char* argv[]) {
    int HR, SpO2;
    if (argc == 3) { HR = stoi(argv[1]); SpO2 = stoi(argv[2]); }
    else { cin >> HR >> SpO2; }
    cout << classifyHealth(HR, SpO2) << endl;
}
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


def check_command(args):
    job = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace',
                         check=False, timeout=45)
    if job.returncode:
        raise RuntimeError(f'Mã thoát {job.returncode}: {job.stderr.strip() or job.stdout.strip()}')
    return job.stdout.rstrip('\r\n')


def load_embedded_program(build):
    source = build / SOURCE_NAME
    source.write_text(PROGRAM_SOURCE, encoding='utf-8')
    executable = build / 'program.exe'
    check_command(['g++', '-std=c++17', str(source), '-o', str(executable)])
    command = [str(executable)]

    def execute(*values):
        if any(type(values[index]) is not int for index in INTEGER_ARGS[PROBLEM]):
            raise ValueError('Tham số kiểu int không biểu diễn được qua giao diện chương trình')
        if any(type(value) not in (int, float) for value in values):
            raise ValueError('Giao diện chương trình yêu cầu tham số số')
        return check_command(command + [str(value) for value in values])

    return execute


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
