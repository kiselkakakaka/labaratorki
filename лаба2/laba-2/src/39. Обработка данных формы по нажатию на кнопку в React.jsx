import { useState } from 'react'
import './App.css'



function App() {
  const[value1, setValue1] = useState(0);
  const[value2, setValue2] = useState(0);
  const[result, setResult] = useState(0);
  return (
    <div>

      <input value={value1} onChange={(event) => setValue1(event.target.value)} />
      <input value={value2} onChange={(event) => setValue2(event.target.value)} />
      <button onClick={() => setResult(Number(value1) + Number(value2))}>btn</button>
      <p>result: {result}</p>
    </div>
  );
}

export default App
