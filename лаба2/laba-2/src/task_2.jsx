import React, { useState } from 'react';
import './App.css';


function App() {
  const [inputValue, setInputValue] = useState('');

  function handleInputChange(event) {
    setInputValue(event.target.value);
  }

  return (
    <div>
      <h1>Введите текст</h1>
      <input
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Введите текст"
      />

      <h2>Количество символов:</h2>
      <p>{inputValue.length}</p>
    </div>
  );
}

export default App;