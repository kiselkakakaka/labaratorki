import React, { useState } from 'react';
import './App.css';


function App() {
    const [selectedCity, setSelectedCity] = useState('');

    const cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань'];

    function handleCityChange(event) {
        setSelectedCity(event.target.value);
    }

    return (
        <div>
            <h1>Выберите город</h1>
            <select value={selectedCity} onChange={handleCityChange}>
                <option value="">Выберите город</option>
                {cities.map((city, index) => (
                    <option key={index} value={city}>
                        {city}
                    </option>
                ))}
            </select>

            <p>Выбранный город: {selectedCity || 'Не выбран'}</p>
        </div>
    );
}

export default App;
    