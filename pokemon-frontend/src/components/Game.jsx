import React, {useState} from "react" 
import Hints from "./Hints" 

export default function Game({pokemon}){ 
    const [pokemonGuess, setPokemonGuess] = useState(""); 
    const pokemonName; //fetched from backend 
    fetch("api/today") 
    const hintsArray = [] //fetched from backend 
    
    function guessPokemon(){ 
        //if wrong, send the prop to the Hints component to dynamically show hints about that pokemon 
        let attempts = 0; 
        
        if(pokemonGuess != pokemonName){ 
            attempts++; hintsArray[0] //first from the hints should be displayed 
            fetch("/api/hints", { 
                method: "POST", 
                body: JSON.stringify({ attempts: attempts }) }) 
                .then(response => { let sprite = setSprite(response.sprite) 
                    let hints = setHints([response.hints]) 
                }) 
            } 
        } 
        
        return( 
            <> 
                <h1>Welcome to Guess the Pokemon</h1>
                <div className="game-area"> 
                    <img src="something" alt="pokemon"/> 
                    <input type="text" value={pokemonGuess} onChange={(e) => setPokemonGuess(e.target.value)} /> 
                    <button className="guess-btn" onClick={guessPokemon} >Guess</button> 
                    {/* <Hints pokemon={{pokemonName: name, no: attempts, hints: hintsArray}}/> */} 
                </div> 
            </> 
        )
    }