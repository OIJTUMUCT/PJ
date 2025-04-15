import requests
import asyncpg
import os

async def log_user_action(user_id: int, action: str):
    print(f"[DEBUG] Trying to log action: {user_id=} {action=}")
    try:
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        print("[DEBUG] Connected to DB")

        await conn.execute(
            "INSERT INTO user_actions (user_id, action) VALUES ($1, $2)",
            user_id, action
        )
        print("[DEBUG] Action logged")
        await conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to log action: {e}")