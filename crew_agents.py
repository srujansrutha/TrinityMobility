import logging
from crewai import Agent, Task, Crew
from langchain.tools import Tool

logger = logging.getLogger(__name__)

class SmartCityAgents:
    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.search_tool = Tool(
            name="city_search",
            description="Search the city knowledge base for information",
            func=lambda query: self.rag_system.query(query)["answer"]
        )
        
    def create_agents(self):
        """Create specialized agents for different city services"""
        
        info_agent = Agent(
            role='Information Retriever',
            goal='Find accurate information from the city database',
            backstory='Expert at searching and retrieving city service information',
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False
        )
        
        policy_agent = Agent(
            role='Policy Expert',
            goal='Provide guidance on city policies and regulations',
            backstory='Specializes in city ordinances, regulations, and compliance requirements',
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False
        )
        
        coordinator_agent = Agent(
            role='Service Coordinator',
            goal='Help citizens navigate city services and procedures',
            backstory='Expert at guiding citizens through city processes and connecting them with the right services',
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False
        )
        
        return info_agent, policy_agent, coordinator_agent
    
    def process_query(self, question: str) -> str:
        """Process query using multi-agent system"""
        # First try to get a direct answer from the RAG system
        direct_answer = self.rag_system.query(question)
        
        # If we have a high-confidence direct answer, use it
        if direct_answer["confidence"] >= 0.7:
            return direct_answer["answer"]
            
        try:
            # Create agents and tasks
            info_agent, policy_agent, coordinator_agent = self.create_agents()
            
            search_task = Task(
                description=f"Search for information about: {question}",
                agent=info_agent,
                expected_output="Detailed factual information about the query"
            )
            
            policy_task = Task(
                description=f"Check if there are any policy or regulatory aspects to: {question}",
                agent=policy_agent,
                expected_output="Policy and regulatory information related to the query"
            )
            
            coordination_task = Task(
                description=f"Provide comprehensive guidance for: {question}",
                agent=coordinator_agent,
                expected_output="Step-by-step guidance addressing the user's question"
            )
            
            # Create and run the crew
            crew = Crew(
                agents=[info_agent, policy_agent, coordinator_agent],
                tasks=[search_task, policy_task, coordination_task],
                verbose=True,
                process={"name": "sequential"}  # Use sequential processing to avoid delegation issues
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            logger.error(f"CrewAI processing error: {e}")
            # Return the direct answer from RAG system if CrewAI fails
            return direct_answer["answer"]