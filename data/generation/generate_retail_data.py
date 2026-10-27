"""
SIGNALFIRE AI - Synthetic Retail Operations Data Generator
Generates realistic, internally-consistent datasets for 8 retail operations tables
over a 90-day simulation window.

Includes controlled anomaly injection with an explicit ground-truth registry
to enable honest analytical evaluation without data fabrication.
"""

import os
import json
import random
import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

# Fix seed for strict reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Apparel", "Home & Garden", "Pantry"]
CARRIERS = ["SwiftFreight", "MetroExpress", "AtlasLogistics", "ApexCourier"]
CHANNELS = ["Direct Web", "Mobile App", "Marketplace"]
COMPLAINT_CATEGORIES = ["Delayed Delivery", "Damaged Packaging", "Wrong Item Sent", "Billing Issue", "Product Defect"]
REFUND_REASONS = ["Late Arrival", "Damaged on Arrival", "Defective Product", "Not as Described", "Changed Mind"]

START_DATE = datetime.date(2026, 7, 1)
NUM_DAYS = 90
SIMULATION_DATES = [START_DATE + datetime.timedelta(days=i) for i in range(NUM_DAYS)]

# Ground Truth Anomaly Definitions
# Injected crisis begins at Day 50 (approx Aug 19, 2026) in the 'North' region
ANOMALY_START_DAY = 50
ANOMALY_START_DATE = START_DATE + datetime.timedelta(days=ANOMALY_START_DAY)
ANOMALY_END_DATE = START_DATE + datetime.timedelta(days=NUM_DAYS - 1)

GROUND_TRUTH_ANOMALIES = [
    {
        "anomaly_id": "GT-ANO-001",
        "dataset": "deliveries",
        "segment_dimension": "region",
        "segment_value": "North",
        "metric": "delay_days",
        "start_date": str(ANOMALY_START_DATE),
        "end_date": str(ANOMALY_END_DATE),
        "root_cause": "Carrier SwiftFreight transit hub breakdown and labor dispute in North hub",
        "nature": "Sudden upward shift in delivery delays from ~1.2 days to ~5.4 days",
        "expected_detection_method": "Robust Z-Score / Rolling Median Delta"
    },
    {
        "anomaly_id": "GT-ANO-002",
        "dataset": "customer_complaints",
        "segment_dimension": "region",
        "segment_value": "North",
        "metric": "complaint_volume",
        "start_date": str(START_DATE + datetime.timedelta(days=ANOMALY_START_DAY + 2)),
        "end_date": str(ANOMALY_END_DATE),
        "root_cause": "Customer dissatisfaction triggered by transit delays and damaged transit parcels",
        "nature": "3.5x surge in daily complaint volume, predominantly 'Delayed Delivery'",
        "expected_detection_method": "IQR / Poisson Outlier / Z-Score"
    },
    {
        "anomaly_id": "GT-ANO-003",
        "dataset": "refunds",
        "segment_dimension": "region",
        "segment_value": "North",
        "metric": "refund_rate",
        "start_date": str(START_DATE + datetime.timedelta(days=ANOMALY_START_DAY + 4)),
        "end_date": str(ANOMALY_END_DATE),
        "root_cause": "Downstream return and refund wave resulting from severe delivery delays",
        "nature": "Refunds rise from 2.6% of orders to 11.4% of orders",
        "expected_detection_method": "Moving Average Delta / Robust Z-Score"
    },
    {
        "anomaly_id": "GT-ANO-004",
        "dataset": "inventory",
        "segment_dimension": "region:category",
        "segment_value": "North:Electronics",
        "metric": "stockout_rate",
        "start_date": str(START_DATE + datetime.timedelta(days=ANOMALY_START_DAY + 6)),
        "end_date": str(ANOMALY_END_DATE),
        "root_cause": "Replenishment logistics stuck in transit causing critical electronics stockouts",
        "nature": "Stockout rate spikes from 3% to 44%",
        "expected_detection_method": "IQR / Percentage Threshold"
    },
    {
        "anomaly_id": "GT-ANO-005",
        "dataset": "customer_retention",
        "segment_dimension": "region",
        "segment_value": "North",
        "metric": "repeat_purchase_rate",
        "start_date": str(START_DATE + datetime.timedelta(days=ANOMALY_START_DAY + 10)),
        "end_date": str(ANOMALY_END_DATE),
        "root_cause": "Customer churn and erosion of brand trust following delivery and refund issues",
        "nature": "Repeat purchase rate drops from 41.5% to 22.0%",
        "expected_detection_method": "Rolling Window Negative Delta"
    }
]

