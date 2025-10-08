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

current_pokemon = {}

@app.route('/api/today', methods=['GET'])
def fetch_pokemon_data():
    pokemon_id = random.randint(1, 898)
    pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
    species_data = requests.get(pokemon_data["species"]["url"]).json()

    generation_info = species_data.get("generation")
    if generation_info and generation_info.get("name") in regions:
        region = regions[generation_info["name"]]
    else:
        region = "an unknown region"

    flavor_text = "No Pokédex entry found for this Pokémon." 
    for entry in species_data.get("flavor_text_entries", []):
        if entry.get("language", {}).get("name") == "en":
            flavor_text = entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
            break 

    # Prepare data for hints
    name_length = len(pokemon_data["name"])
    primary_type = pokemon_data['types'][0]['type']['name'].capitalize()

    hint_pool = []
    if species_data.get("is_legendary"):
        hint_pool.append("This Pokémon is considered Legendary.")
    elif species_data.get("is_mythical"):
        hint_pool.append("This Pokémon is considered Mythical.")
    if species_data.get("evolves_from_species"):
        hint_pool.append("This Pokémon evolves from another species.")
    else:
        hint_pool.append("This Pokémon does not evolve from another species.")
    color_name = species_data.get("color", {}).get("name", "an unknown")
    hint_pool.append(f"It is primarily {color_name} in color.")
    random.shuffle(hint_pool)
    final_hints = [
        f"Its name starts with the letter: {pokemon_data['name'][0].upper()}",
        f"Pokédex entry: {flavor_text}"
    ]
    all_hints = hint_pool + final_hints

    global current_pokemon
    current_pokemon = {
        "name": pokemon_data["name"],
        "hint_list": all_hints
    }

    # Return all necessary info to the frontend
    return jsonify({
        "sprite": pokemon_data.get("sprites", {}).get("front_default"),
        "name_length": name_length,
        "first_hint": f"This Pokémon is a {primary_type} type from the {region} region."
    })

@app.route('/api/guess', methods=['POST'])
def user_guess():
    if not current_pokemon:
        return jsonify({"error": "No Pokémon has been selected. Please refresh to start a new game."}), 400
    data = request.json
    user_guess = data.get("pokemonGuess", "").lower()
    attempts = data.get("attempts", 0)
    actual_name = current_pokemon.get("name", "").lower()
    if user_guess == actual_name:
        return jsonify({"correct": True})
    else:
        if attempts >= 3:
            return jsonify({"correct": False, "answer": current_pokemon.get('name', 'Unknown').capitalize()})
        response_data = {"correct": False, "new_hint": current_pokemon.get("hint_list", [])[attempts]}
        return jsonify(response_data)
    
if __name__ == '__main__':
    app.run(port=5000)

