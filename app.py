from flask import Flask, render_template, request, jsonify
from scheduler import recommend_site, SITES
import json

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html", sites=SITES)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    # expected keys: cores, hours, urgency (1-10), model_size (small/medium/large)
    try:
        cores = int(data.get("cores", 4))
        hours = float(data.get("hours", 1.0))
        urgency = int(data.get("urgency", 5))
        model_size = data.get("model_size", "medium")
    except Exception as e:
        return jsonify({"error":"invalid input", "details": str(e)}), 400

    job = {"cores": cores, "hours": hours, "urgency": urgency, "model_size": model_size}
    rec = recommend_site(job)
    return jsonify(rec)



import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render gives PORT automatically
    app.run(host="0.0.0.0", port=port, debug=True)
