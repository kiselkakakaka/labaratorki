import { useState } from 'react'
import './App.css'
import { use } from 'react';

function App() {
  const [notes, setNotes] = useState([1, 2, 3]);
  function changeHandler(index, event) {
    setNotes([...notes.slice(0, index),  event.target.value, ...notes.slice(index +1)]);
  }
  return(
    <div>

      <input value={notes[0]} onChange={(event) => changeHandler(0, event)} />
      <input value={notes[1]} onChange={(event) => changeHandler(1, event)} />
      <input value={notes[2]} onChange={(event) => changeHandler(2, event)} />
    {getSum(notes)}
    </div>
  );
}

function App() {
  const [notes, setNotes] = useState([1, 2, 3]);
  function changeHandler(index, event) {
    setNotes([...notes.slice(0, index), event.target.value, ...notes.slice(index + 1)]);
  }
  const result = notes.map((note, index) =>{
    return <input key={index} value={note} onChange={(event) => changeHandler(index, event)} />;
  });
  return(
    <div>
      
      {result} {getSum(notes)}
    </div>
  );
}

export default App
