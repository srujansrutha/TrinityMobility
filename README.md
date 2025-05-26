Demo: https://drive.google.com/file/d/1CGFy-P2yaRQ1-cKu9u4H8kpatEzdEUdT/view?usp=drivesdk
# 🌆 Smart City Information Assistant

A comprehensive AI-powered assistant that helps citizens access information about city services, policies, transportation, and public facilities using advanced Retrieval-Augmented Generation (RAG) and a multi-agent system architecture.

---

## 🚀 Features

- **🔍 Advanced RAG System** – Combines semantic search with LLM generation for accurate answers.
- **🤖 Multi-Agent Architecture** – Uses CrewAI to coordinate specialized agents for deeper reasoning.
- **📚 Vector Search with FAISS** – Fast and efficient similarity search powered by locally stored embeddings.
- **⚡ Response Caching** – Reduces latency by reusing high-confidence answers.
- **📏 Confidence Scoring** – Evaluates reliability of answers based on vector similarity.
- **🔗 Source Attribution** – Transparently cites retrieved source content.
- **💬 User-Friendly Interface** – Clean Streamlit-based frontend with chat interface and query history.

---

## 🏗️ Architecture Overview

### Core Components
- **FastAPI Backend** – Handles API requests (`/query`, `/search`, `/health`).
- **LangChain-based RAG System** – Retrieves relevant chunks and generates LLM responses.
- **CrewAI Multi-Agent System** – Specialized agents for information retrieval, policy reasoning, and service coordination.
- **FAISS Vector Store** – Stores embedded documents for efficient similarity search.
- **Streamlit Frontend** – Interactive user interface for query input and result display.

### Multi-Agent Workflow

| Agent                    | Responsibility                                      |
|-------------------------|------------------------------------------------------|
| 🧠 Information Retriever | Extracts relevant chunks from knowledge base         |
| 🧑‍⚖️ Policy Expert        | Interprets regulations and compliance guidelines     |
| 👩‍💼 Service Coordinator  | Summarizes findings into clear user responses        |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- [Ollama](https://ollama.com) installed locally

### 1. Clone the Repository
```bash
git clone https://github.com/srujansrutha/yooooo.git
cd yooooo
2. Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Pull Required Models using Ollama
bash
Copy
Edit
ollama pull mistral
ollama pull nomic-embed-text
▶️ Running the Application
Start Backend API (FastAPI)
bash
Copy
Edit
uvicorn app.main:app --reload
Start Frontend (Streamlit)
bash
Copy
Edit
streamlit run ui/ui.py
Access it at: http://localhost:8501

✅ Example Queries
"How do I apply for a building permit?"

"What are the library hours near downtown?"

"When is garbage collection in Sector 5?"

"What’s the process for starting a small business?"

📁 Project Structure
bash
Copy
Edit
smart_city_assistant/
├── app/
│   ├── main.py               # FastAPI backend
│   ├── vector_store.py       # Embedding + FAISS logic
│   ├── crew.py               # CrewAI orchestration
│   └── config/
│       ├── agents.yaml       # Agent definitions
│       └── tasks.yaml        # Task descriptions
├── ui/
│   └── ui.py                 # Streamlit frontend
├── requirements.txt
└── README.md
📈 Future Enhancements
Automatic knowledge base updating

Mobile-friendly frontend design

Personalized suggestions based on user history

Admin dashboard with analytics


🛠 Built with 💙 using Ollama, LangChain, FAISS, CrewAI, FastAPI, and Streamlit
