import React, {useEffect, useState} from "react" 
import Hints from "./Hints" 

const API_URL = import.meta.env.VITE_API_URL || '';

export default function Game(){ 
    const MAX_ATTEMPTS = 4;
    const [pokemonGuess, setPokemonGuess] = useState(""); 
    const [spriteUrl, setSpriteUrl] = useState(null); 
    const [hints, setHints] = useState([]);
    const [attempts, setAttempts] = useState(0);
    const [isCorrect, setIsCorrect] = useState(false);
    const [answer, setAnswer] = useState("");
    const [nameLength, setNameLength] = useState(0); // State for character length

    useEffect(() => {
        fetch(`${API_URL}/api/today`)
            .then(response => response.json())
            .then(data => {
                setSpriteUrl(data.sprite);
                setHints([data.first_hint]);
                setNameLength(data.name_length); // Save the length from the API
            });
    }, []); 
    
    const handleGuessSubmit = (event) => {
        event.preventDefault();
        if (attempts >= MAX_ATTEMPTS || isCorrect || !pokemonGuess) {
            return;
        }

        fetch(`${API_URL}/api/guess`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pokemonGuess: pokemonGuess,
                attempts: attempts 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.correct) {
                setIsCorrect(true);
            } else {
                if (data.new_hint) {
                    setHints(prevHints => [...prevHints, data.new_hint]);
                }
                setAttempts(prevAttempts => prevAttempts + 1);
                setPokemonGuess(""); 
            }
            if (data.answer) { 
                setAnswer(data.answer);
            }
        });
    };

    return (
        <div className="game-area">
            <h1>Who's That Pokémon?</h1>
            
            <div className="game-stats">
                <div className="attempts-counter">
                    Guesses Remaining: {MAX_ATTEMPTS - attempts}
                </div>
                {/* Display the character length */}
                {nameLength > 0 && (
                    <div className="char-length">
                        Length: {nameLength} letters
                    </div>
                )}
            </div>

            <img 
                src={spriteUrl} 
                alt="A blurred pokemon" 
                className={`pokemon-sprite attempts-${attempts} ${isCorrect || attempts >= MAX_ATTEMPTS ? 'revealed' : ''}`}
            />
            <form onSubmit={handleGuessSubmit}>
                <input 
                    type="text" 
                    value={pokemonGuess} 
                    onChange={(e) => setPokemonGuess(e.target.value)} 
                    disabled={attempts >= MAX_ATTEMPTS || isCorrect}
                    placeholder="Enter your guess..."
                />
                <button 
                    className="guess-btn" 
                    type="submit" 
                    disabled={attempts >= MAX_ATTEMPTS || isCorrect} 
                >
                    Guess
                </button>
            </form>
            <Hints hints={hints} />
            {isCorrect && <p className="win-message">You Guessed Correctly!</p>}
            {attempts >= MAX_ATTEMPTS && !isCorrect && <p className="lose-message">Game Over! The Pokémon was: {answer}</p>}
        </div>
    )
}