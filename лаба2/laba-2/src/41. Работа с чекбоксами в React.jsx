import { useState } from 'react'
import './App.css'

function App() {
  const [checked, setChecked] = useState(true);
  function handleChange() {
    setChecked(!checked);
  }
  return (
    <div>

      <input type='checkbox' checked={checked} onChange={handleChange} />
    </div>
  );
}

function App1(){
  const [checked, setChecked] = useState(true);
  return (
    <div>

      <input type='checkbox' checked={checked} onChange={() => setChecked(!checked)} />
    </div>
  );
}

function App2(){
  const [checked, setChecked] = useState(true);
  return (
    <div>

      <input type='checkbox' checked={checked} onChange={() => setChecked(!checked)} />
      <p>состояние: {checked ? "отмечен" : "не отмечен"}</p>
    </div>
  );
}

export default App
