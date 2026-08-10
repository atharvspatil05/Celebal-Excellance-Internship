#!/usr/bin/env python3

import csv
import os
import random
from datetime import datetime, timedelta

SEED = 42

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

RAW = os.path.join(ROOT, "data", "raw")


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def generate():
    random.seed(SEED)

    # ---------------------------------------------------------
    # CUSTOMERS - 800 rows
    # Exactly 2% intentionally invalid emails = 16 rows.
    # ---------------------------------------------------------

    first_names = [
        "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan",
        "Ishaan", "Kabir", "Neha", "Ananya", "Priya",
        "Meera", "Isha", "Sneha", "Kavya", "Riya",
        "Aditi", "Rahul", "Sahil", "Nikhil", "Vikram"
    ]

    last_names = [
        "Sharma", "Patil", "Deshmukh", "Kulkarni", "Joshi",
        "Verma", "Singh", "Gupta", "Reddy", "Nair",
        "Mehta", "Pawar", "Jadhav", "Khan", "Mishra"
    ]

    domains = [
        "gmail.com",
        "outlook.com",
        "yahoo.com",
        "example.com"
    ]

    customers = []

    for i in range(1, 801):

        name = (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        )

        email = (
            f"{name.lower().replace(' ', '.')}"
            f"{i}@{random.choice(domains)}"
        )

        # Exactly 16 invalid emails.
        if i % 50 == 0:
            if i % 100 == 0:
                email = email.replace("@", "")
            else:
                email = email.split("@")[0] + "@"

        registration = (
            datetime(2025, 1, 1)
            + timedelta(days=random.randint(0, 500))
        )

        customers.append([
            f"CUST{i:04d}",
            name,
            email,
            registration.strftime("%Y-%m-%d"),
            random.choice([
                "REGULAR",
                "PREMIUM",
                "VIP"
            ])
        ])

    # Fixed registration dates for cohort testing.
    customers[0][3] = "2025-01-05"
    customers[1][3] = "2025-01-06"
    customers[2][3] = "2025-01-07"
    customers[3][3] = "2025-01-08"

    # ---------------------------------------------------------
    # PRODUCTS - 640 rows
    # Some names intentionally have spaces / mixed case.
    # ---------------------------------------------------------

    categories = {
        "Electronics": [
            "Smartphone", "Laptop", "Headphones", "Keyboard",
            "Monitor", "Smartwatch", "Tablet", "Camera"
        ],
        "Clothing": [
            "T-Shirt", "Jeans", "Jacket", "Sneakers",
            "Dress", "Hoodie", "Shirt", "Trousers"
        ],
        "Home": [
            "Mixer", "Lamp", "Chair", "Bedsheet",
            "Cookware", "Vacuum Cleaner", "Pillow", "Storage Box"
        ],
        "Books": [
            "Python Guide", "SQL Handbook", "Data Science",
            "Cloud Computing", "AI Fundamentals", "Algorithms",
            "Database Design", "Spark Guide"
        ]
    }

    products = []
    pid = 1

    for category, names in categories.items():

        subcategory = {
            "Electronics": "Gadgets",
            "Clothing": "Apparel",
            "Home": "Household",
            "Books": "Knowledge"
        }[category]

        for name in names:

            for variant in range(1, 21):

                product_name = f"{name} {variant}"

                if pid % 37 == 0:
                    product_name = (
                        f"  {product_name.upper()}  "
                    )

                elif pid % 41 == 0:
                    product_name = (
                        f" {product_name.lower()} "
                    )

                cost_price = round(
                    random.uniform(50, 30000),
                    2
                )

                products.append([
                    f"P{pid:04d}",
                    product_name,
                    category,
                    subcategory,
                    cost_price
                ])

                pid += 1

    product_by_id = {
        row[0]: row
        for row in products
    }

    product_ids = list(product_by_id.keys())

    # Keep P0001 dedicated to returns so SQL Query 5 is guaranteed
    # to return a value.
    normal_product_ids = [
        p for p in product_ids
        if p != "P0001"
    ]

    customer_ids = [
        row[0]
        for row in customers
    ]

    # ---------------------------------------------------------
    # ORDERS - 1,000 rows
    # Exactly 5% missing customer_id = 50 rows.
    # Some wrong date formats.
    # Some future dates for edge-case testing.
    # ---------------------------------------------------------

    orders = []

    today = datetime.now().replace(
        hour=12,
        minute=0,
        second=0,
        microsecond=0
    )

    reserved_customers = {
        "CUST0001",
        "CUST0002",
        "CUST0003",
        "CUST0004",
        "CUST0005",
        "CUST0800"
    }

    random_customer_ids = [
        c for c in customer_ids
        if c not in reserved_customers
    ]

    start = datetime(2025, 1, 1)

    for i in range(1, 1001):

        # Exactly 50 NULL customer IDs.
        if i <= 50:
            customer_id = None

        # Reserved records guarantee useful SQL outputs.
        elif i == 51:
            customer_id = "CUST0001"
        elif i == 52:
            customer_id = "CUST0002"
        elif i == 53:
            customer_id = "CUST0003"
        elif i == 54:
            customer_id = "CUST0004"
        elif i == 55:
            # Customer with no DELIVERED order.
            customer_id = "CUST0800"
        elif i == 56:
            customer_id = "CUST0001"
        elif i == 57:
            customer_id = "CUST0001"
        elif i == 58:
            customer_id = "CUST0001"
        elif i == 59:
            # Used for YoY comparison.
            customer_id = "CUST0005"
        elif i == 60:
            customer_id = "CUST0005"
        else:
            customer_id = random.choice(
                random_customer_ids
            )

        # Fixed dates for cohort / YoY / no-delivery testing.
        if i == 51:
            order_dt = datetime(2025, 1, 10, 10, 0, 0)
        elif i == 52:
            order_dt = datetime(2025, 1, 15, 10, 0, 0)
        elif i == 53:
            order_dt = datetime(2025, 1, 20, 10, 0, 0)
        elif i == 54:
            order_dt = datetime(2025, 1, 25, 10, 0, 0)
        elif i == 55:
            order_dt = datetime(2025, 2, 5, 10, 0, 0)
        elif i == 56:
            order_dt = datetime(2025, 2, 10, 10, 0, 0)
        elif i == 57:
            order_dt = datetime(2025, 3, 10, 10, 0, 0)
        elif i == 58:
            order_dt = datetime(2025, 4, 10, 10, 0, 0)
        elif i == 59:
            order_dt = datetime(2025, 1, 20, 12, 0, 0)
        elif i == 60:
            order_dt = datetime(2026, 1, 20, 12, 0, 0)
        elif i >= 990 and i <= 998:
            # Recent valid dates for dynamic report testing.
            # Keep them at least one day before today.
            order_dt = today - timedelta(
                days=(999 - i)
            )
        elif i >= 999:
            # Future dates for edge-case testing.
            order_dt = today + timedelta(
                days=(i - 998)
            )
        else:
            order_dt = start + timedelta(
                days=random.randint(
                    0,
                    max(1, (today - start).days - 2)
                ),
                seconds=random.randint(0, 86399)
            )

        # Force one customer to have no delivered order.
        if i == 55:
            status = "CANCELLED"
        else:
            status = random.choices(
                [
                    "PLACED",
                    "SHIPPED",
                    "DELIVERED",
                    "CANCELLED",
                    "RETURNED"
                ],
                weights=[
                    12,
                    16,
                    45,
                    12,
                    15
                ],
                k=1
            )[0]

        if i % 97 == 0:
            order_date = order_dt.strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        else:
            order_date = order_dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        orders.append([
            f"O{i:05d}",
            customer_id,
            order_date,
            status,
            random.choice([
                "NORTH",
                "SOUTH",
                "EAST",
                "WEST",
                "CENTRAL"
            ])
        ])

    order_ids = [
        row[0]
        for row in orders
    ]

    # ---------------------------------------------------------
    # ORDER ITEMS - 3,000 rows
    # Exactly 3% negative quantity = 90 rows.
    # Extra edge cases:
    # - 20 zero quantities
    # - 20 discounts > 100
    # - 20 unknown order_id values
    # ---------------------------------------------------------

    order_items = []

    for i in range(1, 3001):

        # 90 return records for P0001.
        # This guarantees returns > purchases for P0001.
        if i <= 90:

            order_id = random.choice(
                order_ids[60:900]
            )

            product_id = "P0001"

            quantity = -random.randint(1, 3)

        # Product pair data for Frequently Bought Together.
        elif i <= 120:

            pair_index = i - 91
            order_index = 100 + (pair_index // 2)

            order_id = order_ids[order_index]

            if pair_index % 2 == 0:
                product_id = "P0002"
            else:
                product_id = "P0003"

            quantity = random.randint(1, 3)

        # 20 zero-quantity records.
        elif i <= 140:

            order_id = random.choice(
                order_ids[60:900]
            )

            product_id = random.choice(
                normal_product_ids
            )

            quantity = 0

        else:

            order_id = random.choice(
                order_ids
            )

            product_id = random.choice(
                normal_product_ids
            )

            quantity = random.randint(1, 5)

        unit_price = round(
            product_by_id[product_id][4]
            * random.uniform(1.08, 1.65),
            2
        )

        # 20 invalid discounts.
        if 141 <= i <= 160:
            discount = round(
                random.uniform(101, 150),
                2
            )
        else:
            discount = round(
                random.uniform(0, 30),
                2
            )

        # 20 invalid order references.
        if i >= 2981:
            order_id = f"O999{i:05d}"

        order_items.append([
            f"OI{i:06d}",
            order_id,
            product_id,
            quantity,
            unit_price,
            discount
        ])

    # ---------------------------------------------------------
    # WRITE FILES
    # ---------------------------------------------------------

    write_csv(
        os.path.join(RAW, "customers.csv"),
        [
            "customer_id",
            "customer_name",
            "email",
            "registration_date",
            "customer_type"
        ],
        customers
    )

    write_csv(
        os.path.join(RAW, "products.csv"),
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "cost_price"
        ],
        products
    )

    write_csv(
        os.path.join(RAW, "orders.csv"),
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "region_code"
        ],
        orders
    )

    write_csv(
        os.path.join(RAW, "order_items.csv"),
        [
            "item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount_percent"
        ],
        order_items
    )

    print("Generated:")
    print(f"  customers.csv   : {len(customers)} rows")
    print(f"  products.csv    : {len(products)} rows")
    print(f"  orders.csv      : {len(orders)} rows")
    print(f"  order_items.csv : {len(order_items)} rows")


if __name__ == "__main__":
    generate()