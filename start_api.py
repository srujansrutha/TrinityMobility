import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 Starting Smart City API Server...")
    print(f"📡 API will run on: http://localhost:{settings.API_PORT}")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=settings.API_PORT,
        reload=False
    )