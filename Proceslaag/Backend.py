from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000"

@app.route('/bereken_zorgtoeslag', methods=['GET'])
def bereken_zorgtoeslag():
    status = request.args.get('status', '')
    inkomen = int(request.args.get('inkomen', 0))

    # Bepaal het juiste endpoint op basis van de status
    if status == 'alleenstaand':
        endpoint = '/zorgtoeslag_alleenstaand'
    elif status == 'met_partner':
        endpoint = '/zorgtoeslag_met_partner'
    else:
        return jsonify({"error": "Ongeldige status"}), 400

    # Haal data op van de API-server
    response = requests.get(f"{API_URL}{endpoint}")
    if response.status_code != 200:
        return jsonify({"error": "Kon gegevens niet ophalen van de API"}), 500

    data = response.json()

    # Zoek het juiste bedrag
    for item in data:
        if inkomen <= item["toetsingsinkomen_tot"]:
            return jsonify(item)

    # Als het inkomen hoger is dan alle grenzen in de dataset
    return jsonify({"error": "Geen zorgtoeslag beschikbaar voor dit inkomen"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
