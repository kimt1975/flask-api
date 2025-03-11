import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# 🔹 Indlæs JSON-data med fejlhåndtering
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "sponsorship_data.json")
try:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        sponsorship_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Fejl ved indlæsning af JSON-fil: {e}")
    sponsorship_data = []

# 🔹 Forbedret logning
@app.before_request
def log_request_info():
    print(f"🔍 Forespørgsel modtaget: {request.method} {request.path}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query-parametre: {request.args}")

# 🔹 Endpoint til at hente unikke værdier fra kolonnen 'Brandværdier'
@app.route("/values", methods=["GET"])
def get_values():
    unique_values = set()
    
    # Gennemgå hver sponsor og tilføj værdier fra 'Brandværdier'
    for sponsor in sponsorship_data:
        brand_values = [v.strip() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        unique_values.update(brand_values)
    
    return jsonify(sorted(list(unique_values))), 200, {"Content-Type": "application/json; charset=utf-8"}

# 🔹 Hjælpefunktion til filtrering
def matches_filter(sponsor, filter_param, filter_value):
    if not filter_param or not filter_value:
        return True
    value = sponsor
    for level in filter_param.split("."):
        value = value.get(level, "")
        if not value:
            return False
    return filter_value.lower() in str(value).lower()

# 🔹 Hovedendpoint til at hente sponsor-data
@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    selected_values = request.args.getlist("brand_values")  # Hent værdier som liste
    filtered_sponsorships = []

    for sponsor in sponsorship_data:
        brand_values = [v.strip() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        
        # Tjek om nogle af de valgte værdier matcher
        if any(value in brand_values for value in selected_values):
            filtered_sponsorships.append({
                "Navn": sponsor.get("Navn"),
                "Tilskuere i snit": sponsor.get("Tilskuere i snit"),
                "Aldersgruppe": sponsor.get("Aldersgruppe"),
                "Brandværdier": sponsor.get("Brandværdier"),
                "Kommentarer": sponsor.get("Kommentarer")
            })

    return jsonify(filtered_sponsorships), 200, {"Content-Type": "application/json; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)