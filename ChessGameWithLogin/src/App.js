import React, { useState } from 'react';
import ChessBoard from './components/ChessBoard';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';

const handleLogin = async (username, password) => {
  try {
    const response = await axios.post('/api/login', { username, password });
    setUser(response.data);
  } catch (error) {
    console.error('Login failed:', error);
  }
};

const handleRegistration = async (username, password) => {
  try {
    const response = await axios.post('/api/register', { username, password });
    setUser(response.data);
  } catch (error) {
    console.error('Registration failed:', error);
  }
};

const handleMove = async (from, to) => {
  try {
    const response = await axios.post('/api/move', { from, to });
    setGame(response.data);
  } catch (error) {
    console.error('Invalid move:', error);
  }
};

  return (
    <div className="app">
      <h1>Chess Game</h1>
      {user ? (
        <div className="chess-container">
          <ChessBoard board={game.board} onMove={handleMove} />
        </div>
      ) : (
        <>
          <LoginForm onLogin={handleLogin} />
          <RegistrationForm onRegister={handleRegistration} />
        </>
      )}
    </div>
  );
;

export default App;