import subprocess
import sys
from config import settings

if __name__ == "__main__":
    print("🌐 Starting Smart City Frontend...")
    print(f"🌐 Frontend will run on: http://localhost:{settings.STREAMLIT_PORT}")
    
    subprocess.run([
        sys.executable, "-m", "streamlit", 
        "run", "streamlit_app.py",
        "--server.port", str(settings.STREAMLIT_PORT)
    ])