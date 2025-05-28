import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------
# Load environment variables
# -------------------------------
from dotenv import load_dotenv

# Load .env from project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

# -------------------------------
# Include app directory in path
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -------------------------------
# Import app settings and models
# -------------------------------
from app.core.config import settings
from app.db.base import Base  # Make sure this imports all your models

# -------------------------------
# Alembic Config
# -------------------------------
config = context.config
fileConfig(config.config_file_name)

# Inject DB URL from settings
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Metadata for autogeneration
target_metadata = Base.metadata

# -------------------------------
# Offline migrations (SQL script)
# -------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# -------------------------------
# Online migrations (live DB)
# -------------------------------
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Track column type changes
        )
        with context.begin_transaction():
            context.run_migrations()

# -------------------------------
# Entry point
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
