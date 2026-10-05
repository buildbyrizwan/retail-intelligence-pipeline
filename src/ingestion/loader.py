import logging
import pandas as pd
from sqlalchemy import text
from src.ingestion.generator import generate_synthetic_orders
from src.utils.db import get_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def load_raw_orders(batch_size: int = 500, num_customers: int = 100, days_back: int = 45) -> int:
    """Generates synthetic orders and loads them directly into raw.orders."""
    logger.info("Generating %d synthetic order events...", batch_size)
    orders = generate_synthetic_orders(
        num_orders=batch_size,
        num_customers=num_customers,
        days_back=days_back
    )
    
    # Convert validated Pydantic models to a DataFrame
    df = pd.DataFrame([order.to_dict() for order in orders])

    engine = get_engine()
    
    logger.info("Writing batch to PostgreSQL (raw.orders)...")
    with engine.begin() as conn:
        df.to_sql(
            name="orders",
            schema="raw",
            con=conn,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=500
        )
        
        # Verify total count in table
        result = conn.execute(text("SELECT COUNT(*) FROM raw.orders;"))
        total_rows = result.scalar()
        
    logger.info("Batch load complete! Total rows in raw.orders: %d", total_rows)
    return total_rows


if __name__ == "__main__":
    load_raw_orders(batch_size=500, num_customers=80, days_back=60)