def generate_all_datasets(output_dir: str = "data/csv") -> Dict[str, pd.DataFrame]:
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Suppliers
    suppliers_data = []
    supplier_names = [
        ("SUP-101", "Apex Precision Tech", "Electronics", 7, 1.2, 94.5),
        ("SUP-102", "Nordic Gear Ltd", "Apparel", 12, 2.1, 91.0),
        ("SUP-103", "Verdant Living Inc", "Home & Garden", 14, 1.8, 89.5),
        ("SUP-104", "Harvest Gold Supply", "Pantry", 5, 0.9, 97.2),
        ("SUP-105", "Silicon Core Components", "Electronics", 9, 3.8, 86.0),
        ("SUP-106", "Atlas Fabrics Corp", "Apparel", 10, 2.5, 90.2),
    ]
    for s_id, name, cat, lead, defect, rel in supplier_names:
        suppliers_data.append({
            "supplier_id": s_id,
            "supplier_name": name,
            "product_id": f"PRD-{cat[:3].upper()}-01",
            "category": cat,
            "lead_time_days": lead,
            "defect_rate_pct": defect,
            "reliability_score": rel
        })
    df_suppliers = pd.DataFrame(suppliers_data)
    df_suppliers.to_csv(os.path.join(output_dir, "suppliers.csv"), index=False)

    # 2. Products Catalog
    products = [
        {"product_id": "PRD-ELE-01", "name": "UltraSound ANC Headphones", "category": "Electronics", "price": 149.99},
        {"product_id": "PRD-ELE-02", "name": "Vision4K Smart Monitor", "category": "Electronics", "price": 299.99},
        {"product_id": "PRD-APP-01", "name": "Merino Wool Thermal Sweater", "category": "Apparel", "price": 79.50},
        {"product_id": "PRD-APP-02", "name": "All-Weather Technical Parka", "category": "Apparel", "price": 189.00},
        {"product_id": "PRD-HOM-01", "name": "Modular Hydroponic Garden", "category": "Home & Garden", "price": 119.00},
        {"product_id": "PRD-HOM-02", "name": "Ergonomic Ceramic Cookware Set", "category": "Home & Garden", "price": 159.50},
        {"product_id": "PRD-PAN-01", "name": "Organic Cold-Pressed Olive Oil 1L", "category": "Pantry", "price": 24.99},
        {"product_id": "PRD-PAN-02", "name": "Single-Origin Highland Coffee Beans", "category": "Pantry", "price": 18.50},
    ]

    # Generate daily transactional data
    orders_data = []
    sales_data = []
    deliveries_data = []
    complaints_data = []
    refunds_data = []
    inventory_data = []

    order_seq = 100000
    sale_seq = 200000
    deliv_seq = 300000
    comp_seq = 400000
    ref_seq = 500000
    inv_seq = 600000

    for day_idx, current_date in enumerate(SIMULATION_DATES):
        is_crisis_period = (day_idx >= ANOMALY_START_DAY)
        
        # Day of week seasonality
        dow_multiplier = 1.25 if current_date.weekday() in (4, 5, 6) else 0.95

        for region in REGIONS:
            is_affected_region = (region == "North" and is_crisis_period)

            # Base order count per region per day
            base_orders = int(np.random.normal(45, 6) * dow_multiplier)
            if is_affected_region:
                # Retention drop leads to slight order decline in late crisis
                days_into_crisis = day_idx - ANOMALY_START_DAY
                if days_into_crisis > 15:
                    base_orders = int(base_orders * 0.82)

            for _ in range(max(15, base_orders)):
                order_seq += 1
                cust_id = f"CUST-{random.randint(1000, 9999)}"
                channel = random.choices(CHANNELS, weights=[0.5, 0.35, 0.15])[0]
                
                # Pick product
                prod = random.choice(products)
                units = random.choices([1, 2, 3], weights=[0.8, 0.16, 0.04])[0]
                line_amount = round(prod["price"] * units, 2)

                order_id = f"ORD-{order_seq}"
                orders_data.append({
                    "order_id": order_id,
                    "customer_id": cust_id,
                    "order_date": current_date,
                    "region": region,
                    "channel": channel,
                    "order_total": line_amount,
                    "status": "Completed"
                })

                sale_seq += 1
                sales_data.append({
                    "sale_id": f"SAL-{sale_seq}",
                    "order_id": order_id,
                    "product_id": prod["product_id"],
                    "category": prod["category"],
                    "sale_date": current_date,
                    "region": region,
                    "amount": line_amount,
                    "units_sold": units
                })

                # Delivery generation
                deliv_seq += 1
                carrier = random.choice(CARRIERS)
                promised_days = random.choice([2, 3])

                # Anomaly 1: Delivery Delay in North
                if is_affected_region:
                    # SwiftFreight or regional bottleneck
                    actual_days = int(np.random.normal(5.8, 1.4))
                    actual_days = max(promised_days, actual_days)
                    delay_days = max(0, actual_days - promised_days)
                    deliv_status = "Delayed" if delay_days > 0 else "Delivered"
                else:
                    actual_days = promised_days + (1 if random.random() < 0.10 else 0)
                    delay_days = max(0, actual_days - promised_days)
                    deliv_status = "Delivered" if delay_days == 0 else "Delayed"

                deliveries_data.append({
                    "delivery_id": f"DEL-{deliv_seq}",
                    "order_id": order_id,
                    "carrier": carrier,
                    "dispatch_date": current_date,
                    "delivery_date": current_date + datetime.timedelta(days=actual_days),
                    "promised_days": promised_days,
                    "actual_days": actual_days,
                    "delay_days": delay_days,
                    "status": deliv_status,
                    "region": region
                })

                # Anomaly 2: Complaints surge
                complaint_prob = 0.02
                if is_affected_region:
                    complaint_prob = 0.095  # 4.75x increase

                if random.random() < complaint_prob:
                    comp_seq += 1
                    cat = "Delayed Delivery" if is_affected_region and random.random() < 0.70 else random.choice(COMPLAINT_CATEGORIES)
                    sev = "High" if (is_affected_region and random.random() < 0.6) else random.choice(["Low", "Medium", "High"])
                    complaints_data.append({
                        "complaint_id": f"CMP-{comp_seq}",
                        "customer_id": cust_id,
                        "order_id": order_id,
                        "complaint_date": current_date + datetime.timedelta(days=min(actual_days, 4)),
                        "category": cat,
                        "severity": sev,
                        "region": region,
                        "resolution_status": random.choice(["Open", "Investigating", "Resolved"])
                    })

                # Anomaly 3: Refund surge
                refund_prob = 0.025
                if is_affected_region:
                    refund_prob = 0.114  # 4.5x increase

                if random.random() < refund_prob:
                    ref_seq += 1
                    reason = "Late Arrival" if is_affected_region and random.random() < 0.65 else random.choice(REFUND_REASONS)
                    refunds_data.append({
                        "refund_id": f"REF-{ref_seq}",
                        "order_id": order_id,
                        "product_id": prod["product_id"],
                        "refund_date": current_date + datetime.timedelta(days=actual_days + 1),
                        "amount": line_amount,
                        "reason": reason,
                        "region": region
                    })

            # Inventory snapshots per region per product
            for p in products:
                inv_seq += 1
                base_stock = 120
                is_elec = (p["category"] == "Electronics")
                
                # Anomaly 4: Stockout crisis for North Electronics
                if is_affected_region and is_elec:
                    stock_level = max(0, int(np.random.normal(8, 4)))
                    stockout_flag = 1 if stock_level < 15 else 0
                else:
                    stock_level = int(np.random.normal(110, 18))
                    stockout_flag = 1 if stock_level < 20 else 0

                inventory_data.append({
                    "inventory_id": f"INV-{inv_seq}",
                    "product_id": p["product_id"],
                    "snapshot_date": current_date,
                    "region": region,
                    "stock_level": max(0, stock_level),
                    "reorder_threshold": 25,
                    "stockout_flag": stockout_flag
                })

    # 8. Customer Retention Cohorts (weekly snapshots)
    retention_data = []
    cohort_seq = 700000
    for week_num, snapshot_date in enumerate(SIMULATION_DATES[::7]):
        for region in REGIONS:
            cohort_seq += 1
            is_late_crisis = (region == "North" and snapshot_date >= (ANOMALY_START_DATE + datetime.timedelta(days=10)))
            
            if is_late_crisis:
                # Anomaly 5: Repeat purchase rate drops significantly
                repeat_rate = round(float(np.random.normal(0.22, 0.02)), 4)
                churn_rate = round(float(np.random.normal(0.28, 0.02)), 4)
                active_cust = int(np.random.normal(3200, 150))
            else:
                repeat_rate = round(float(np.random.normal(0.415, 0.02)), 4)
                churn_rate = round(float(np.random.normal(0.12, 0.015)), 4)
                active_cust = int(np.random.normal(4800, 200))

            retention_data.append({
                "cohort_id": f"COH-{cohort_seq}",
                "snapshot_date": snapshot_date,
                "region": region,
                "active_customers": active_cust,
                "repeat_purchase_rate": max(0.05, min(0.95, repeat_rate)),
                "churn_rate": max(0.01, min(0.95, churn_rate))
            })

    # Assemble DataFrames and export to CSV
    dfs = {
        "sales": pd.DataFrame(sales_data),
        "orders": pd.DataFrame(orders_data),
        "deliveries": pd.DataFrame(deliveries_data),
        "customer_complaints": pd.DataFrame(complaints_data),
        "refunds": pd.DataFrame(refunds_data),
        "inventory": pd.DataFrame(inventory_data),
        "suppliers": df_suppliers,
        "customer_retention": pd.DataFrame(retention_data),
    }

    for name, df in dfs.items():
        df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)

    # Save ground truth metadata
    ground_truth_path = os.path.join(os.path.dirname(output_dir), "ground_truth.json")
    with open(ground_truth_path, "w") as f:
        json.dump(GROUND_TRUTH_ANOMALIES, f, indent=2)

    return dfs

if __name__ == "__main__":
    dfs = generate_all_datasets()
    print("Synthetic Retail Datasets Generated Successfully:")
    for k, v in dfs.items():
        print(f"  - {k}: {len(v)} rows")
    print(f"Ground truth anomalies saved.")
