import React, { useState } from 'react';
import './App.css';


function App() {
  const [items, setItems] = useState([]);
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');
  const [input3, setInput3] = useState('');

  const addItem = () => {
    if (input1.trim() && input2.trim() && input3.trim()) { 
      const newItem = `${input1}, ${input2}, ${input3}`;
      setItems(prevItems => [...prevItems, newItem]);
      setInput1('');
      setInput2('');
      setInput3('');
    }
  };

  return (
    <div>
      <h1>Добавление элемента в список</h1>
      <input
        type="text"
        value={input1}
        onChange={(e) => setInput1(e.target.value)}
        placeholder="Введите первое значение"
      />
      <input
        type="text"
        value={input2}
        onChange={(e) => setInput2(e.target.value)}
        placeholder="Введите второе значение"
      />
      <input
        type="text"
        value={input3}
        onChange={(e) => setInput3(e.target.value)}
        placeholder="Введите третье значение"
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