import { useState } from 'react'
import './App.css'
import { use } from 'react';

function App() {
  const [notes, setNotes] = useState([1, 2, 3, 4, 5]);
  const result = notes.map((note, index) => {
    return <li key={index}>{note}</li>;
  });
  return (
    <div>
      
      <ul> {result} </ul>
    </div>
  );
}


export default App
