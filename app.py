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
        brand_values = [v.strip() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        unique_values.update(brand_values)
    
    return jsonify(sorted(list(unique_values))), 200, {"Content-Type": "application/json; charset=utf-8"}

# 🔹 Hjælpefunktion til at konvertere tal til værdier
def convert_numbers_to_values(selected_numbers, value_list):
    try:
        selected_values = [value_list[int(num) - 1] for num in selected_numbers if num.isdigit() and 1 <= int(num) <= len(value_list)]
    except (ValueError, IndexError):
        selected_values = []
    return selected_values

# 🔹 Hovedendpoint til at hente sponsor-data
@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    brand_value_options = [
        "Ambitiøs", "Innovativ", "Familievenlig", "Historisk", 
        "Lokal", "Energisk", "Passioneret", "Professionel",
        "Rå", "Skæv", "Soulful"
    ]

    # 🔹 Frit valg af værdier
    selected_values = request.args.getlist("brand_values")
    selected_categories = request.args.getlist("categories")

    # 🔹 Konverter numeriske valg til tekst
    selected_values = [
        brand_value_options[int(num) - 1] if num.isdigit() and 1 <= int(num) <= len(brand_value_options) 
        else num.strip()  # Frit indtastede værdier accepteres direkte
        for num in selected_values
    ]

    print("👉 Valgte brandværdier:", selected_values)
    print("👉 Valgte kategorier:", selected_categories)
    
    filtered_sponsorships = []
    for sponsor in sponsorship_data:
        brand_values = [v.strip() for v in sponsor.get("Brandværdier", "").replace(";", ",").split(",")]
        category = sponsor.get("Kategori")

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