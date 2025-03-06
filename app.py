import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Liste over tilladte mails
allowed_emails = {"kim.traulsen@gmail.com", "bruger@firma.dk", "dinmail@domæne.dk"}

@app.route("/validate_email", methods=["GET"])
def validate_email():
    user_email = request.args.get("email")

    if not user_email:
        response = {"error": "Ingen mailadresse oplyst"}
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False).encode('utf-8'),
            status=400,
            mimetype='application/json'
        )

    if "@" not in user_email:
        response = {"error": "Ugyldig mailadresse"}
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False).encode('utf-8'),
            status=400,
            mimetype='application/json'
        )

    if user_email not in allowed_emails:
        response = {"error": "Adgang nægtet"}
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False).encode('utf-8'),
            status=403,
            mimetype='application/json'
        )

    response = {"message": "Mail godkendt"}
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False).encode('utf-8'),
        status=200,
        mimetype='application/json'
    )

rights_database = [
    # Fodboldklubber
    {"name": "FC København", "values": "Tradition, konkurrence, internationalt udsyn", "audience": "Fodboldfans", "activation": "TV-eksponering"},
    {"name": "Brøndby IF", "values": "Passion, fællesskab, dedikation", "audience": "Fodboldfans", "activation": "Stadionbranding"},
    {"name": "Aalborg BK", "values": "Historie, udvikling, talentfokus", "audience": "Fodboldfans", "activation": "Lokale sponsoraktiviteter"},
    {"name": "FC Nordsjælland", "values": "Innovation, ungdomsudvikling, bæredygtighed", "audience": "Unge, familier", "activation": "CSR-samarbejde"},
    
    # Håndboldklubber
    {"name": "Aalborg Håndbold", "values": "Vindervilje, konkurrence, international ambition", "audience": "Håndboldfans", "activation": "Arena branding"},
    {"name": "GOG", "values": "Ungdomsudvikling, fællesskab, engagement", "audience": "Børnefamilier, lokale sportsfans", "activation": "Lokale events"},
    
    # Festivaler & Kultur
    {"name": "Roskilde Festival", "values": "Kreativitet, fællesskab, bæredygtighed", "audience": "Musikelskere", "activation": "Live events"},
    {"name": "Smukfest", "values": "Nærvær, hygge, unikke oplevelser", "audience": "Musikfans, unge voksne", "activation": "Storytelling, sponsor lounges"},
    {"name": "NorthSide", "values": "Bæredygtighed, innovation, moderne musik", "audience": "Miljøbevidste unge", "activation": "Bæredygtige samarbejder"},
    
    # Erhvervs- & bæredygtighedsrettigheder
    {"name": "TechBBQ", "values": "Innovation, iværksætteri, netværk", "audience": "Startups, investorer", "activation": "Keynote branding, netværksevents"},
    {"name": "Folkemødet", "values": "Demokrati, debat, engagement", "audience": "Politikere, NGO'er, erhvervsfolk", "activation": "Paneldebatter, partnerskaber"},
    
    # Esport & Gaming
    {"name": "Blast Premier", "values": "Konkurrence, gaming, digital innovation", "audience": "Esportsfans, gamere", "activation": "Digitale sponsorater"},
    {"name": "Astralis", "values": "High performance, mental styrke, gaming", "audience": "Gamere, unge mænd", "activation": "Merchandise, streaming-partnerskaber"}
]

# 🔹 **NY RUTE: Valider mail**
@app.route("/validate_email", methods=["GET"])
def validate_email():
    user_email = request.args.get("email")

    if not user_email:
        return jsonify({"error": "Ingen mailadresse oplyst"}), 400  # Bad request

    if "@" not in user_email:
        return jsonify({"error": "Ugyldig mailadresse"}), 400  # Bad request

    if user_email not in allowed_emails:
        return jsonify({"error": "Adgang nægtet"}), 403  # Forbidden

    return jsonify({"message": "Mail godkendt"}), 200  # OK

# 🔹 **OPDATERET /sponsorships: Kræver godkendt mail**
@app.route('/sponsorships', methods=['GET'])
def get_sponsorships():
    user_email = request.headers.get("X-User-Email")

    # Tjek om mail er oplyst
    if not user_email:
        return jsonify({"error": "Ingen mailadresse oplyst"}), 400

    # Tjek om mail er godkendt
    if user_email not in allowed_emails:
        return jsonify({"error": "Adgang nægtet"}, ensure_ascii=False), 403

    # Hent søgeparametre fra URL
    values_query = request.args.get("values")
    audience_query = request.args.get("audience")

    # Konverter til liste (hvis bruger har angivet flere værdier, fx "innovation, bæredygtighed")
    values_filter = values_query.split(",") if values_query else []
    audience_filter = audience_query.split(",") if audience_query else []

    # Filtrer databasen
    filtered_sponsorships = [
        sponsorship for sponsorship in rights_database
        if (not values_filter or any(value in sponsorship["values"] for value in values_filter))
        and (not audience_filter or any(aud in sponsorship["audience"] for aud in audience_filter))
    ]

    # Returnér filtrerede resultater
    return jsonify(filtered_sponsorships)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Brug Render's port, ellers 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Lyt på alle netværk
