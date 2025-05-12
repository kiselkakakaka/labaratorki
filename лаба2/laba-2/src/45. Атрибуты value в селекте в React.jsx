import { useState } from 'react'
import './App.css'

function App() {
  const [value, setValue] = useState("");
  return (
    <div>
      <select value={value} onChange={(event) => setValue(event.target.value)}>

        <option value='1'>text1</option>
        <option value='2'>text2</option>
        <option value='3'>text3</option>
      </select>
      <p>

        {value === "1" && "вы выбрали перый пункт"}
        {value === "2" && "вы выбрали второй пункт"}
        {value === "3" && "вы выбрали третий пункт"}
      </p>
    </div>
  );
}


export default App
