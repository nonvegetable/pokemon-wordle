import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Game from './components/Game';
import './App.css'; 

function App() {
  return (
    <div className="app-container">
      <Navbar />
      <main>
        <Game />
      </main>
      <Footer />
    </div>
  );
}

export default App;