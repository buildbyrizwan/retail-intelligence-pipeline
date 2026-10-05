import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import List
from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()

# Define product catalog categories with baseline pricing ranges
PRODUCT_CATALOG = {
    "Electronics": {"min_price": 50.0, "max_price": 1200.0, "weight": 0.25},
    "Apparel": {"min_price": 15.0, "max_price": 180.0, "weight": 0.35},
    "Home & Kitchen": {"min_price": 20.0, "max_price": 350.0, "weight": 0.20},
    "Books & Media": {"min_price": 8.0, "max_price": 60.0, "weight": 0.10},
    "Fitness & Outdoors": {"min_price": 25.0, "max_price": 400.0, "weight": 0.10},
}

PAYMENT_METHODS = ["credit_card", "debit_card", "upi", "net_banking", "cash_on_delivery"]


class OrderEvent(BaseModel):
    """Schema validation for an incoming retail transaction event."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    product_id: str
    category: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=1, le=10)
    order_timestamp: datetime
    payment_method: str

    def to_dict(self) -> dict:
        return self.model_dump()


def generate_synthetic_orders(
    num_orders: int = 100,
    num_customers: int = 50,
    days_back: int = 30
) -> List[OrderEvent]:
    """Generates a batch of validated synthetic order events."""
    # Pre-generate a fixed customer pool so some customers have repeat orders (cohorts)
    customer_pool = [f"CUST_{i:04d}" for i in range(1, num_customers + 1)]
    
    # Pre-generate products
    categories = list(PRODUCT_CATALOG.keys())
    weights = [PRODUCT_CATALOG[cat]["weight"] for cat in categories]
    
    events: List[OrderEvent] = []
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days_back)
    
    for _ in range(num_orders):
        category = random.choices(categories, weights=weights)[0]
        price_range = PRODUCT_CATALOG[category]
        price = round(random.uniform(price_range["min_price"], price_range["max_price"]), 2)
        
        # Random timestamp within the specified window
        random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
        event_time = start_time + timedelta(seconds=random_seconds)
        
        order = OrderEvent(
            customer_id=random.choice(customer_pool),
            product_id=f"PROD_{category[:3].upper()}_{random.randint(101, 199)}",
            category=category,
            price=price,
            quantity=random.choices([1, 2, 3, 4, 5], weights=[0.6, 0.2, 0.1, 0.06, 0.04])[0],
            order_timestamp=event_time,
            payment_method=random.choice(PAYMENT_METHODS)
        )
        events.append(order)

    return events


if __name__ == "__main__":
    # Test batch generation
    sample_orders = generate_synthetic_orders(num_orders=5, num_customers=3)
    print(f"Generated {len(sample_orders)} sample orders successfully:\n")
    for order in sample_orders:
        print(order.to_dict())