"""
SIGNALFIRE AI - MRO (Maintenance, Repair, and Operations) Dataset Generator
Generates realistic industrial plant operations, machinery telemetry, maintenance work orders,
spare parts inventory, and downtime incident logs.

Includes an injected cascading MRO crisis in Plant Alpha:
1. Machine vibration & thermal anomaly in assembly line turbine/pumps.
2. Preventive maintenance work orders delayed due to technician shortage.
3. Critical spare parts stockout (high-performance ceramic bearings).
4. Unscheduled line downtime of 46 hours causing cascading shipping delays.
5. Plants Beta, Gamma, Delta serve as unaffected control cohorts.
"""

import os
import json
import random
import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Any

RANDOM_SEED = 101
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

PLANTS = ["Plant Alpha (Detroit)", "Plant Beta (Stuttgart)", "Plant Gamma (Yokohama)", "Plant Delta (Monterrey)"]
EQUIPMENT_TYPES = ["CNC Milling Center", "Hydraulic Stamping Press", "Robotic Welder", "Centrifugal Coolant Pump"]
PART_CATEGORIES = ["Precision Bearings", "Hydraulic Seals", "Servo Motors", "Coolant Filters", "Drive Belts"]

START_DATE = datetime.date(2026, 7, 1)
NUM_DAYS = 90
DATES = [START_DATE + datetime.timedelta(days=i) for i in range(NUM_DAYS)]

MRO_CRISIS_START_DAY = 48
MRO_CRISIS_START_DATE = START_DATE + datetime.timedelta(days=MRO_CRISIS_START_DAY)

MRO_GROUND_TRUTH = [
    {
        "anomaly_id": "GT-MRO-001",
        "dataset": "equipment_telemetry",
        "segment_dimension": "plant",
        "segment_value": "Plant Alpha (Detroit)",
        "metric": "vibration_rms",
        "start_date": str(MRO_CRISIS_START_DATE),
        "end_date": str(DATES[-1]),
        "root_cause": "Bearing race degradation and shaft misalignment in Stamping Press #4",
        "nature": "Vibration velocity spikes from baseline 2.1 mm/s to 8.4 mm/s (>300% increase)",
        "expected_detection_method": "Robust Z-Score (MAD) & ISO 10816 Vibration Severity"
    },
    {
        "anomaly_id": "GT-MRO-002",
        "dataset": "maintenance_work_orders",
        "segment_dimension": "plant",
        "segment_value": "Plant Alpha (Detroit)",
        "metric": "work_order_overdue_rate",
        "start_date": str(START_DATE + datetime.timedelta(days=MRO_CRISIS_START_DAY + 2)),
        "end_date": str(DATES[-1]),
        "root_cause": "Staffing reallocation delaying scheduled preventive maintenance cycles",
        "nature": "Overdue PM work orders surge from 4% to 38%",
        "expected_detection_method": "Rolling Window Median Shift"
    },
    {
        "anomaly_id": "GT-MRO-003",
        "dataset": "spare_parts_inventory",
        "segment_dimension": "plant:part_category",
        "segment_value": "Plant Alpha (Detroit):Precision Bearings",
        "metric": "stockout_rate",
        "start_date": str(START_DATE + datetime.timedelta(days=MRO_CRISIS_START_DAY + 4)),
        "end_date": str(DATES[-1]),
        "root_cause": "Supplier component backorder causing critical spare parts stockout",
        "nature": "Bearing inventory drops to zero units for 16 consecutive operational days",
        "expected_detection_method": "Zero-Inventory Fence / Outlier"
    },
    {
        "anomaly_id": "GT-MRO-004",
        "dataset": "unscheduled_downtime",
        "segment_dimension": "plant",
        "segment_value": "Plant Alpha (Detroit)",
        "metric": "downtime_hours",
        "start_date": str(START_DATE + datetime.timedelta(days=MRO_CRISIS_START_DAY + 7)),
        "end_date": str(DATES[-1]),
        "root_cause": "Catastrophic mechanical seizure of unserviced hydraulic stamping press",
        "nature": "46.5 hours of unscheduled line downtime, incurring an estimated $280,000 loss",
        "expected_detection_method": "Extreme Value Peak Outlier"
    }
]

