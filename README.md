# PokéGuess

A Wordle-inspired daily Pokémon guessing game. Each day players worldwide try to identify the "Pokémon of the Day" from a blurred sprite and progressively revealing clues. This repository contains a React frontend and a Flask backend that uses the PokéAPI.

## Table of contents
- [Key features](#key-features)
- [Tech stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Local setup](#local-setup)
  - [Backend (Flask)](#backend-flask)
  - [Frontend (React)](#frontend-react)
- [Gameplay](#gameplay)
- [Deployment](#deployment)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License & credits](#license--credits)
- [Contact](#contact)

## Key features
- Daily Challenge: everyone receives the same Pokémon each day.
- Progressive hints: image becomes clearer and textual hints are revealed after incorrect guesses.
- Fuzzy matching: tolerant to minor typos using fuzzy string matching.
- Dynamic hints: hints generated from Pokémon attributes (color, evolution, legendary status, etc.).
- Mobile-first, responsive UI.

## Tech stack
- Frontend: React (Vite)
- Backend: Flask (Python)
- Fuzzy matching: thefuzz (Python)
- Data source: PokéAPI
- Deployment: Vercel (frontend) and Render (backend)

## Prerequisites
- Node.js & npm
- Python 3.x and pip

## Local setup

Note: run the backend and frontend in separate terminals.

### Backend (Flask)
1. Clone repo and enter backend:
   ```bash
   git clone <repo-url>
   cd who-that-pokemon/pokemon-backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```
   The backend will be available at http://localhost:5000

### Frontend (React)
1. In a new terminal:
   ```bash
   cd who-that-pokemon/pokemon-frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Create a local .env with the backend URL:
   ```bash
   echo "VITE_API_URL=http://localhost:5000" > .env
   ```
4. Start the dev server:
   ```bash
   npm run dev
   ```
   Open the site at the URL shown by Vite (commonly http://localhost:5173)

## Gameplay
- A heavily blurred sprite is shown.
- Players type a guess (case-insensitive).
- Correct guess advances to the next challenge and awards points.
- Incorrect guess reveals a new hint and sharpens the sprite; limited attempts apply.
- Hints are filtered to avoid redundancy.

## Deployment
- Frontend: deploy static site (Vercel recommended).
- Backend: deploy Flask app as a web service (e.g., Render).
- Set VITE_API_URL in the frontend environment to point to the live backend URL.

## Project structure (example)
- pokemon-frontend/ — React source, Vite config
- pokemon-backend/ — Flask app and dependencies
- assets/ or public/ — images and static assets
- data/ — optional manifests (e.g., pokemon.json)
- README.md — this file

## Contributing
1. Fork the repository.
2. Create a branch: `git checkout -b feat/my-change`
3. Implement changes and add tests if applicable.
4. Open a pull request with a clear description.


## Contact
Open an issue or pull request in this repository for questions, bug reports, or feature suggestions.