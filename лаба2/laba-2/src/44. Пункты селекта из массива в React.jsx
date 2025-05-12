import { useState } from 'react'
import './App.css'

function App() {
  const text = ["text1", "text2", "text3", "text4"];
  const [value, setValue] = useState("");
  const options = texts.map((text, index) => {
    return <option key={index}>{text}</option>;
  });
  return (
    <div>
      <select value={value} onChange={(event) => setValue(event.target.value)}>
        {options}
      </select>
      <p> ваш выбор: {value} </p>
    </div>
  );
}


export default App
