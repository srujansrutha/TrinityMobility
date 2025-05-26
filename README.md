# Smart City Information Assistant

A comprehensive assistant for citizens to query information about city services, policies, and facilities.

## Features

- FastAPI backend with RAG system
- Streamlit frontend interface
- Multi-agent system using CrewAI
- Vector search using FAISS
- Local LLM deployment with Ollama

## Technical Implementation

### RAG System
The system uses a pure Retrieval-Augmented Generation (RAG) approach that:
- Enhances queries with relevant keywords based on question content
- Implements dynamic response caching for frequently asked questions
- Uses a sophisticated confidence scoring algorithm
- Provides source attribution for transparency

### Multi-Agent System
The CrewAI implementation includes specialized agents:
- Information Retriever Agent
- Policy Expert Agent
- Service Coordinator Agent

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure Ollama is running with the mistral:7b model:
   ```
   ollama pull mistral:7b
   ```

3. Start the application (two-step process):

   **Step 1:** Start the API server
   ```
   python start_api.py
   ```

   **Step 2:** In a new terminal, start the Streamlit frontend
   ```
   python start_streamlit.py
   ```

4. Access the application:
   - API: http://localhost:8000
   - Frontend: http://localhost:8501

## Usage

- Ask questions about city services, facilities, and policies
- Toggle between standard RAG and CrewAI multi-agent system
- View conversation history
- Try example queries

## Example Queries

- "How do I apply for a building permit?"
- "What are the library hours near downtown?"
- "When is garbage collection in Zone A?"
- "What's the process for starting a small business?"
- "What are the noise ordinance rules?"