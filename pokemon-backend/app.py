from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random


app = Flask(__name__)
CORS(app)

@app.route('/api/today', methods=['GET'])
def fetch_pokemon_data():
    pokemon_id = random.randint(1, 898)
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
    data = response.json()
    
    return jsonify({
        "name": data["name"],
        "type": data["types"][0]["type"]["name"],
        "sprite": data["sprites"]["front_default"]
    })

# @app.route('/api/today', methods=['GET'])
# def pokemon_of_the_day():
#     id = random.randint(1, 898)
#     return id

@app.route('/api/hints', methods=['POST'])
def get_hints():
    return jsonify({
        "hint1":
        "hint2":
        "hint3":
    })


if __name__ == '__main__':
    app.run(port=5000)