import React, { useState } from 'react';
import './App.css';


function App() {
  const initialArray = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  const [numbers, setNumbers] = useState(initialArray);

  const calculateAverage = () => {
    const sum = numbers.reduce((acc, num) => acc + num, 0);
    return (sum / numbers.length).toFixed(2);
  };

  const handleInputChange = (index, event) => {
    const newNumbers = [...numbers];
    newNumbers[index] = Number(event.target.value);
    setNumbers(newNumbers);
  };

  return (
    <div>
      <h1>Редактирование массива и расчет среднего арифметического</h1>
      <div>
        {numbers.map((num, index) => (
          <div key={index}>
            <label>
              Элемент {index + 1}:
              <input
                type="number"
                value={num}
                onChange={(event) => handleInputChange(index, event)}
              />
            </label>
          </div>
        ))}
      </div>
      <h2>Среднее арифметическое: {calculateAverage()}</h2>
    </div>
  );
}

export default App;