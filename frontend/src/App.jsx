import "./App.css";
import logo from "./assets/logo.png";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [topic, setTopic] = useState("");
  const [mode, setMode] = useState("Summary");
  const [difficulty, setDifficulty] = useState("Medium");
  const [responseText, setResponseText] = useState("");
  const [loading, setLoading] = useState(false);
  const [followUp, setFollowUp] = useState("");
  const [followResponse, setFollowResponse] = useState("");
  const [days, setDays] = useState(7);
  const [showAnswers, setShowAnswers] = useState(false);

  

    const handleGenerate = async () => {
  if (!topic) {
    alert("Please enter a topic");
    return;
  }

  setLoading(true);
  setShowAnswers(false);

  try {
    const response = await fetch(
      "https://epistudy.onrender.com/generate",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic,
          mode,
          difficulty,
          days,
        }),
      }
    );

    const data = await response.json();

    setResponseText(data.response);

  } catch (error) {
    setResponseText("Error generating response.");
    console.error(error);

  } finally {
    setLoading(false);
  }
};
const handleFollowUp = async () => {
  if (!followUp) return;

  try {
    const response = await fetch(
      "https://epistudy.onrender.com/followup",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
            body: JSON.stringify({
      question: followUp,
      previous_response: responseText,
    }),
      }
    );
    const downloadResponse = () => {
      const blob = new Blob([responseText], { type: "text/plain" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "response.txt";
      a.click();

      window.URL.revokeObjectURL(url);
    };

    const downloadFollowUp = () => {
      const blob = new Blob([followResponse], { type: "text/plain" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "followup.txt";
      a.click();

      window.URL.revokeObjectURL(url);
    };

    const data = await response.json();

    setFollowResponse(data.response);

  } catch (error) {
    setFollowResponse("Error generating follow-up.");
  }
};
const downloadResponse = () => {
    const element = document.createElement("a");
    const file = new Blob([responseText], { type: "text/plain" });

    element.href = URL.createObjectURL(file);
    element.download = "response.txt";

    document.body.appendChild(element);
    element.click();
  };

  const downloadFollowUp = () => {
    const element = document.createElement("a");
    const file = new Blob([followResponse], { type: "text/plain" });

    element.href = URL.createObjectURL(file);
    element.download = "followup.txt";

    document.body.appendChild(element);
    element.click();
  };
  return (
    <div className="app">
      <div className="header">
        <img
          src={logo}
          alt="EpiStudy Logo"
          className="main-logo"
        />

    </div>

      <div className="main-layout">
        {/* LEFT PANEL */}
        <div className="left-panel">
          <h2 className="section-title">
            Study Controls
          </h2>

          <input
            className="input-box"
            placeholder="Enter a topic..."
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />

          <div className="mode-group">
            <select
              className="select-box"
              value={mode}
              onChange={(e) => setMode(e.target.value)}
            >
              <option>Summary</option>
              <option>Flashcards</option>
              <option>Explain Simply</option>
              <option>Study Plan</option>
              <option>Test Me</option>
            </select>
          </div>

          <div className="mode-group">
            <select
              className="select-box"
              value={difficulty}
              onChange={(e) =>
                setDifficulty(e.target.value)
              }
            >
              <option>Easy</option>
              <option>Medium</option>
              <option>Hard</option>
            </select>
          </div>
              {mode === "Study Plan" && (
              <input
                type="number"
                className="input-box"
                placeholder="Enter number of days"
                value={days}
                onChange={(e) => setDays(e.target.value)}
              />
            )}
          <button
            className="generate-btn"
            onClick={handleGenerate}
          >
            {loading
              ? "Generating..."
              : "Generate Response"}
          </button>
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">
          <h2 className="section-title">
            AI Response
          </h2>
          {mode === "Test Me" && (
            <button
              className="answer-btn"
              onClick={() => setShowAnswers(!showAnswers)}
            >
              {showAnswers ? "Hide Answers" : "Show Answers"}
            </button>
          )}

          <div className="response-text">
            <ReactMarkdown>
              {
                showAnswers
                  ? (responseText || "Your AI-generated notes, flashcards, explanations, tests, and study plans will appear here.")
                  : (responseText || "Your AI-generated notes, flashcards, explanations, tests, and study plans will appear here.")
                      .replace(/## Answers[\s\S]*/i, "")
                      .replace(/Answers:[\s\S]*/i, "")
              }
              </ReactMarkdown>
          </div>
          <button onClick={downloadResponse}>
            Download Response
          </button>
          <div className="follow-up-section">
  <input
    className="input-box"
    placeholder="Ask a follow-up question..."
    value={followUp}
    onChange={(e) => setFollowUp(e.target.value)}
  />

  <button
    className="generate-btn"
    onClick={handleFollowUp}
  >
    Ask Follow-Up
  </button>

  <div className="response-text">
    <ReactMarkdown>
      {followResponse}
    </ReactMarkdown>
  </div>
  <button onClick={downloadFollowUp}>
  Download Follow-Up
</button>
</div>
        </div>
      </div>
    </div>
  );
}