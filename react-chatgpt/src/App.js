import React, { useState, useEffect } from "react";
import user from "./duck.jpeg";
import assistant from "./chat.png";
import Deleteicon from "./delete-bin.png";

const completions_url = "http://104.255.9.187:11508/respond";

//toDo: localstorage, onKey press Enter, fix bug to setValue("") after submit in the input.
const App = () => {
  const [value, setValue] = useState("");
  const [message, setMessage] = useState(null);
  const [previousChats, setPreviousChats] = useState([]);
  const [currentTitle, setCurrentTitle] = useState("");

  const createNewChat = () => {
    setMessage("");
    setValue("");
    setCurrentTitle(null);
  };

  const handleClick = (uniqueTitle) => {
    setCurrentTitle(uniqueTitle);
    setMessage("");
    setValue("");
  };

  const getMessages = async () => {
    const options = {
      method: "POST",
      body: JSON.stringify({
        content: value,
        role: "user",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    };
    try {
      const response = await fetch(
        completions_url,
        options
      );
      const data = await response.json();

      if (
        data.choices &&
        Array.isArray(data.choices) &&
        data.choices.length > 0
      ) {
        setMessage(data.choices[0].message);
      } else {
        console.error(data);
        setMessage("The API is not answering!");
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setMessage(
        `An error occurred while communicating with the server: ${error.message}`
      );
    }
  };
  const handleDelete = (deleteTitle) => {
    const newChats = previousChats.filter((chat) => chat.title !== deleteTitle);
    setPreviousChats(newChats);
  };
  // const handleKeyPress = (e) => {
  //   if (e.key === "Enter") {
  //     getMessages();
  //   }
  // };

  useEffect(() => {
    if (!currentTitle && value && message) {
      setCurrentTitle(value);
    }

    if (currentTitle && value && message) {
      setPreviousChats((prevChats) => [
        ...prevChats,
        { title: currentTitle, role: "user", content: value },
        { title: currentTitle, role: message.role, content: message.content },
      ]);
    } // eslint-disable-next-line
  }, [message, currentTitle]);

  const currentChat = previousChats.filter(
    (previousChat) => previousChat.title === currentTitle
  );

  const uniqueTitles = Array.from(
    new Set(previousChats.map((previousChats) => previousChats.title))
  );

  return (
    <div className="app">
      <section className="side-bar">
        <button onClick={createNewChat}>+ New chat</button>
        <ul className="history">
          {uniqueTitles?.map((uniqueTitle, index) => (
            <li key={index} onClick={() => handleClick(uniqueTitle)}>
              {uniqueTitle}
              <img
                alt=""
                src={Deleteicon}
                role="button"
                onClick={() => handleDelete(uniqueTitle)}
              />
            </li>
          ))}
        </ul>
        {/* <nav>
          <p>Made by a cyborg called Laura</p>
        </nav> */}
      </section>
      <section className="main">
        {!currentTitle && <h1>WikiLLM</h1>}
        <ul className="feed">
          {currentChat?.map((chatMessage, index) => (
            <li key={index}>
              <p className="role">
                {chatMessage.role === "user" ? (
                  <img alt="" src={user} />
                ) : (
                  <img alt="" src={assistant} />
                )}
              </p>
              <p>{chatMessage.content}</p>
            </li>
          ))}
        </ul>
        <div className="bottom-section">
          <div className="input-container">
            <input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              // onKeyDown={handleKeyPress}
            />
            <div id="submit" onClick={getMessages}>
              ➢
            </div>
          </div>
          <p className="info">
            Free Research Preview. ChatGPT may produce inaccurate information
            about people, places, or facts. ChatGPT May 24 Version
          </p>
        </div>
      </section>
    </div>
  );
};

export default App;
