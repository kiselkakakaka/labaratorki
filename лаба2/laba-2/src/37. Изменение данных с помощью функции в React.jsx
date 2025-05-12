import './App.css'

function square(num) {
  return num ** 2;
}
function App(){
  const [value, setValue] = useState(0);
  function handleChange(event) {
    setValue(event.target.value);
  }
  return(
    <div>

      <input value={value} onChange={handleChange} /> <p>{square(value)}</p>
    </div>
  )
}

export default App
