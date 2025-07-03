from config import get_conn
import sqlite3
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

mcp = FastMCP()

@mcp.tool()
async def create_user(
    name: str = Field(description="User's name"),
    email: str = Field(description="User's email"),
    ctx: Context = Field(description="Request context"),
    ) -> dict:
    """Creates a new user in the SQLite database.
    
    Args:
        name (str): The user's name.
        email (str): The user's email.

    Returns:
        dict: A dictionary containing the status and message of the operation."""
    conn = await get_conn()
    try:
        await conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        await conn.commit()
        cursor = await conn.execute("SELECT last_insert_rowid()")
        (await cursor.fetchone())[0]
        return {"status": "success", "message": f"Hi {name}, Successfully created!"}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": str(e)}
    finally:
        await conn.close()

@mcp.tool()
async def list_users(ctx: Context) -> dict:
    """Lists all registered users in the database.
    
    Args:
        None

    Returns:
        dict: A dictionary containing the list of users with status and message."""
    conn = await get_conn()
    try:
        cursor = await conn.execute("SELECT id, name, email FROM users")
        users = await cursor.fetchall()
        return {"status": "success", "message": [{"id": u[0], "name": u[1], "email": u[2]} for u in users]}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": str(e)}
    finally:
        await conn.close()


@mcp.tool()
async def get_user_by_email(
    user_email: str = Field(description="User's email"),
    ctx: Context = Field(description="Request context"),
    ) -> dict:
    """Retrieves a specific user by email.

    Args:
        user_email (str): The user's email.

    Returns:
        dict: A dictionary containing the status and message of the operation."""
    conn = await get_conn()
    try:
        cursor = await conn.execute("SELECT id, name, email FROM users WHERE email = ?", (user_email,))
        user = await cursor.fetchone()
        if user:
            return {"status": "success", "message": f"Hi {user[1]}! How can I help you today?"}
        else:
            return {"status": "error", "message": f"User with email {user_email} not found."}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": str(e)}
    finally:
        await conn.close()


mcp_tools_users = (
    create_user,
    list_users,
    get_user_by_email,
)