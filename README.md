
# Helpdesk Assistant: Gemini-Powered Conversational Dashboard

> Real-time insights for sharper conversations, smarter agents.

## 🧠 Description

**Helpdesk Assistant** is a Gemini-powered conversational dashboard designed to help call center agents perform better through real-time analysis of ongoing calls. By integrating cutting-edge AI capabilities like **sentiment analysis**, **summarization**, **transcription**, and **agent suggestions**, this tool empowers agents with instant feedback and actionable insights—directly from the call.

Built with a responsive **Dash** interface, this Python-based tool seamlessly processes live audio, analyzes it with **Generative AI**, and presents results in an intuitive dashboard. Whether it’s customer mood, key points of a conversation, or intelligent response cues, the dashboard ensures that your agents are always one step ahead.

---

## ✨ Key Features

- 🔍 **Real-time Sentiment Analysis**
- 📝 **Live Summarization of Conversations**
- 💡 **Actionable Suggestions for Agents**
- 📜 **Transcription (as an additional layer)**

---

## 🧰 Tech Stack

- **Backend:** Python, Gemini API, `SpeechRecognizer`, `sqlite`, `threading`
- **Frontend:** Dash by Plotly
- **Other Tools:** OpenAI/Google Gen AI for intelligent text processing

---

## ⚙️ Setup Instructions

1. Clone the repository.
2. Ensure you have Python installed (preferably Python 3.8+).
3. Use a Python-based IDE (we recommend **VS Code** for its rich feature set).
4. Navigate to the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

1. Make sure you have your **API Key** or **`service-account.json`** file ready.
2. Set the environment variable or point to your key file in your code.
3. Run the app using:
   ```bash
   python app.py
   ```

---

## 🖼️ Screenshots

### 🔹 Landing Page
![Landing](images/Landing.png)

### 🔹 Dashboard in Action
![Dashboard](images/Dashboard.png)

---

## 📈 Future Improvements

- Build a **multi-page dashboard** with detailed agent-wise and call-wise analytics.
- Add a **manager dashboard** with historical data, agent performance metrics, and summary views.
- Customize landing pages based on **user role** (Agent vs Manager).
- Introduce **call scoring** and performance badges for motivation and gamification.

## 🤝 Contributions & Feedback

Pull requests and issues are welcome! Let’s make helpdesk analytics smarter together 🚀

---

### 🗒️ Note

This is my first attempt at building with **Dash** and working on the frontend side overall. Some callbacks might feel a bit clunky, but I'm actively improving them. The project is still in its **experimental phase**, and I'm also refining the prompts and AI responses.

This marks the **first release** of a much **bigger vision** I’m working toward. More updates and improvements coming soon!