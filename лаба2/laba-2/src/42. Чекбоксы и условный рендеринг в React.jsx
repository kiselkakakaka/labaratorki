import { useState } from 'react'
import './App.css'

function App() {
  const [checked, setChecked] = useState(true);
  let message;
  if (checked) {
    message = <p>Сообщение 1</p>;
  } else {
    message = <p>Сообщение 2</p>;
  }
  return (
    <div>
      <input type='checkbox' checked={checked} onChange={() => setChecked(!checked)} />
      <div>{message}</div>
    </div>
  );
}


export default App
