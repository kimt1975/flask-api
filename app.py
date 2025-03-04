from flask import Flask, jsonify
import json

app = Flask(__name__)

# Dummy-database med sponsorrettigheder
sponsorships = [
    {"name": "FC København", "values": "Tradition, konkurrence, internationalt udsyn", "audience": "Fodboldfans", "activation": "TV-eksponering"},
    {"name": "Roskilde Festival", "values": "Kreativitet, fællesskab, bæredygtighed", "audience": "Musikelskere", "activation": "Live events"},
    {"name": "Aalborg Håndbold", "values": "Vindervilje, konkurrence, international ambition", "audience": "Håndboldfans", "activation": "Arena branding"}
]

@app.route('/')
def home():
    return "Flask virker!"

@app.route('/sponsorships', methods=['GET'])
def get_sponsorships():
    return app.response_class(
        response=json.dumps(sponsorships, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)