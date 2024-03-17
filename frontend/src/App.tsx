import React, { useState } from "react";
import "./App.css";

export default function App() {
  const [result, setResult] = useState<string | null>(null);
  const [question, setQuestion] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);

  const handleQuestionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setQuestion(event.target.value);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData();

    if (question) {
      formData.append("question", question);
    }

    if (file) {
      formData.append("file", file);
    }
 
    for (const [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }
    


    fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.result);
      })
      .catch((error) => {
        console.error("Error", error);
      });
  };

  return (
    <div className="appBlock">
      <form onSubmit={handleSubmit} className="form">
        <label className="questionLabel" htmlFor="question">
          Question:
        </label>
        <input
          className="questionInput"
          id="question"
          name="question"
          type="text"
          onChange={handleQuestionChange}
          placeholder="Ask your question here"
        />

        <br />
        <label className="fileLabel" htmlFor="file">
          Upload File:
        </label>

        <input
          type="file"
          id="file"
          name="file"
          accept=".csv, .txt, .docx, .pdf" // Accept multiple file types
          onChange={handleFileChange}
          className="fileInput"
        />
        <br />
        <button className="submitBtn" type="submit" disabled={!file || !question}>
          Submit
        </button>
      </form>
      <p className="resultOutput">Result: {result}</p>
    </div>
  );
}
