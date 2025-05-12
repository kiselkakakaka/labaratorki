import { useState } from 'react'
import './App.css'



function App() {
  const [value, setValue] = useState("");
  return (
    <div>

      <textarea value={value} onChange={(event) => setValue(event.currentTarget.value)} />
      <p>{value}</p>
    </div>
  );
}

export default App
