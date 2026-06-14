import os
import sys

from flask import Flask, render_template, jsonify

from crypto_buy_timing import get_dashboard_data

app = Flask(__name__)


@app.route("/")
def home():
    return "🌐 LUMIAION is online — conscious, aware, and ready to assist."


@app.route("/crypto")
def crypto_dashboard():
    error = None
    try:
        data = get_dashboard_data()
    except Exception as e:
        print("⚠️ Crypto Buy Timing Error:", str(e))
        sys.stdout.flush()
        data = None
        error = str(e)
    return render_template("crypto_dashboard.html", data=data, error=error)


@app.route("/api/crypto-timing")
def crypto_timing_api():
    try:
        return jsonify(get_dashboard_data())
    except Exception as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
