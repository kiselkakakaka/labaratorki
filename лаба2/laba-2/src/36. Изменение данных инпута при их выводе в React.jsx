import './App.css'

function App() {
  const [value, setValue] = useState(0);
  function handleChange(event){
    setValue(event.target.value);
  }
  return(
    <div>

      <input value={value} onChange={handleChange} />
      <p>{value ** 2}</p>
    </div>
  )
}

export default App
