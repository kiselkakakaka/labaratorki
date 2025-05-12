import './App.css'

function App(){
  const [value1, setValue1] = useState(0);
  const [value2, setValue2] = useState(0);
  function handleChange1(event) {
    setValue1(+event.target.value);
  }
  function handleChange2(event) {
    setValue2(+event.target.value);
  }
  return (
    <div>

      <input value={value1} onChange={handleChange1} />
      <input value={value2} onChange={handleChange2} />
      <p>result: {value1 + value2}</p>
    </div>
  );
}

export default App
