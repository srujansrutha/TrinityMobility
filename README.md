## Smart City Information Assistant ##

A comprehensive AI-powered assistant that helps citizens access information about city services, policies, and facilities using advanced RAG (Retrieval-Augmented Generation) and multi-agent systems.

🌟 Features
Advanced RAG System: Pure retrieval-augmented generation with dynamic query enhancement

Multi-Agent Architecture: Specialized agents for different aspects of city information

Vector Search: FAISS-powered similarity search for efficient information retrieval

Response Caching: Automatic caching of high-confidence responses

Confidence Scoring: Sophisticated algorithm to assess answer reliability

Source Attribution: Transparent citation of information sources

User-Friendly Interface: Clean Streamlit frontend with chat history

🏗️ Architecture
Core Components
FastAPI Backend: Handles API requests and serves data

RAG System: Retrieves relevant information from the knowledge base

CrewAI Multi-Agent System: Provides enhanced responses through specialized agents

FAISS Vector Database: Stores and retrieves document embeddings efficiently

Streamlit Frontend: User interface for interacting with the system

Multi-Agent System
The system implements three specialized agents:

Information Retriever Agent: Focuses on finding accurate factual information

Policy Expert Agent: Specializes in city regulations and compliance requirements

Service Coordinator Agent: Helps citizens navigate procedures and services

🚀 Installation
Prerequisites
Python 3.9+

Ollama for local LLM deployment

Setup
Clone the repository:

git clone https://github.com/srujansrutha/yooooo.git
cd yooooo

Copy
bash
Install dependencies:

pip install -r requirements.txt

Copy
bash
Pull the Mistral 7B model using Ollama:

ollama pull mistral:7b

Copy
bash
Create a .env file (optional):

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b
API_PORT=8000
STREAMLIT_PORT=8501

Copy
🏃‍♂️ Running the Application
Step 1: Start the API Server
python start_api.py

Copy
bash
The first run will create the vector database, which may take a few minutes. Subsequent runs will load the existing database.

Step 2: Start the Frontend
In a new terminal:

python start_streamlit.py

Copy
bash
Step 3: Access the Application
Open your browser and go to:

Frontend: http://localhost:8501

API Documentation: http://localhost:8000/docs

💡 Usage
Type your question in the chat input

Toggle "Use CrewAI Multi-Agent System" for complex queries

View confidence scores and sources for each answer

Clear history using the sidebar button

📊 Technical Details
RAG Implementation
The RAG system uses a pure retrieval-augmented generation approach:

def query(self, question: str) -> Dict[str, Any]:
    # Enhance retrieval by adding common keywords to the query
    enhanced_query = self._enhance_query(question)
    
    # Get result from QA chain
    result = self.qa_chain({"query": enhanced_query})
    
    confidence = self._calculate_confidence(result["source_documents"])
    
    sources = [
        doc.metadata.get("title", "Unknown") 
        for doc in result["source_documents"]
    ]
    
    return {
        "answer": result["result"],
        "confidence": confidence,
        "sources": sources,
        "source_documents": result["source_documents"]
    }

Copy
python
Confidence Calculation
Confidence is calculated based on document relevance and quantity:

def _calculate_confidence(self, source_docs) -> float:
    if not source_docs:
        return 0.0
        
    # Calculate base confidence from number of sources
    base_confidence = min(0.9, 0.5 + (len(source_docs) * 0.1))
    
    # Adjust confidence based on relevance scores if available
    relevance_scores = []
    for doc in source_docs:
        if hasattr(doc, 'metadata') and 'score' in doc.metadata:
            relevance_scores.append(doc.metadata['score'])
    
    # If we have relevance scores, factor them in
    if relevance_scores:
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        adjusted_confidence = base_confidence + (min(1.0, avg_relevance) * 0.5)
        return min(0.95, adjusted_confidence)
    
    return base_confidence

Copy
python
Multi-Agent System
The CrewAI implementation uses specialized agents with sequential task processing:

crew = Crew(
    agents=[info_agent, policy_agent, coordinator_agent],
    tasks=[search_task, policy_task, coordination_task],
    verbose=True,
    process={"name": "sequential"}
)

Copy
python
📁 Project Structure
smart-city-assistant/
├── config.py                # Configuration settings
├── crew_agents.py           # Multi-agent system implementation
├── knowledge_processor.py   # Vector database management
├── knowledge.json           # City information knowledge base
├── main.py                  # FastAPI backend
├── models.py                # Data models
├── rag_system.py            # RAG implementation
├── requirements.txt         # Dependencies
├── start_api.py             # API server startup script
├── start_streamlit.py       # Frontend startup script
└── streamlit_app.py         # Streamlit frontend

Copy
📋 Example Queries
"How do I apply for a building permit?"

"What are the library hours near downtown?"

"When is garbage collection in Zone A?"

"What's the process for starting a small business?"

"What are the noise ordinance rules?"

🔧 Customization
Adding New Knowledge
To expand the knowledge base, add new entries to knowledge.json and delete the faiss_index directory to rebuild the vector database.

Modifying Agent Behavior
Agent roles and behaviors can be customized in crew_agents.py.

