import streamlit as st
import requests
from config import settings

def main():
    st.set_page_config(
        page_title="Smart City Assistant",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Smart City Information Assistant")
    st.markdown("Your intelligent guide to city services, facilities, and policies")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Settings")
        api_url = st.text_input("API URL", value=f"http://localhost:{settings.API_PORT}")
        use_crew_ai = st.checkbox("Use CrewAI Multi-Agent System", value=False)
        
        st.header("Quick Actions")
        if st.button("Clear History"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about city services, facilities, or policies..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Searching city database..."):
                try:
                    endpoint = "/query-crew" if use_crew_ai else "/query"
                    response = requests.post(
                        f"{api_url}{endpoint}",
                        json={"question": prompt}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "No response received")
                        
                        st.markdown(answer)
                        
                        if "confidence" in data:
                            st.caption(f"Confidence: {data['confidence']:.2%}")
                        if "sources" in data and data["sources"]:
                            st.caption(f"Sources: {', '.join(data['sources'][:3])}")
                        
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer
                        })
                    else:
                        error_msg = f"Error: {response.status_code} - {response.text}"
                        st.error(error_msg)
                        
                except requests.exceptions.ConnectionError:
                    error_msg = "Cannot connect to the API. Please ensure the FastAPI server is running."
                    st.error(error_msg)
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.error(error_msg)
    
    # Example queries
    st.markdown("---")
    st.subheader("Example Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Building Permits"):
            st.rerun()
    
    with col2:
        if st.button("Library Hours"):
            st.rerun()
    
    with col3:
        if st.button("Waste Collection"):
            st.rerun()

if __name__ == "__main__":
    main()
