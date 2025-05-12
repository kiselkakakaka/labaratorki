import React, { useState } from 'react';
import './App.css';


function App() {
  const [items, setItems] = useState([]);
  
  const addItem = () => {
    const newItem = `Элемент ${items.length + 1}`;
    setItems(prevItems => [...prevItems, newItem]);
  };

  return (
    <div>
      <h1>Добавление элемента в список</h1>
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