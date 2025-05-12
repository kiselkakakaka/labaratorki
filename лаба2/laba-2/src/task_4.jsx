import React, { useState } from 'react';
import './App.css';


function App() {
  const [isAdult, setIsAdult] = useState(false);

  function handleCheckboxChange() {
    setIsAdult(!isAdult);
  }

  return (
    <div>
      <h1>Проверьте свой возраст</h1>
      <label>
        <input
          type="checkbox"
          checked={isAdult}
          onChange={handleCheckboxChange}
        />
        Мне уже 18 лет
      </label>

      {isAdult ? (
        <div>
          <h2>Ура, вам уже есть 18</h2>
          <p>Здесь расположен контент только для взрослых</p>
        </div>
      ) : (
        <div>
          <p>Увы, вам еще нет 18 лет :(</p>
        </div>
      )}
    </div>
  );
}

export default App;