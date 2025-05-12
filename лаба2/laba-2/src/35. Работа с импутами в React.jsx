import './App.css'


function App() {
  const [value, setValue] = useState("");
  return(
    <div>
      <input value ={value} onChange={(event) => setValue(event.target.value)} />
      <p>text: {value}</p>
    </div>
  );
}

export default App
