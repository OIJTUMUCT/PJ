import asyncpg
import asyncio
import os

async def init_db():
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

    await conn.execute("""
    CREATE TABLE IF NOT EXISTS user_actions (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        action TEXT NOT NULL,
        timestamp TIMESTAMPTZ DEFAULT NOW()
    );
    """)
    await conn.close()

if __name__ == '__main__':
    asyncio.run(init_db())