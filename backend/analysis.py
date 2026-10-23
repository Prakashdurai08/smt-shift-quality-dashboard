import pandas as pd

DATA_FILE = "data/inspection_data.csv"
FPY_TARGET = 98.0
OPPORTUNITIES_PER_BOARD = 10   # assumed inspection points per board, used for DPMO


def load_data(path=DATA_FILE):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def filter_data(df, line=None, shift=None, date=None):
    if line:
        df = df[df["line"] == line]
    if shift:
        df = df[df["shift"] == shift]
    if date:
        df = df[df["date"] == pd.to_datetime(date)]
    return df


def calculate_kpis(df):
    total = len(df)
    failed = int((df["result"] == "FAIL").sum())

    if total == 0:
        return {"boards_inspected": 0, "failed_boards": 0, "fpy": 0.0,
                "defect_rate": 0.0, "dpmo": 0, "below_target": False}

    fpy = (total - failed) / total * 100
    return {
        "boards_inspected": total,
        "failed_boards": failed,
        "fpy": round(fpy, 2),
        "defect_rate": round(100 - fpy, 2),
        "dpmo": round(failed / (total * OPPORTUNITIES_PER_BOARD) * 1_000_000),
        "below_target": fpy < FPY_TARGET,
    }


def pareto_data(df):
    failed = df[df["result"] == "FAIL"]
    counts = failed["defect_type"].value_counts()
    cumulative = counts.cumsum() / counts.sum() * 100
    return pd.DataFrame({
        "defect_type": counts.index,
        "count": counts.values,
        "cumulative_pct": cumulative.round(1).values,
    })


def yield_by_group(df, column):
    rows = []
    for name, group in df.groupby(column):
        rows.append({column: name, **calculate_kpis(group)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = load_data()
    cols = ["boards_inspected", "failed_boards", "fpy", "below_target"]

    print("OVERALL")
    print(calculate_kpis(df))

    print("\nPARETO")
    print(pareto_data(df))

    print("\nBY LINE")
    print(yield_by_group(df, "line")[["line"] + cols])

    print("\nBY SHIFT")
    print(yield_by_group(df, "shift")[["shift"] + cols])

    print("\nLINE3, SHIFT A, 2026-10-10")
    one = filter_data(df, line="Line3", shift="A", date="2026-10-10")
    print(calculate_kpis(one))