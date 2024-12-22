from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import logging

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Completely disable SQLAlchemy logging to console
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.engine.base.Engine").setLevel(logging.ERROR)

# Configure file logging for SQLAlchemy
sql_handler = logging.FileHandler("logs/sqlalchemy.log")
sql_handler.setLevel(logging.INFO)
sql_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
sql_handler.setFormatter(sql_formatter)

# Add handler to SQLAlchemy loggers
for name in ["sqlalchemy", "sqlalchemy.engine", "sqlalchemy.engine.base.Engine"]:
    logger = logging.getLogger(name)
    logger.addHandler(sql_handler)
    logger.propagate = False

# Create SQLite database URL with absolute path
SQLALCHEMY_DATABASE_URL = "sqlite:///data/finance_tracker.db"

# Create engine with SQLite configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False,  # Disable SQL statement logging to console
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


# Create all tables if they don't exist
def init_db():
    inspector = inspect(engine)
    if not inspector.get_table_names():
        Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: Add event listeners to log SQL to file without console output
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(logging.INFO)
    logging.getLogger("sqlalchemy.engine").info("Executing query: %s", statement)


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logging.getLogger("sqlalchemy.engine").info("Finished executing query")
