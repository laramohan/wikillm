# ChatGPT Clone based on React.js

A simple chat application using OpenAI's GPT-3.5 Turbo for natural language processing.
This project was created with a boiler plate with [npx create-react-app react-chatgpt).

## Overview
This project is a chat application built with React on the frontend and a Node.js server on the backend. It leverages OpenAI's GPT-3.5 Turbo to provide conversational responses based on user input.

## Features

- **Dynamic Chat History:** Keep track of your conversations with the chat history displayed on the sidebar.
- **User-Friendly Interface:** Intuitive and easy-to-use interface for a seamless chatting experience.
- **GPT-3.5 Turbo Integration:** Leverage the power of OpenAI's GPT-3.5 Turbo for generating natural and context-aware responses.

## Prerequisites

- [Node.js](https://nodejs.org/) installed
- [React](https://reactjs.org/) installed
- OpenAI API key (Sign up at [OpenAI](https://beta.openai.com/signup/) to get your API key)
- Your own API_KEY is avalaible in https://platform.openai.com/account/api-keys

## Setup

### Backend (Node.js Server)
1. Clone the repository:
```sh
git clone https://github.com/your-username/chatgpt-clone.git
```
2. Navigate to the server directory:
```bash
cd chatgpt-clone/server
```
3. Install dependencies:
```bash
npm install
```
4. Create a .env file in the server directory and add your OpenAI API key:
```env
API_KEY=your-openai-api-key
```
5. Start the server:
```bash
npm run start:backend
```
The server will run on http://localhost:8000.

### Frontend (React App)
1. Navigate to the client directory:
```bash
cd chatgpt-clone/
```
2. Install dependencies:
```bash
npm install
```
3. Start the React app:
```bash
npm run start:frontend
```

## Usage

1. Visit http://localhost:3000 in your browser.
2. Interact with the chat application by creating new chats, selecting previous chats, and exploring the dynamic chat history.

## Issues and Contributions
You need to have payment plan to avoid:
```javascript
error: "You exceeded your current quota, please check your plan and billing details."
```
Also there is a list of toDo in [App.js](./src/App.js)
If you encounter any more issues or have suggestions for improvement, feel free to open an issue or create a pull request.

## Thanks for reading!
:heart::heart::heart:
