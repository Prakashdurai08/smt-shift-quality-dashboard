from flask import Flask, jsonify, request
from flask_cors import CORS

from analysis import (load_data, filter_data, calculate_kpis,
                      pareto_data, yield_by_group)

app = Flask(__name__)
CORS(app)

df_all = load_data()   # loaded once when the server starts


def get_filtered():
    return filter_data(
        df_all,
        line=request.args.get("line"),
        shift=request.args.get("shift"),
        date=request.args.get("date"),
    )


@app.errorhandler(ValueError)
def bad_input(error):
    return jsonify({"error": "Invalid filter value"}), 400


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "rows": len(df_all)})


@app.route("/api/options")
def options():
    return jsonify({
        "lines": sorted(df_all["line"].unique().tolist()),
        "shifts": sorted(df_all["shift"].unique().tolist()),
        "dates": sorted(df_all["date"].dt.strftime("%Y-%m-%d").unique().tolist()),
    })


@app.route("/api/kpis")
def kpis():
    return jsonify(calculate_kpis(get_filtered()))


@app.route("/api/pareto")
def pareto():
    return jsonify(pareto_data(get_filtered()).to_dict(orient="records"))


@app.route("/api/yield-by-line")
def yield_line():
    return jsonify(yield_by_group(get_filtered(), "line").to_dict(orient="records"))


@app.route("/api/yield-by-shift")
def yield_shift():
    return jsonify(yield_by_group(get_filtered(), "shift").to_dict(orient="records"))


@app.route("/api/trend")
def trend():
    g = yield_by_group(get_filtered(), "date")
    if g.empty:
        return jsonify([])
    g["date"] = g["date"].dt.strftime("%Y-%m-%d")
    return jsonify(g.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)