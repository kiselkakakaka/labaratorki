import { useState } from 'react'
import './App.css'
function App() {
  const [value, setValue] = useState("text");
  return (
    <div>

      <input defaultValue={value} />
    </div>
  );
}

function App(){
  const [checked, setChecked] = useState(true);
  return (
    <div>

      <input type='checkbox' defaultChecked={checked} />
    </div>
  );
}

export default App
