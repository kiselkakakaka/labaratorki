import { useState } from 'react'
import './App.css'

function App() {
  const [value, setValue] = useState("");
  function handleChange(event) {
    setValue(event.target.value);
  }
  return (
    <div>

      <select value={value} onChange={handleChange}>

        <option>text1</option>
        <option>text2</option>
        <option>text3</option>
        <option>text4</option>
      </select>
      <p> ваш выбор: {value}</p>
    </div>
  );
}


export default App
