import React, { useState } from 'react';
import './App.css';


function App() {
  const [items, setItems] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const addItem = () => {
    if (inputValue.trim() !== '') { 
      setItems(prevItems => [...prevItems, inputValue]);
      setInputValue('');
    }
  };

  return (
    <div>
      <h1>Добавление элемента в список</h1>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Введите текст"
      />
      <button onClick={addItem}>Добавить элемент</button>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;