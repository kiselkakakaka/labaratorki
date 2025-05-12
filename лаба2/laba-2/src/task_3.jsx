import React, { useState } from 'react';
import './App.css';


function App() {
  const [values, setValues] = useState(Array(5).fill(''));

  function handleInputChange(index, event) {
    const newValues = [...values];
    newValues[index] = event.target.value;
    setValues(newValues);
  }

  function calculateAverage() {
    const numbers = values.map(value => parseFloat(value)).filter(num => !isNaN(num));
    const total = numbers.reduce((acc, num) => acc + num, 0);
    return numbers.length > 0 ? (total / numbers.length).toFixed(2) : 0;
  }

  return (
    <div>
      <h1>Введите числа</h1>
      {values.map((value, index) => (
        <input
          key={index}
          type="number"
          value={value}
          onChange={(event) => handleInputChange(index, event)}
          placeholder={`Число ${index + 1}`}
        />
      ))}

      <h2>Среднее арифметическое:</h2>
      <p>{calculateAverage()}</p>
    </div>
  );
}

export default App;