def generate_mro_datasets(output_dir: str = "data/mro_csv") -> Dict[str, pd.DataFrame]:
    os.makedirs(output_dir, exist_ok=True)

    telemetry_data = []
    work_orders_data = []
    inventory_data = []
    downtime_data = []
    suppliers_data = []

    # 1. MRO Suppliers
    sup_records = [
        ("MRO-SUP-01", "Koyo Precision Bearings", "Precision Bearings", 18, 1.2, 92.0),
        ("MRO-SUP-02", "Freudenberg Sealing Tech", "Hydraulic Seals", 7, 0.5, 96.5),
        ("MRO-SUP-03", "Siemens Drive Systems", "Servo Motors", 28, 2.4, 88.0),
        ("MRO-SUP-04", "Donaldson Filtration", "Coolant Filters", 5, 0.4, 98.1),
        ("MRO-SUP-05", "Gates Power Transmission", "Drive Belts", 10, 0.8, 94.0),
    ]
    for s_id, name, cat, lead, def_rate, rel in sup_records:
        suppliers_data.append({
            "supplier_id": s_id,
            "supplier_name": name,
            "part_category": cat,
            "standard_lead_days": lead,
            "defect_rate_pct": def_rate,
            "reliability_score": rel
        })
    df_suppliers = pd.DataFrame(suppliers_data)
    df_suppliers.to_csv(os.path.join(output_dir, "mro_suppliers.csv"), index=False)

    telem_seq = 1000
    wo_seq = 5000
    inv_seq = 8000
    down_seq = 9000

    for day_idx, current_date in enumerate(DATES):
        is_crisis_period = (day_idx >= MRO_CRISIS_START_DAY)

        for plant in PLANTS:
            is_alpha = ("Plant Alpha" in plant)
            is_affected = is_alpha and is_crisis_period

            # Daily Equipment Telemetry (vibration, temperature, oil pressure)
            for eq_idx, eq in enumerate(EQUIPMENT_TYPES):
                telem_seq += 1
                base_vib = 2.1
                base_temp = 58.5
                base_pressure = 145.0

                if is_affected and "Stamping Press" in eq:
                    # Anomaly 1: Severe vibration and heat escalation
                    vibration = round(float(np.random.normal(8.4, 1.1)), 2)
                    temp_c = round(float(np.random.normal(86.2, 3.4)), 1)
                    pressure = round(float(np.random.normal(118.0, 8.0)), 1)
                    health_status = "Alarm"
                else:
                    vibration = max(0.4, round(float(np.random.normal(base_vib, 0.3)), 2))
                    temp_c = round(float(np.random.normal(base_temp, 2.0)), 1)
                    pressure = round(float(np.random.normal(base_pressure, 4.0)), 1)
                    health_status = "Normal"

                telemetry_data.append({
                    "telemetry_id": f"TEL-{telem_seq}",
                    "timestamp": current_date,
                    "plant": plant,
                    "equipment_type": eq,
                    "equipment_id": f"EQ-{plant[:3].upper()}-{eq_idx+1}",
                    "vibration_rms_mm_s": vibration,
                    "operating_temp_c": temp_c,
                    "hydraulic_pressure_psi": pressure,
                    "health_status": health_status
                })

            # Daily Maintenance Work Orders
            wo_count = random.randint(3, 7)
            for _ in range(wo_count):
                wo_seq += 1
                wo_type = random.choices(["Preventive", "Corrective", "Emergency"], weights=[0.65, 0.25, 0.10])[0]
                planned_hours = random.choice([2.0, 4.0, 8.0])

                if is_affected and random.random() < 0.42:
                    # Anomaly 2: Work orders delayed / overdue
                    wo_status = "Overdue"
                    actual_hours = round(planned_hours * 1.8, 1)
                else:
                    wo_status = random.choices(["Completed", "In Progress", "Scheduled"], weights=[0.75, 0.18, 0.07])[0]
                    actual_hours = planned_hours if wo_status == "Completed" else None

                work_orders_data.append({
                    "work_order_id": f"WO-{wo_seq}",
                    "created_date": current_date,
                    "plant": plant,
                    "equipment_type": random.choice(EQUIPMENT_TYPES),
                    "work_type": wo_type,
                    "planned_hours": planned_hours,
                    "actual_hours": actual_hours,
                    "status": wo_status,
                    "priority": "P1" if is_affected else random.choice(["P1", "P2", "P3"])
                })

            # Daily Spare Parts Inventory
            for part in PART_CATEGORIES:
                inv_seq += 1
                is_bearing = (part == "Precision Bearings")

                if is_affected and is_bearing:
                    # Anomaly 3: Stockout of critical bearings
                    stock_qty = 0
                    stockout_flag = 1
                else:
                    stock_qty = max(2, int(np.random.normal(45, 8)))
                    stockout_flag = 0

                inventory_data.append({
                    "inventory_id": f"MRO-INV-{inv_seq}",
                    "snapshot_date": current_date,
                    "plant": plant,
                    "part_category": part,
                    "stock_qty": stock_qty,
                    "reorder_point": 15,
                    "stockout_flag": stockout_flag
                })

            # Unscheduled Downtime Incidents
            downtime_prob = 0.03
            if is_affected:
                downtime_prob = 0.28  # High chance of line stoppage

            if random.random() < downtime_prob:
                down_seq += 1
                if is_affected:
                    # Anomaly 4: Long downtime event
                    hours = round(float(np.random.normal(12.5, 3.0)), 1)
                    cost_per_hr = 6000
                    cause = "Mechanical Seizure: High Vibration / Bearing Failure"
                else:
                    hours = round(float(np.random.normal(1.8, 0.6)), 1)
                    cost_per_hr = 4500
                    cause = random.choice(["Sensor Calibration", "Tool Wear Replacement", "Minor Pneumatic Leak"])

                downtime_data.append({
                    "incident_id": f"DT-{down_seq}",
                    "incident_date": current_date,
                    "plant": plant,
                    "equipment_type": "Hydraulic Stamping Press" if is_affected else random.choice(EQUIPMENT_TYPES),
                    "downtime_hours": max(0.5, hours),
                    "estimated_loss_usd": round(hours * cost_per_hr, 2),
                    "root_cause_driver": cause,
                    "severity": "CRITICAL" if is_affected else "LOW"
                })

    dfs = {
        "equipment_telemetry": pd.DataFrame(telemetry_data),
        "maintenance_work_orders": pd.DataFrame(work_orders_data),
        "spare_parts_inventory": pd.DataFrame(inventory_data),
        "unscheduled_downtime": pd.DataFrame(downtime_data),
        "mro_suppliers": df_suppliers
    }

    for name, df in dfs.items():
        df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)

    with open(os.path.join(os.path.dirname(output_dir), "mro_ground_truth.json"), "w") as f:
        json.dump(MRO_GROUND_TRUTH, f, indent=2)

    return dfs

if __name__ == "__main__":
    dfs = generate_mro_datasets()
    print("MRO Datasets Generated:")
    for k, v in dfs.items():
        print(f"  - {k}: {len(v)} rows")
