import React, { useState } from 'react';
import './App.css';


function App() {
  const initDate = { year: 2025, month: 12, day: 31 };
  const [date, setDate] = useState(initDate);
  
  const [items, setItems] = useState([]);
  
  const getDayOfWeek = () => {
    const { year, month, day } = date;
    const dateObj = new Date(year, month - 1, day);
    const daysOfWeek = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    return daysOfWeek[dateObj.getDay()];
  };

  const handleInputChange = (field, event) => {
    const value = event.target.value;
    setDate(prevDate => ({
      ...prevDate,
      [field]: Number(value) 
    }));
  };

  const addItem = () => {
    const newItem = `Элемент ${items.length + 1}`; 
    setItems(prevItems => [...prevItems, newItem]); 
  };

  return (
    <div>
      <h1>Редактирование даты</h1>
      <div>
        <label>
          Год:
          <input
            type="number"
            value={date.year}
            onChange={(event) => handleInputChange('year', event)}
          />
        </label>
      </div>
      <div>
        <label>
          Месяц:
          <input
            type="number"
            value={date.month}
            onChange={(event) => handleInputChange('month', event)}
          />
        </label>
      </div>
      <div>
        <label>
          День:
          <input
            type="number"
            value={date.day}
            onChange={(event) => handleInputChange('day', event)}
          />
        </label>
      </div>
      <h2>Дата:</h2>
      <p>Год: {date.year}</p>
      <p>Месяц: {date.month}</p>
      <p>День: {date.day}</p>
      <p>День недели: {getDayOfWeek()}</p>

      <h2>Список элементов</h2>
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