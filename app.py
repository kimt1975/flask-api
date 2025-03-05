from flask import Flask, jsonify
import json

app = Flask(__name__)

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


@app.route('/sponsorships', methods=['GET'])
def get_sponsorships():
    try:
        return jsonify(rights_database)  # Flask's indbyggede JSON-metode
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Returnér detaljeret fejlhåndtering

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Brug Render's port, ellers 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Lyt på alle netværk
