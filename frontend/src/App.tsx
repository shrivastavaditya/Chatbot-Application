import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopyright, faArrowCircleRight } from '@fortawesome/free-solid-svg-icons';
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState<{ sender: string; message: string }[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);

  useEffect(() => {
    // Scroll to bottom of chatbox when messages change
    const chatbox = document.getElementById("chatbox");
    if (chatbox) {
      chatbox.scrollTop = chatbox.scrollHeight;
    }
  }, [messages]);

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
    sendMessage();
  };

  const sendMessage = () => {
    const formData = new FormData();

    if (question) {
      formData.append("question", question);
      setQuestion(""); // Clear the question input after submitting

      // Append the user's question to the chatbox
      const chatbox = document.getElementById("chatbox");
      if (chatbox) {
        const userMessage = document.createElement("div");
        userMessage.textContent = question;
        userMessage.classList.add("userMessage");
        chatbox.appendChild(userMessage);
        chatbox.scrollTop = chatbox.scrollHeight;
      }
    }
    if (file) {
      formData.append("file", file);
    }

    fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        const chatbox = document.getElementById("chatbox");
        if (chatbox) {
          const ansbox = document.createElement("div");
          ansbox.textContent = data.result;
          ansbox.classList.add("botMessage");
          chatbox.appendChild(ansbox);
          chatbox.scrollTop = chatbox.scrollHeight;
        }
      })
      .catch((error) => {
        console.error("Error", error);
      });
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent form submission
      sendMessage();
    }
  };

  return (
    <div className="appBlock">

      <h1 className="heading">FileBot: LLM ChatBot</h1>

      <form onSubmit={handleSubmit} className="form">
        <input
          type="file"
          id="file"
          name="file"
          accept=".csv, .txt, .docx, .pdf"
          onChange={handleFileChange}
          className="fileInput"
        />
        
       
        <div className="chatbox" id="chatbox">
          <div className="botMessage">Hi!!!</div>
          <div className="botMessage">Please upload your .txt, .pdf, .docx or .csv file to be preprocessed and ask the question further!!</div>
        </div>
        <div className="questionContainer" id="questionContainer">
              <input
                className="questionInput"
                id="question"
                name="question"
                type="text"
                value={question}
                onChange={handleQuestionChange}
                onKeyPress={handleKeyPress} // Handle keypress event
                placeholder="Ask your question here"
              />
              <button className="submitBtn" type="submit" disabled={!file || !question}>
              <FontAwesomeIcon icon={faArrowCircleRight} />
              </button>
            </div>
      </form>
    </div>
  );
}
