import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def test_connection():
    # 1. Get the URL
    database_url = os.getenv("CONNECTION_STRING")
    
    if not database_url:
        print("❌ Error: DATABASE_URL not found in .env file.")
        return

    # 2. Fix the protocol for SQLAlchemy + Asyncpg
    # Supabase copies "postgres://" by default, but SQLAlchemy needs "postgresql+asyncpg://"
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    
    # If the URL doesn't specify a driver, ensure it has asyncpg
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    print(f"Attempting to connect to host: {database_url.split('@')[1].split('/')[0]}...")

    # 3. Create Engine
    try:
        engine = create_async_engine(database_url, echo=False)
        
        # 4. Try to Connect and Run a Query
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT version();"))
            version = result.scalar()
            
            print("\n✅ CONNECTION SUCCESSFUL!")
            print("------------------------------------------------")
            print(f"Database Version: {version}")
            print("------------------------------------------------")
            
        await engine.dispose()

    except Exception as e:
        print("\n❌ CONNECTION FAILED")
        print("------------------------------------------------")
        print(f"Error: {e}")
        print("------------------------------------------------")
        print("Troubleshooting tips:")
        print("1. Check if your IP is allowed in Supabase (Network Restrictions).")
        print("2. Verify the password is correct (special characters must be URL encoded).")
        print("3. Ensure you are using port 5432 (Direct) or 6543 (Pooler).")

if __name__ == "__main__":
    asyncio.run(test_connection())