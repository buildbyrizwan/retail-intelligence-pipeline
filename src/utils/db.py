import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Load environment variables from the .env file
load_dotenv()


def get_db_url() -> str:
    """Constructs the PostgreSQL connection string from environment variables."""
    user = os.getenv("DB_USER", "pipeline_user")
    password = os.getenv("DB_PASSWORD", "pipeline_secret")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "retail_warehouse")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"


def get_engine() -> Engine:
    """Creates and returns a SQLAlchemy database engine."""
    database_url = get_db_url()
    return create_engine(database_url, pool_pre_ping=True)


if __name__ == "__main__":
    # Quick sanity check to print the connection URL (masking password)
    url = get_db_url()
    masked_url = url.split("://")[0] + "://***:***@" + url.split("@")[-1]
    print(f"Database URL configured: {masked_url}")