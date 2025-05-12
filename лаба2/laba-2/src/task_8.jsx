import React, { useState } from 'react';
import './App.css';


function App() {
  const initDate = { year: 2025, month: 12, day: 31 };
  const [date, setDate] = useState(initDate);

  const getDayOfWeek = () => {
    const { year, month, day } = date;
    const dateObj = new Date(year, month - 1, day);
    const daysOfWeek = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    return daysOfWeek[dateObj.getDay()];
  };

  return (
    <div>
      <h1>Дата из состояния</h1>
      <p>Год: {date.year}</p>
      <p>Месяц: {date.month}</p>
      <p>День: {date.day}</p>
      <p>День недели: {getDayOfWeek()}</p>
    </div>
  );
}

export default App;