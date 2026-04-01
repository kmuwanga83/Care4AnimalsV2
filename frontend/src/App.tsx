const topics = [
  "Disease Management",
  "Vaccination",
  "Animal Welfare",
  "Feeding & Nutrition",
  "Transport & Handling",
];

export default function App() {
  return (
    <div className="shell">
      <header className="hero">
        <h1>CARE4ANIMALS</h1>
        <p>Bite-sized animal wellness knowledge for farmers.</p>
      </header>

      <section className="card">
        <h2>Select language</h2>
        <div className="chips">
          <button>English</button>
          <button>Luganda</button>
          <button>Swahili</button>
        </div>
      </section>

      <section className="card">
        <h2>Topics</h2>
        <ul className="topicList">
          {topics.map((topic) => (
            <li key={topic}>{topic}</li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Sample lesson</h2>
        <h3>Recognising Sick Animals</h3>
        <p>Check appetite, breathing, wounds, walking, and body condition every day.</p>
      </section>
    </div>
  );
}
