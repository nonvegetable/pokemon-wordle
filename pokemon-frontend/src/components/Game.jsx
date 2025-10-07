import React, {useEffect, useState} from "react" 
import Hints from "./Hints" 

export default function Game({pokemon}){ 
    const [pokemonGuess, setPokemonGuess] = useState(""); 
    const [pokemonName, setPokemonName] = useState("");
    const [spriteUrl, setSpriteUrl] = useState(null); 
    const [hints, setHints] = useState([]);
    const [attempts, setAttempts] = useState(0);
    const [isCorrect, setIsCorrect] = useState(false);
    const [answer, setAnswer] = useState("");
    
    useEffect(() => {
        fetch('/api/today', {
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                setSpriteUrl(data.sprite);
                setHints([data.first_hint]);
            })
    }, []); 
    
    // function guessPokemon() {
    //     event.preventDefault();

    //     fetch("/api/guess", {
    //             method: "POST",
    //             headers: {
    //                 'Content-Type': 'application/json' 
    //             },
    //             body: JSON.stringify({ pokemonGuess: pokemonGuess, attempts: attempts})
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.correct) {
    //                 setIsCorrect(true);
    //             } else {
    //                 setHints(prevHints => [...prevHints, data.new_hint]);
    //                 setAttempts(prevAttempts => prevAttempts + 1);
    //             }
    //         })
    // }
        
        // if(pokemonGuess != pokemonName){ 
        //     attempts++; hintsArray[0] 
        //     fetch("/api/hints", { 
        //         method: "POST", 
        //         body: JSON.stringify({ attempts: attempts}) 
        //     }) 
        //     .then(
        //         response => { let sprite = setSprite(response.sprite) 
        //         let hints = setHints([response.hints]) 
        //     }) 
        // } 
        
        // In Game.jsx
        // Remove the standalone `function guessPokemon() { ... }`

        return (
            <>
                <h1>Welcome to Guess the Pokemon</h1>
                <div className="game-area">
                    <img src={spriteUrl} alt="A blurred pokemon"/>
                    <form onSubmit={(event) => {
                        event.preventDefault();

                        if (attempts >= 4 || isCorrect) {
                            return;
                        }

                        fetch("/api/guess", {
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
                                setHints(prevHints => [...prevHints, data.new_hint]);
                                setAttempts(prevAttempts => prevAttempts + 1);

                                setPokemonGuess(""); 
                            }

                            if (data.answer) { 
                                setAnswer(data.answer);
                            }
                        });
                    }}>
                        <input type="text" value={pokemonGuess} onChange={(e) => setPokemonGuess(e.target.value)} disabled={attempts >= 4 || isCorrect} />
                        <button className="guess-btn" type="submit" disabled={attempts >= 4 || isCorrect} >Guess</button>
                    </form>
                    <Hints hints={hints} />
                    {isCorrect && <p className="win-message">You got it right!</p>}
                    {attempts >= 4 && !isCorrect && <p className="lose-message">Game Over! The Pokémon was: {answer}</p>}
                </div>
            </>
        )
    }