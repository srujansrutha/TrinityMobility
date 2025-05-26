import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import QueryRequest, QueryResponse, SearchRequest, SearchResult
from knowledge_processor import KnowledgeBaseProcessor
from rag_system import SmartCityRAG
from crew_agents import SmartCityAgents
from config import settings

# Setup logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Global variables
knowledge_processor = KnowledgeBaseProcessor()
rag_system = None
crew_agents = None
conversation_history = {}

# Initialize FastAPI app
app = FastAPI(title="Smart City Information Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup"""
    global rag_system, crew_agents
    
    logger.info("Initializing Smart City Assistant...")
    
    try:
        # Load knowledge base from file
        vector_store = knowledge_processor.load_from_file(settings.KNOWLEDGE_BASE_PATH)
        
        # Initialize RAG system
        rag_system = SmartCityRAG(vector_store)
        
        # Initialize CrewAI agents
        crew_agents = SmartCityAgents(rag_system)
        
        logger.info("System initialized successfully!")
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="System not initialized")
        
        result = rag_system.query(request.question)
        
        if request.user_id not in conversation_history:
            conversation_history[request.user_id] = []
        
        conversation_history[request.user_id].append({
            "question": request.question,
            "answer": result["answer"],
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            sources=result["sources"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Query endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query-crew")
async def query_crew_endpoint(request: QueryRequest):
    """Query endpoint using CrewAI multi-agent system"""
    try:
        if not crew_agents:
            raise HTTPException(status_code=503, detail="CrewAI system not initialized")
        
        # First get a RAG result for fallback and confidence scoring
        rag_result = rag_system.query(request.question)
        
        # Try to get result from CrewAI
        crew_result = crew_agents.process_query(request.question)
        
        return {
            "answer": crew_result,
            "confidence": rag_result["confidence"],
            "sources": rag_result["sources"],
            "method": "CrewAI Multi-Agent",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"CrewAI query error: {e}")
        # Return RAG result as fallback
        if rag_system:
            rag_result = rag_system.query(request.question)
            return {
                "answer": rag_result["answer"],
                "confidence": rag_result["confidence"],
                "sources": rag_result["sources"],
                "method": "RAG Fallback",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_endpoint(request: SearchRequest):
    """Vector search endpoint"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="System not initialized")
        
        docs = rag_system.vector_store.similarity_search_with_score(
            request.query, 
            k=request.top_k
        )
        
        results = []
        for doc, score in docs:
            results.append(SearchResult(
                content=doc.page_content,
                metadata=doc.metadata,
                score=float(score)
            ))
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Search endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}")
async def get_conversation_history(user_id: str):
    """Get conversation history for a user"""
    return {
        "user_id": user_id,
        "history": conversation_history.get(user_id, [])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)