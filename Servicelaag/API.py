from flask import Flask, jsonify

app = Flask(__name__)

alleenstaand_data = [
    {"toetsingsinkomen_tot": 26500, "bedrag_per_maand": 123},
    {"toetsingsinkomen_tot": 27000, "bedrag_per_maand": 121},
    {"toetsingsinkomen_tot": 27500, "bedrag_per_maand": 115},
    {"toetsingsinkomen_tot": 28000, "bedrag_per_maand": 110},
    {"toetsingsinkomen_tot": 28500, "bedrag_per_maand": 104},
    {"toetsingsinkomen_tot": 29000, "bedrag_per_maand": 98},
    {"toetsingsinkomen_tot": 29500, "bedrag_per_maand": 93},
    {"toetsingsinkomen_tot": 30000, "bedrag_per_maand": 87},
    {"toetsingsinkomen_tot": 30500, "bedrag_per_maand": 81},
    {"toetsingsinkomen_tot": 31000, "bedrag_per_maand": 75},
    {"toetsingsinkomen_tot": 31500, "bedrag_per_maand": 70},
    {"toetsingsinkomen_tot": 32000, "bedrag_per_maand": 64},
    {"toetsingsinkomen_tot": 32500, "bedrag_per_maand": 58},
    {"toetsingsinkomen_tot": 33000, "bedrag_per_maand": 53},
    {"toetsingsinkomen_tot": 33500, "bedrag_per_maand": 47},
    {"toetsingsinkomen_tot": 34000, "bedrag_per_maand": 41},
    {"toetsingsinkomen_tot": 34500, "bedrag_per_maand": 36},
    {"toetsingsinkomen_tot": 35000, "bedrag_per_maand": 30},
    {"toetsingsinkomen_tot": 35500, "bedrag_per_maand": 24},
    {"toetsingsinkomen_tot": 36000, "bedrag_per_maand": 19},
    {"toetsingsinkomen_tot": 36500, "bedrag_per_maand": 13},
    {"toetsingsinkomen_tot": 37000, "bedrag_per_maand": 7},
    {"toetsingsinkomen_tot": 37496, "bedrag_per_maand": 0, "boodschap": "U krijgt geen zorgtoeslag"}
]
    
met_partner_data = [
    {"toetsingsinkomen_tot": 26500, "bedrag_per_maand": 236},
    {"toetsingsinkomen_tot": 27000, "bedrag_per_maand": 233},
    {"toetsingsinkomen_tot": 27500, "bedrag_per_maand": 228},
    {"toetsingsinkomen_tot": 28000, "bedrag_per_maand": 222},
    {"toetsingsinkomen_tot": 28500, "bedrag_per_maand": 216},
    {"toetsingsinkomen_tot": 29000, "bedrag_per_maand": 211},
    {"toetsingsinkomen_tot": 29500, "bedrag_per_maand": 205},
    {"toetsingsinkomen_tot": 30000, "bedrag_per_maand": 199},
    {"toetsingsinkomen_tot": 30500, "bedrag_per_maand": 194},
    {"toetsingsinkomen_tot": 31000, "bedrag_per_maand": 188},
    {"toetsingsinkomen_tot": 31500, "bedrag_per_maand": 182},
    {"toetsingsinkomen_tot": 32000, "bedrag_per_maand": 177},
    {"toetsingsinkomen_tot": 32500, "bedrag_per_maand": 171},
    {"toetsingsinkomen_tot": 33000, "bedrag_per_maand": 165},
    {"toetsingsinkomen_tot": 33500, "bedrag_per_maand": 159},
    {"toetsingsinkomen_tot": 34000, "bedrag_per_maand": 154},
    {"toetsingsinkomen_tot": 34500, "bedrag_per_maand": 148},
    {"toetsingsinkomen_tot": 35000, "bedrag_per_maand": 142},
    {"toetsingsinkomen_tot": 35500, "bedrag_per_maand": 137},
    {"toetsingsinkomen_tot": 36000, "bedrag_per_maand": 131},
    {"toetsingsinkomen_tot": 36500, "bedrag_per_maand": 125},
    {"toetsingsinkomen_tot": 37000, "bedrag_per_maand": 120},
    {"toetsingsinkomen_tot": 37500, "bedrag_per_maand": 114},
    {"toetsingsinkomen_tot": 38000, "bedrag_per_maand": 108},
    {"toetsingsinkomen_tot": 38500, "bedrag_per_maand": 102},	
    {"toetsingsinkomen_tot": 39000, "bedrag_per_maand": 97},
    {"toetsingsinkomen_tot": 39500, "bedrag_per_maand": 91},
    {"toetsingsinkomen_tot": 40000, "bedrag_per_maand": 85},
    {"toetsingsinkomen_tot": 40500, "bedrag_per_maand": 80},
    {"toetsingsinkomen_tot": 41000, "bedrag_per_maand": 74},
    {"toetsingsinkomen_tot": 41500, "bedrag_per_maand": 68},
    {"toetsingsinkomen_tot": 42000, "bedrag_per_maand": 63},
    {"toetsingsinkomen_tot": 42500, "bedrag_per_maand": 57},
    {"toetsingsinkomen_tot": 43000, "bedrag_per_maand": 51},
    {"toetsingsinkomen_tot": 43500, "bedrag_per_maand": 46},
    {"toetsingsinkomen_tot": 44000, "bedrag_per_maand": 40},
    {"toetsingsinkomen_tot": 44500, "bedrag_per_maand": 34},
    {"toetsingsinkomen_tot": 45000, "bedrag_per_maand": 28},
    {"toetsingsinkomen_tot": 45500, "bedrag_per_maand": 23},
    {"toetsingsinkomen_tot": 46000, "bedrag_per_maand": 17},
    {"toetsingsinkomen_tot": 46500, "bedrag_per_maand": 11},
    {"toetsingsinkomen_tot": 47000, "bedrag_per_maand": 6},
    {"toetsingsinkomen_tot": 47368, "bedrag_per_maand": 0, "boodschap": "U krijgt geen zorgtoeslag"}
]

@app.route('/zorgtoeslag_alleenstaand', methods=['GET'])
def Zorgtoeslag_alleenstaand():
    return jsonify(alleenstaand_data)

@app.route('/zorgtoeslag_met_partner', methods=['GET'])
def Zorgtoeslag_met_partner():
    return jsonify(met_partner_data)

if __name__ == '__main__':
    app.run(debug=True)
