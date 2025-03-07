import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# 🔹 Indlæs JSON-databasen ved opstart
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "sponsorship_data.json")

with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
    rights_database = json.load(f)

# Liste over tilladte e-mails
allowed_emails = {"kim.traulsen@gmail.com", "bruger@firma.dk", "dinmail@domæne.dk"}

@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    """Filtrerer sponsorater baseret på kategori, underkategori og specifik parameter."""
    user_email = request.headers.get("X-User-Email")

    # 🔹 Valider e-mail
    if not user_email or user_email not in allowed_emails:
        return jsonify({"error": "Adgang nægtet"}), 403

    # 🔹 Hent søgeparametre
    category = request.args.get("category")
    subcategory = request.args.get("subcategory")
    filter_param = request.args.get("filter_param")  # fx "målgruppe"
    filter_value = request.args.get("filter_value")  # fx "unge"

    # 🔹 Filtrering af data
    filtered_sponsorships = [
        s for s in rights_database
        if (not category or s.get("category") == category) and
           (not subcategory or s.get("subcategory") == subcategory) and
           (not filter_param or filter_value.lower() in s.get(filter_param, "").lower())
    ]

    # 🚀 RETURN ER HER INDE I FUNKTIONEN! 🚀
    return jsonify(filtered_sponsorships), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
