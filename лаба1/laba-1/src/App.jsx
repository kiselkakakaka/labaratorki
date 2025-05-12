import { useState } from "react";

function App() {
  const [value, setValue] = useState("");

  return (
    <div>
      <h1>Лабораторная работа №1</h1>
      <input
        type="text"
        placeholder="Введите текст"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <p>Вы ввели: {value}</p>
    </div>
  );
}

export default App;
