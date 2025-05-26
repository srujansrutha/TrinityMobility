import json
import logging
import os
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

logger = logging.getLogger(__name__)

class KnowledgeBaseProcessor:
    def __init__(self):
        self.documents: List[Document] = []
        self.vector_store = None
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.index_path = "faiss_index"
    
    def load_from_file(self, file_path: str):
        """Load knowledge base from JSON file"""
        # Try to load existing vector store first
        if os.path.exists(self.index_path):
            try:
                logger.info(f"Loading existing vector store from {self.index_path}")
                self.vector_store = FAISS.load_local(self.index_path, self.embeddings)
                logger.info("Vector store loaded successfully")
                return self.vector_store
            except Exception as e:
                logger.warning(f"Failed to load existing vector store: {e}")
                logger.info("Creating new vector store...")
        
        # If no existing vector store, create a new one
        with open(file_path, 'r') as f:
            knowledge_data = json.load(f)
        return self.load_knowledge_base(knowledge_data)
        
    def load_knowledge_base(self, knowledge_data: Dict):
        """Process the provided JSON knowledge base"""
        logger.info("Loading knowledge base...")
        
        for category, items in knowledge_data.get("knowledge_base", {}).items():
            if isinstance(items, list):
                for item in items:
                    content = f"Title: {item.get('title', '')}\n"
                    content += f"Category: {item.get('category', '')}\n"
                    content += f"Content: {item.get('content', '')}\n"
                    
                    for key, value in item.items():
                        if key not in ['title', 'category', 'content', 'id']:
                            content += f"{key.title()}: {value}\n"
                    
                    doc = Document(
                        page_content=content,
                        metadata={
                            "id": item.get("id", ""),
                            "title": item.get("title", ""),
                            "category": item.get("category", ""),
                            "source_category": category
                        }
                    )
                    self.documents.append(doc)
        
        logger.info(f"Loaded {len(self.documents)} documents")
        return self.chunk_documents()
    
    def chunk_documents(self):
        """Split documents into chunks for better retrieval"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        chunked_docs = text_splitter.split_documents(self.documents)
        logger.info(f"Created {len(chunked_docs)} chunks")
        
        self.vector_store = FAISS.from_documents(chunked_docs, self.embeddings)
        logger.info("Vector store created successfully")
        
        # Save the vector store to disk
        self.vector_store.save_local(self.index_path)
        logger.info(f"Vector store saved to {self.index_path}")
        
        return self.vector_store