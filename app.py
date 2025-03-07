import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# 🔹 Indlæs JSON-databasen ved opstart
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "sponsorship_data.json")

with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
    sponsorship_data = json.load(f)

# Liste over tilladte e-mails
allowed_emails = {"kim.traulsen@gmail.com", "bruger@firma.dk", "dinmail@domæne.dk"}

@app.before_request
def log_request_info():
    print("Modtaget headers:", request.headers)

@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    """Filtrerer sponsorater baseret på kategori, underkategori og specifikke parametre."""
    user_email = request.headers.get("X-User-Email")

    # 🔹 Valider e-mail
    if not user_email or user_email not in allowed_emails:
        return jsonify({"error": "Adgang nægtet"}), 403

    # 🔹 Hent søgeparametre
    category = request.args.get("category")
    subcategory = request.args.get("subcategory")
    filter_param = request.args.get("filter_param")  # fx "target_audience.age_range"
    filter_value = request.args.get("filter_value")  # fx "20-40 år"

    filtered_sponsorships = []

    # 🔹 Filtrering af data
    for cat_key, subcats in sponsorship_data.items():
        if category and cat_key != category:
            continue
        for subcat_key, sponsors in subcats.items():
            if subcategory and subcat_key != subcategory:
                continue
            for sponsor in sponsors:
                if filter_param and filter_value:
                    param_levels = filter_param.split(".")
                    value = sponsor
                    for level in param_levels:
                        value = value.get(level, "")
                        if not value:
                            break
                    if isinstance(value, str) and filter_value.lower() not in value.lower():
                        continue
                filtered_sponsorships.append(sponsor)
    
    return jsonify(filtered_sponsorships), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
