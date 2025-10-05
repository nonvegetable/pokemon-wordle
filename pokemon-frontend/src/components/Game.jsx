import React, {useState} from "react"
import Hints from "./Hints"

export default function Game({pokemon}){

    const [pokemonGuess, setPokemonGuess] = useState("");

    const hintsArray = []

    function guessPokemon(){
        alert(`You guessed ${pokemonGuess}`)
        //if wrong, send the prop to the Hints component to dynamically show hints about that pokemon
        let attempts;
    }

    return(
        <>
            <h1>Welcome to Guess the Pokemon</h1>
            <div className="game-area">
                <img src="something" alt="pokemon"/>
                <input
                    type="text"
                    value={pokemonGuess}
                    onChange={(e) => setPokemonGuess(e.target.value)}
                />
                <button className="guess-btn" onClick={guessPokemon} >Guess</button>
                {/* <Hints pokemon={{pokemonName: name, no: attempts, hints: hintsArray}}/> */}
            </div>
 
        </>
    )
}