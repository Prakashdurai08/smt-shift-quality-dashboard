import os
import matplotlib
matplotlib.use("Agg")   # draw to files, no pop-up window
import matplotlib.pyplot as plt

from analysis import load_data, pareto_data, yield_by_group, FPY_TARGET

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREY = "#b4b2a9"


def pareto_chart(df, path):
    p = pareto_data(df)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(p["defect_type"], p["count"], color=BLUE)
    ax.set_ylabel("Defect count")
    ax.set_title("Defect Pareto")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")

    ax2 = ax.twinx()
    ax2.plot(p["defect_type"], p["cumulative_pct"], color=ORANGE, marker="o")
    ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Cumulative %")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def defects_by_line_chart(df, path):
    g = yield_by_group(df, "line")
    worst = g["failed_boards"].max()
    colors = [BLUE if v == worst else GREY for v in g["failed_boards"]]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(g["line"], g["failed_boards"], color=colors)
    ax.bar_label(bars)
    ax.set_ylabel("Failed boards")
    ax.set_title("Defects by line")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fpy_trend_chart(df, path):
    g = yield_by_group(df, "date")
    labels = g["date"].dt.strftime("%d %b")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(labels, g["fpy"], color=BLUE, marker="o")
    ax.axhline(FPY_TARGET, color=ORANGE, linestyle="--", linewidth=1,
               label="Target " + str(FPY_TARGET) + "%")
    ax.set_ylabel("FPY %")
    ax.set_title("Daily first-pass yield")
    ax.legend()

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs("reports/charts", exist_ok=True)
    df = load_data()
    pareto_chart(df, "reports/charts/pareto.png")
    defects_by_line_chart(df, "reports/charts/defects_by_line.png")
    fpy_trend_chart(df, "reports/charts/fpy_trend.png")
    print("Charts saved in reports/charts/")