from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
from datetime import date
from thefuzz import fuzz # <-- NEW: Import for fuzzy string matching

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

# --- NEW: Logic for "Pokémon of the Day" ---
# These variables will store the daily Pokémon's data in memory.
pokemon_of_the_day = {}
pokemon_date = None

def get_pokemon_for_today():

    global pokemon_of_the_day, pokemon_date
    today = date.today()

    # If we already have a Pokémon and it's for today, no need to fetch again.
    if pokemon_of_the_day and pokemon_date == today:
        return

    # Create a seed from the date (e.g., 20251008)
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    pokemon_id = random.randint(1, 898)

    # Fetch all data for the selected Pokémon
    pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
    species_data = requests.get(pokemon_data["species"]["url"]).json()
    
    # (The rest of the data fetching logic is the same as before)
    generation_info = species_data.get("generation")
    region = regions.get(generation_info["name"]) if generation_info else "an unknown region"

    flavor_text = "No Pokédex entry found."
    for entry in species_data.get("flavor_text_entries", []):
        if entry.get("language", {}).get("name") == "en":
            flavor_text = entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
            break
            
    name_length = len(pokemon_data["name"])
    primary_type = pokemon_data['types'][0]['type']['name'].capitalize()

    hint_pool = []
    if species_data.get("is_legendary"): hint_pool.append("This Pokémon is Legendary.")
    elif species_data.get("is_mythical"): hint_pool.append("This Pokémon is Mythical.")
    if species_data.get("evolves_from_species"): hint_pool.append("This Pokémon evolves from another species.")
    else: hint_pool.append("This Pokémon does not evolve.")
    color_name = species_data.get("color", {}).get("name", "unknown")
    hint_pool.append(f"It is primarily {color_name} in color.")
    random.shuffle(hint_pool)
    final_hints = [ f"Its name starts with: {pokemon_data['name'][0].upper()}", f"Pokédex entry: {flavor_text}" ]
    
    # Store the generated Pokémon data globally for the day
    pokemon_date = today
    pokemon_of_the_day = {
        "name": pokemon_data["name"],
        "sprite": pokemon_data.get("sprites", {}).get("front_default"),
        "name_length": name_length,
        "first_hint": f"This Pokémon has {name_length} letters. It is a {primary_type} type from the {region} region.",
        "hint_list": hint_pool + final_hints
    }

@app.route('/api/today', methods=['GET'])
def fetch_pokemon_data():
    get_pokemon_for_today() # Ensure the daily Pokémon is loaded
    # Return only the safe, initial data to the frontend
    return jsonify({
        "sprite": pokemon_of_the_day["sprite"],
        "name_length": pokemon_of_the_day["name_length"],
        "first_hint": pokemon_of_the_day["first_hint"]
    })

@app.route('/api/guess', methods=['POST'])
def user_guess():
    get_pokemon_for_today() # Ensure the daily Pokémon is loaded before a guess
    if not pokemon_of_the_day:
        return jsonify({"error": "Could not determine the Pokémon of the day. Please try again."}), 500

    data = request.json
    user_guess = data.get("pokemonGuess", "").lower()
    attempts = data.get("attempts", 0)
    actual_name = pokemon_of_the_day.get("name", "").lower()

    # --- NEW: Use fuzzy matching instead of an exact check ---
    # We set a ratio of 85, which is good for catching minor typos.
    if fuzz.ratio(user_guess, actual_name) > 85:
        return jsonify({"correct": True})
    else:
        if attempts >= 3:
            return jsonify({
                "correct": False,
                "answer": pokemon_of_the_day.get('name', 'Unknown').capitalize()
            })

        response_data = {
            "correct": False,
            "new_hint": pokemon_of_the_day.get("hint_list", [])[attempts]
        }
        return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5000)

