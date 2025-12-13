from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.route.auth import router as auth_router
from src.config.settings import settings
from src.database.connection import test_connection,create_db_and_tables

app = FastAPI(title="Penny Finnance Assistant",
              description="Assistant backend",
              version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],                        # allow POST, OPTIONS, etc.
    allow_headers=["*"],                        # allow Authorization header
)

@app.on_event("startup")
async def startup_event():
    """
    Runs tasks when the application starts: testing connection and 
    creating database tables.
    """
    print("🚀 Running startup sequence...")
    
    # 1. Test connection (will exit if connection fails)
    await test_connection()
    
    # 2. Create tables
    # await create_db_and_tables()
    
    print("✅ Startup sequence complete.")

# --- Include Routers ---
app.include_router(auth_router)