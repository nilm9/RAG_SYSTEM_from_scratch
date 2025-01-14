from sqlalchemy import text
from rag_project.adapters.database.connection import engine
from rag_project.adapters.database.models import Base
def init_db():
    """
    Initialize the database schema by creating tables and extensions.
    """
    try:
        with engine.connect() as connection:
            # Enable pgvector extension
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            print(" pgvector extension enabled or already exists.")

        # Create all tables defined in models
        Base.metadata.create_all(engine)
        print(" Database schema created successfully.")

    except Exception as e:
        print(f" Failed to initialize database schema: {e}")


if __name__ == '__main__':
    init_db()
