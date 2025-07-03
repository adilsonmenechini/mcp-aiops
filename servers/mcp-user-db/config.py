import aiosqlite

async def get_conn():
    """Cria uma conexão assíncrona com o banco de dados."""
    db = await aiosqlite.connect("users.db")
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """
    )
    await db.commit()
    return db
