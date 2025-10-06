from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

regions = {
  "generation-i": "Kanto",
  "generation-ii": "Johto",
  "generation-iii": "Hoenn",
  "generation-iv": "Sinnoh",
  "generation-v": "Unova",
  "generation-vi": "Kalos",
  "generation-vii": "Alola",
  "generation-viii": "Galar",
  "generation-ix": "Paldea"
}

app = Flask(__name__)
CORS(app)

@app.route('/api/today', methods=['GET'])
def fetch_pokemon_data():
    pokemon_id = random.randint(1, 898)
    pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
    species_data = requests.get(pokemon_data["species"]["url"]).json()
    region = regions[species_data["generation"]["name"]]

    global current_pokemon
    current_pokemon = {
        "name": pokemon_data["name"],
        "type": pokemon_data["types"][0]["type"]["name"],
        "ability": pokemon_data["abilities"][0]["ability"]["name"],
        "generation": species_data["generation"]["name"],
        "region": region,
        "is_legendary": species_data["is_legendary"],
        "flavor_text": species_data["flavor_text_entries"][0]["flavor_text"]
    }

    return jsonify({
        "sprite": pokemon_data["sprites"]["front_default"],
        "first_hint": f"This Pokémon is a {current_pokemon['type'].capitalize()} type from the {current_pokemon['region']} region!"
    })


@app.route('/api/hints', methods=['POST'])
def get_hints():
    attempts = request.json.get("attempts")
    hint_list = [
        f"Type: {current_pokemon['type'].capitalize()}",
        f"Region: {current_pokemon['region']}",
        f"Ability: {current_pokemon['ability'].capitalize()}",
        f"Fun fact: {current_pokemon['flavor_text']}",
    ]
    return jsonify({ "hint": hint_list[min(attempts, len(hint_list)-1)] })

@app.route('/api/guess', methods=['POST'])
def user_guess():
    user_guess = request.json.get("pokemonGuess", "").lower()
    actual_name = current_pokemon.get("name", "").lower()

    if user_guess == actual_name:
        return jsonify({"correct": True})
    else:
        return jsonify({
            "correct": False,
            "new_hint": f"Starts with: {current_pokemon['name'][0].upper()}"
        })

if __name__ == '__main__':
    app.run(port=5000)