import { useState } from 'react'
import './App.css'

function App() {
  const [notes, setNotes] = useState(initNotes);
  const result = notes.map((note) => {
    return (
      <li key={note.id}>
        
        <span>{note.prop1}</span> <span>{note.prop2}</span> <span>{note.prop3}</span>
      </li>
    );
  });
  return (
    <div>
      
      <ul> {result} </ul>
    </div>
  );
}


export default App
