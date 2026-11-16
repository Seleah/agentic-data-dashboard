'''Copyright 2026 Seleah O'Connor

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://apache.org

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

CLEAN_FILE = Path("data/retail_demo_clean.csv")
ISSUES_FILE = Path("data/retail_demo_with_quality_issues.csv")

FIELDS = [
    "transaction_id",
    "transaction_date",
    "store_id",
    "state",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "discount_pct",
    "transaction_type",
]

STORES = [
    ("ST001", "CA"), ("ST002", "TX"), ("ST003", "NY"),
    ("ST004", "FL"), ("ST005", "IL"), ("ST006", "WA"),
    ("ST007", "CO"), ("ST008", "GA"),
]

PRODUCTS = [
    ("P1001", "Cotton T-shirt", "Apparel", 24.99),
    ("P1002", "Denim Jeans", "Apparel", 59.99),
    ("P1003", "Running Socks", "Apparel", 12.50),
    ("P2001", "Ceramic Mug", "Home", 14.99),
    ("P2002", "Throw Blanket", "Home", 39.99),
    ("P2003", "Storage Basket", "Home", 22.00),
    ("P3001", "Wireless Mouse", "Electronics", 29.99),
    ("P3002", "USB-C Charger", "Electronics", 19.99),
    ("P3003", "Bluetooth Speaker", "Electronics", 49.99),
    ("P4001", "Water Bottle", "Outdoor", 21.99),
    ("P4002", "Camping Lantern", "Outdoor", 34.99),
    ("P4003", "Daypack", "Outdoor", 54.99),
    ("P5001", "Notebook Set", "Stationery", 9.99),
    ("P5002", "Desk Organizer", "Stationery", 18.50),
    ("P5003", "Pen Pack", "Stationery", 6.99),
]

START_DATE = date(2025, 1, 1)
DAYS = 365
ROW_COUNT = 5_000


def date_weight(day):
    """Create plausible seasonal and weekend variation."""
    month_factor = {
        1: 0.88, 2: 0.90, 3: 0.95, 4: 0.98,
        5: 1.00, 6: 1.03, 7: 1.05, 8: 1.02,
        9: 0.98, 10: 1.04, 11: 1.30, 12: 1.42,
    }[day.month]
    weekend_factor = 1.25 if day.weekday() >= 5 else 1.0
    return month_factor * weekend_factor


def make_row(i):
    day = START_DATE + timedelta(days=random.randrange(DAYS))
    store_id, state = random.choice(STORES)
    product_id, name, category, base_price = random.choice(PRODUCTS)

    # Small stable-looking price variation, rounded to cents.
    unit_price = round(base_price * random.uniform(0.94, 1.06), 2)
    discount_pct = random.choices(
        [0, 5, 10, 15, 20],
        weights=[45, 20, 20, 10, 5],
    )[0]

    quantity = random.choices(
        [1, 2, 3, 4, 5, 6],
        weights=[45, 25, 14, 8, 5, 3],
    )[0]

    # More returns for products with more underlying sales.
    transaction_type = random.choices(
        ["sale", "return"],
        weights=[97, 3],
    )[0]

    # Returns use a positive quantity; transaction_type determines direction.
    # This avoids ambiguous negative quantities in the source data.
    return {
        "transaction_id": f"TXN{i:06d}",
        "transaction_date": day.isoformat(),
        "store_id": store_id,
        "state": state,
        "product_id": product_id,
        "product_name": name,
        "category": category,
        "quantity": quantity,
        "unit_price": f"{unit_price:.2f}",
        "discount_pct": discount_pct,
        "transaction_type": transaction_type,
    }


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


clean_rows = [make_row(i) for i in range(1, ROW_COUNT + 1)]
write_csv(CLEAN_FILE, clean_rows)

# Copy clean rows and add intentionally invalid records.
# Keep this file separate so it is never mistaken for clean production data.
dirty_rows = [row.copy() for row in clean_rows]

error_mutations = [
    {"transaction_date": "2025-19-45"},  # Invalid date
    {"store_id": ""},                    # Missing required store ID
    {"quantity": 0},                     # Invalid quantity: zero
    {"unit_price": "-12.50"},            # Invalid price: negative
    {"category": "Mystery"},             # Unknown category
    {"transaction_type": "exchange"},    # Invalid transaction type
    {"unit_price": "not-a-price"},       # Invalid price: string
]

available_indices = list(range(1, len(dirty_rows)))
chosen_indices = random.sample(available_indices, len(error_mutations) + 1)

# Use the last chosen index to overwrite an existing row with a duplicate of row 0
duplicate_idx = chosen_indices.pop()

# replace valid data with invalid data
for idx, mutation in zip(chosen_indices, error_mutations):
    dirty_rows[idx].update(mutation)

# add duplicate transaction
dirty_rows.insert(duplicate_idx, clean_rows[0].copy())

write_csv(ISSUES_FILE, dirty_rows)

print(f"Created {CLEAN_FILE} with {len(clean_rows)} valid rows.")
print(f"Created {ISSUES_FILE} with {len(dirty_rows)} rows, including intentional errors.")
