import { useState } from 'react'
import './App.css'

function App() {
  const [value, setValue] = useState(1);
  function changeHandler(event) {
    setValue(event.target.value);
  }
  return (

    <input
      type='radio'
      label='radio'
      value='1'
      checked = {value === "1" ? true : false}
      onChange={changeHandler}
    />

  );
}


export default App
