import { useEffect, useState } from "react";
import { fetchLanguages, fetchTopics, fetchLessons } from "./api";

type Language = {
  code: string;
  name: string;
};

type Topic = {
  id: number;
  slug: string;
  title: string;
};

type Lesson = {
  id: number;
  slug: string;
  title: string;
  language: string;
  body: string;
  sms_part_count: number;
};

export default function App() {
  const [languages, setLanguages] = useState<Language[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true);
        setError("");

        const [languageData, topicData, lessonData] = await Promise.all([
          fetchLanguages(),
          fetchTopics(),
          fetchLessons(selectedLanguage),
        ]);

        setLanguages(languageData);
        setTopics(topicData);
        setLessons(lessonData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load data");
      } finally {
        setLoading(false);
      }
    }

    loadInitialData();
  }, [selectedLanguage]);

  return (
    <div className="shell">
      <header className="hero">
        <h1>CARE4ANIMALS</h1>
        <p>Bite-sized animal wellness knowledge for farmers.</p>
      </header>

      {loading && <section className="card"><p>Loading...</p></section>}
      {error && <section className="card"><p>{error}</p></section>}

      {!loading && !error && (
        <>
          <section className="card">
            <h2>Select language</h2>
            <div className="chips">
              {languages.map((language) => (
                <button
                  key={language.code}
                  onClick={() => setSelectedLanguage(language.code)}
                >
                  {language.name}
                </button>
              ))}
            </div>
            <p>Current language: {selectedLanguage}</p>
          </section>

          <section className="card">
            <h2>Topics</h2>
            <ul className="topicList">
              {topics.map((topic) => (
                <li key={topic.id}>{topic.title}</li>
              ))}
            </ul>
          </section>

          <section className="card">
            <h2>Lessons</h2>
            {lessons.map((lesson) => (
              <div key={lesson.id} style={{ marginBottom: "16px" }}>
                <h3>{lesson.title}</h3>
                <p>{lesson.body}</p>
                <small>SMS parts: {lesson.sms_part_count}</small>
              </div>
            ))}
          </section>
        </>
      )}
    </div>
  );
}
