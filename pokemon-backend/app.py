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
        "types": [t['type']['name'] for t in pokemon_data['types']], 
        "ability": pokemon_data["abilities"][0]["ability"]["name"],
        "region": region,
        "is_legendary": species_data["is_legendary"],
        "is_mythical": species_data["is_mythical"],
        "evolves_from": species_data.get("evolves_from_species"), 
        "color": species_data["color"]["name"],
        "flavor_text": species_data["flavor_text_entries"][0]["flavor_text"].replace('\n', ' ').replace('\f', ' ') 
    }

    return jsonify({
        "sprite": pokemon_data["sprites"]["front_default"],
        "first_hint": f"This Pokémon is a {current_pokemon['types'][0].capitalize()} type."
    })

# previously tried to use the hints api to give hints instead of checking guesses
# still keeping it here jsut in cas efor the future

# @app.route('/api/hints', methods=['POST'])
# def get_hints():
#     attempts = request.json.get("attempts")rom the {current_pokemon['region']} region!
#     hint_list = [
#         f"Type: {current_pokemon['type'].capitalize()}",
#         f"Region: {current_pokemon['region']}",
#         f"Ability: {current_pokemon['ability'].capitalize()}",
#         f"Fun fact: {current_pokemon['flavor_text']}",
#     ]
#     return jsonify({ "hint": hint_list[min(attempts, len(hint_list)-1)] })

@app.route('/api/guess', methods=['POST'])
def user_guess():
    data = request.json
    user_guess = data.get("pokemonGuess", "").lower()
    attempts = data.get("attempts", 0)
    actual_name = current_pokemon.get("name", "").lower()

    if user_guess == actual_name:
        return jsonify({"correct": True})
    else:

        hint_pool = []

        if current_pokemon['is_legendary']:
            hint_pool.append("This Pokémon is considered Legendary.")
        elif current_pokemon['is_mythical']:
            hint_pool.append("This Pokémon is considered Mythical.")

        if current_pokemon['evolves_from']:
            hint_pool.append("This Pokémon evolves from another species.")
        else:
            hint_pool.append("This Pokémon does not evolve.")
            
        if len(current_pokemon['types']) > 1:
            hint_pool.append(f"It has two types; one of them is {current_pokemon['types'][0].capitalize()}.")

        hint_pool.append(f"It is primarily {current_pokemon['color']} in color.")
        hint_pool.append(f"It can be found in the {current_pokemon['region']} region.")
        hint_pool.append(f"Its name starts with the letter: {current_pokemon['name'][0].upper()}")
        hint_pool.append(f"One of its abilities is {current_pokemon['ability'].capitalize()}.")
        random.shuffle(hint_pool)
        hint_pool.append(f"Pokédex entry: {current_pokemon['flavor_text']}")
        hint_index = min(attempts, len(hint_pool) - 1)

        response_data = {
            "correct": False,
            "new_hint": hint_pool[hint_index] \
        }
    
        if attempts >= 3:
            response_data["answer"] = current_pokemon['name'].capitalize()

        return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5000)