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

# 🔹 Liste over brandværdier og kategorier som brugeren kan vælge via tal
BRAND_VALUES = [
    "Ambitiøs", "Innovativ", "Familievenlig", "Historisk", "Lokal",
    "Energisk", "Passioneret", "Professionel", "Rå", "Skæv", "Soulful"
]

CATEGORIES = [
    "Herrefodbold", "Kvindefodbold", "Herrehåndbold",
    "Kvindehåndbold", "Musik", "Festivaler"
]

# 🔹 Endpoint til at hente unikke værdier fra kolonnen 'Brandværdier'
@app.route("/values", methods=["GET"])
def get_values():
    return jsonify(BRAND_VALUES), 200, {"Content-Type": "application/json; charset=utf-8"}

# 🔹 Endpoint til at hente unikke kategorier
@app.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(CATEGORIES), 200, {"Content-Type": "application/json; charset=utf-8"}

# 🔹 Hovedendpoint til at hente sponsor-data
@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    selected_values = [BRAND_VALUES[int(v) - 1] for v in request.args.getlist("brand_values") if v.isdigit()]
    selected_categories = [CATEGORIES[int(c) - 1] for c in request.args.getlist("categories") if c.isdigit()]

    if not selected_values:
        return jsonify({"Fejl": "Vælg venligst 3-5 brandværdier."}), 400
    if not selected_categories:
        return jsonify({"Fejl": "Vælg venligst 1-3 kategorier."}), 400

    filtered_sponsorships = []
    for sponsor in sponsorship_data:
        brand_values = [v.strip() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        category = sponsor.get("Kategori")

        # Nyt: Kun ét match kræves
        if any(value in brand_values for value in selected_values) and category in selected_categories:
            filtered_sponsorships.append({
                "Navn": sponsor.get("Navn"),
                "Tilskuere i snit": sponsor.get("Tilskuere i snit"),
                "Aldersgruppe": sponsor.get("Aldersgruppe"),
                "Brandværdier": sponsor.get("Brandværdier"),
                "Kommentarer": sponsor.get("Kommentarer")
            })

    if not filtered_sponsorships:
        return jsonify({
            "Besked": "Ingen resultater fundet. Prøv at vælge andre værdier eller kategorier.",
            "Tips": "Overvej at vælge bredere værdier eller flere kategorier for bedre resultater."
        }), 404

    return jsonify(filtered_sponsorships), 200, {"Content-Type": "application/json; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
