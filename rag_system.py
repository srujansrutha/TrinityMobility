import logging
from typing import Dict, Any
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import settings

logger = logging.getLogger(__name__)

class SmartCityRAG:
    def __init__(self, vector_store, llm_model=None):
        self.vector_store = vector_store
        self.llm = Ollama(
            model=llm_model or settings.OLLAMA_MODEL, 
            temperature=0.1
        )
        self.qa_chain = self._create_qa_chain()
        self.response_cache = {}  # Cache for storing successful responses
        
    def _create_qa_chain(self):
        """Create the QA chain with custom prompt"""
        prompt_template = """
        You are a helpful Smart City Information Assistant. Use the following context to answer the citizen's question about city services, facilities, and policies.

        Context:
        {context}

        Question: {question}

        Instructions:
        - Provide accurate, helpful information based on the context
        - Include specific details like addresses, phone numbers, hours, and fees when available
        - If you don't have enough information, say so clearly
        - Be concise but comprehensive
        - Format important information clearly
        - If the question refers to a sector or zone not explicitly mentioned in the context, explain that the city uses zone designations (A, B, C, D, E) instead of sectors
        - For questions about building permits, include form numbers, required documents, fees, and contact information
        - For questions about business licenses, include application steps, fees, and renewal information
        - For questions about waste collection, include pickup schedules for different zones
        - For questions about library hours, include opening times for different days and location details

        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 7}),  # Increased k for better context
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a query and return response with metadata using pure RAG approach"""
        # Check cache first for identical questions
        if question in self.response_cache:
            logger.info(f"Cache hit for question: {question}")
            return self.response_cache[question]
            
        # Use RAG for all queries
        try:
            # Enhance retrieval by adding common keywords to the query
            enhanced_query = self._enhance_query(question)
            
            # Get result from QA chain
            result = self.qa_chain({"query": enhanced_query})
            
            confidence = self._calculate_confidence(result["source_documents"])
            
            sources = [
                doc.metadata.get("title", "Unknown") 
                for doc in result["source_documents"]
            ]
            
            response = {
                "answer": result["result"],
                "confidence": confidence,
                "sources": sources,
                "source_documents": result["source_documents"]
            }
            
            # Cache high-confidence responses
            if confidence > 0.7:
                self.response_cache[question] = response
                
            return response
            
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return {
                "answer": "I apologize, but I encountered an error processing your request. Please try again.",
                "confidence": 0.0,
                "sources": [],
                "source_documents": []
            }
    
    def _enhance_query(self, question: str) -> str:
        """Enhance query with relevant keywords based on question content"""
        question_lower = question.lower()
        
        if "permit" in question_lower or "building" in question_lower:
            return f"{question} form requirements fees process"
        elif "business" in question_lower or "license" in question_lower:
            return f"{question} application fees requirements renewal"
        elif "garbage" in question_lower or "waste" in question_lower or "collection" in question_lower:
            return f"{question} schedule zones pickup days"
        elif "library" in question_lower or "hours" in question_lower:
            return f"{question} opening times schedule location"
        elif "sector" in question_lower or "zone" in question_lower:
            return f"{question} waste collection schedule zones"
        else:
            return question
    
    def _calculate_confidence(self, source_docs) -> float:
        """Calculate confidence based on document relevance and quantity"""
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
            # Normalize relevance to 0-0.5 range and add to base confidence
            adjusted_confidence = base_confidence + (min(1.0, avg_relevance) * 0.5)
            return min(0.95, adjusted_confidence)
        
        return base_confidence