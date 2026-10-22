import csv
import random
from datetime import date, timedelta

random.seed(42)  # same data every run

LINE_FAIL_RATE = {"Line1": 0.018, "Line2": 0.024, "Line3": 0.032, "Line4": 0.016}
SHIFTS = ["A", "B", "C"]
DEFECTS = ["Insufficient solder", "Bridging", "Tombstone",
           "Missing component", "Misalignment"]
DEFECT_WEIGHTS = [42, 28, 17, 9, 4]
BOARDS_PER_SHIFT = 300
DAYS = 7
START_DATE = date(2026, 10, 8)

COLUMNS = ["date", "shift", "line", "board_id", "result",
           "defect_type", "paste_volume_pct", "reflow_peak_temp"]


def make_row(board_no, day, shift, line):
    failed = random.random() < LINE_FAIL_RATE[line]
    paste = random.gauss(100, 6)
    temp = random.gauss(245, 2.5)

    if failed:
        result = "FAIL"
        defect = random.choices(DEFECTS, weights=DEFECT_WEIGHTS)[0]
        if defect == "Insufficient solder":
            paste = random.gauss(72, 6)
        elif defect == "Bridging":
            paste = random.gauss(128, 7)
        elif defect == "Tombstone":
            temp = random.gauss(238, 3)
    else:
        result = "PASS"
        defect = "None"

    return [day.isoformat(), shift, line, "B" + str(board_no).zfill(6),
            result, defect, round(paste, 1), round(temp, 1)]


rows = []
board_no = 1
for d in range(DAYS):
    day = START_DATE + timedelta(days=d)
    for shift in SHIFTS:
        for line in LINE_FAIL_RATE:
            for _ in range(BOARDS_PER_SHIFT):
                rows.append(make_row(board_no, day, shift, line))
                board_no += 1

with open("data/inspection_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(COLUMNS)
    writer.writerows(rows)

fails = sum(1 for r in rows if r[4] == "FAIL")
print("Rows written:", len(rows))
print("Failed boards:", fails)
print("Overall FPY:", round((len(rows) - fails) / len(rows) * 100, 2), "%")