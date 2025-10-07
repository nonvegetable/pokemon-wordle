import React, {useEffect, useState} from "react" 
import Hints from "./Hints" 

export default function Game({pokemon}){ 
    const [pokemonGuess, setPokemonGuess] = useState(""); 
    const [pokemonName, setPokemonName] = useState("");
    const [spriteUrl, setSpriteUrl] = useState(''); // Or null
    const [hints, setHints] = useState([]);
    const [attempts, setAttempts] = useState(0);
    const [isCorrect, setIsCorrect] = useState(false);
    
    useEffect(() => {
        fetch('/api/today')
            .then(response => response.json())
            .then(data => {
                setSpriteUrl(data.sprite);
                setHints([data.first_hint]);
            })
    }, []); 
    
    function guessPokemon() {
        fetch("/api/guess", {
                method: "POST",
                body: JSON.stringify({ pokemonGuess: pokemonGuess })
            })
            .then(response => response.json())
            .then(data => {
                if (data.correct) {
                    setIsCorrect(true);
                } else {
                    setHints(prevHints => [...prevHints, data.new_hint]);
                    setAttempts(prevAttempts => prevAttempts + 1);
                }
            })
    }
        
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
        
        return( 
            <> 
                <h1>Welcome to Guess the Pokemon</h1>
                <div className="game-area"> 
                    <img src={spriteUrl} alt="A blurred pokemon"/> 
                    <input type="text" value={pokemonGuess} onChange={(e) => setPokemonGuess(e.target.value)} /> 
                    <button className="guess-btn" onClick={guessPokemon}>Guess</button> 
                    <Hints hints={hints} /> 
                </div>
            </> 
        )
    }