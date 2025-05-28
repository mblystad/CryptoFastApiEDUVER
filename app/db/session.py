from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # We'll define this in Step 4

# Create the SQLAlchemy engine using the database URL from the config
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,  # This will typically be a PostgreSQL connection string
    pool_pre_ping=True  # Helps detect stale connections and reconnect automatically
)

# Create a sessionmaker factory bound to the engine
# A session is the primary way we interact with the database (e.g., querying, inserting)
SessionLocal = sessionmaker(
    autocommit=False,  # We'll manage commits manually (recommended)
    autoflush=False,   # Disable autoflush to avoid unintended writes
    bind=engine        # Bind the session to the engine created above
)
