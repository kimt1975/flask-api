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
    
    for sponsor in sponsorship_data:
        brand_values = [v.strip().lower() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        unique_values.update(brand_values)
    
    return jsonify(sorted(list(unique_values))), 200, {"Content-Type": "application/json; charset=utf-8"}

# 🔹 Hovedendpoint til at hente sponsor-data
@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    selected_values = [v.strip().lower() for v in request.args.getlist("brand_values")]
    category_map = {
    "1": "herrefodbold",
    "2": "kvindefodbold",
    "3": "herrehåndbold",
    "4": "kvindehåndbold",
    "5": "musik",
    "6": "festivaler"
}

selected_categories = [category_map.get(v.strip(), "").strip().lower() for v in request.args.getlist("categories") if category_map.get(v.strip())]

    print("👉 Valgte brandværdier:", selected_values)
    print("👉 Valgte kategorier:", selected_categories)
    print("👉 Data fra JSON-filen:")

    for sponsor in sponsorship_data:
        print(f"{sponsor['Navn']}: {sponsor['Brandværdier']} | {sponsor['Kategori']}")

    filtered_sponsorships = []
    for sponsor in sponsorship_data:
        brand_values = [v.strip().lower() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        category = sponsor.get("Kategori", "").strip().lower()

        # 🔥 Logning til fejlsøgning af kategorier
        print(f"👉 Kontrol: Kategori i JSON: '{category}', Valgte kategorier: {selected_categories}")

        # 🔥 Kun ét match kræves
        if any(value in brand_values for value in selected_values) and category in selected_categories:
            filtered_sponsorships.append({
                "Navn": sponsor.get("Navn"),
                "Tilskuere i snit": sponsor.get("Tilskuere i snit"),
                "Aldersgruppe": sponsor.get("Aldersgruppe"),
                "Brandværdier": sponsor.get("Brandværdier"),
                "Kommentarer": sponsor.get("Kommentarer"),
                "Aktiveringsmuligheder": sponsor.get("Aktiveringsmuligheder")
            })

    if not filtered_sponsorships:
        return jsonify({
            "Besked": "Ingen resultater fundet. Prøv at vælge andre værdier eller kategorier.",
            "Tips": "Overvej at vælge bredere værdier eller flere kategorier for bedre resultater."
        }), 404

    return jsonify(filtered_sponsorships), 200, {"Content-Type": "application/json; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
