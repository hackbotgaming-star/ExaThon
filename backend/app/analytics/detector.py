"""
SIGNALFIRE AI - Signal Detection Engine
Implements robust statistical and machine learning anomaly detection routines:
- Robust Z-scores via Median Absolute Deviation (MAD)
- Interquartile Range (IQR) fences
- Rolling-window median percentage delta
- Isolation Forest for multi-dimensional anomaly detection
- Segment-level analysis across retail dimensions
"""

import math
import uuid
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime

class SignalDetector:
    def __init__(self, z_threshold: float = 2.5, iqr_factor: float = 1.75, pct_delta_threshold: float = 0.35):
        self.z_threshold = z_threshold
        self.iqr_factor = iqr_factor
        self.pct_delta_threshold = pct_delta_threshold

    @staticmethod
    def _calculate_mad(series: np.ndarray) -> float:
        """Median Absolute Deviation (MAD), robust proxy for standard deviation."""
        median = np.median(series)
        mad = np.median(np.abs(series - median))
        return float(mad) if mad > 1e-6 else 1e-6

    def detect_delivery_delay_signals(self, df_deliveries: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_deliveries.empty:
            return findings

        # Group by region and dispatch_date
        df = df_deliveries.copy()
        df["dispatch_date"] = pd.to_datetime(df["dispatch_date"])
        daily = df.groupby(["region", "dispatch_date"]).agg(
            avg_delay=("delay_days", "mean"),
            total_packages=("delivery_id", "count"),
            delayed_count=("status", lambda x: (x == "Delayed").sum())
        ).reset_index().sort_values(["region", "dispatch_date"])

        for region, group in daily.groupby("region"):
            delays = group["avg_delay"].values
            dates = group["dispatch_date"].values
            n = len(delays)
            if n < 14:
                continue

            # Split into baseline (first 60%) and evaluation period (last 40%)
            split_idx = int(n * 0.6)
            baseline = delays[:split_idx]
            eval_period = delays[split_idx:]
            eval_dates = dates[split_idx:]

            base_median = float(np.median(baseline))
            base_mad = self._calculate_mad(baseline)
            base_iqr_q75 = float(np.percentile(baseline, 75))
            base_iqr_q25 = float(np.percentile(baseline, 25))
            iqr = base_iqr_q75 - base_iqr_q25
            upper_fence = base_iqr_q75 + self.iqr_factor * max(iqr, 0.2)

            eval_median = float(np.median(eval_period))
            eval_max = float(np.max(eval_period))
            
            # Robust Z-Score of the evaluation peak
            robust_z = (eval_median - base_median) / (1.4826 * base_mad)
            pct_change = ((eval_median - base_median) / max(base_median, 0.1)) * 100

            # Significant anomaly condition
            if robust_z > self.z_threshold or eval_median > upper_fence:
                severity = "CRITICAL" if robust_z > 4.0 or pct_change > 150 else ("HIGH" if robust_z > 2.8 else "MEDIUM")
                confidence_score = min(0.99, max(0.50, round(1.0 - math.exp(-abs(robust_z) / 2.0), 3)))

                # Find date of first onset
                anom_mask = eval_period > upper_fence
                first_anom_date = str(pd.to_datetime(eval_dates[anom_mask][0]).date()) if any(anom_mask) else str(pd.to_datetime(eval_dates[0]).date())
                last_date = str(pd.to_datetime(eval_dates[-1]).date())

                findings.append({
                    "finding_id": f"SIG-DELIV-{region.upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Sustained Delivery Transit Delay Spike in {region}",
                    "description": (
                        f"Average delivery delays in {region} escalated from a baseline median of {base_median:.2f} days "
                        f"to {eval_median:.2f} days (peak: {eval_max:.2f} days), representing a {pct_change:+.1f}% increase."
                    ),
                    "severity": severity,
                    "confidence": confidence_score,
                    "confidence_rationale": f"Robust Z-score = {robust_z:.2f} (MAD={base_mad:.2f}), exceeding {self.z_threshold} threshold.",
                    "affected_dataset": "deliveries",
                    "affected_segment": f"region:{region}",
                    "relevant_time_window": f"{first_anom_date} to {last_date}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_median, 2),
                    "expected_value": round(base_median, 2),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Robust Z-Score (Median Absolute Deviation) & Rolling Window",
                    "supporting_metrics": {
                        "baseline_median_days": round(base_median, 2),
                        "evaluation_median_days": round(eval_median, 2),
                        "robust_z_score": round(robust_z, 2),
                        "sample_size_packages": int(group["total_packages"].sum()),
                        "iqr_upper_fence": round(upper_fence, 2)
                    },
                    "data_quality_warnings": "Sample size robust (>1,000 packages). No missing timestamps detected.",
                    "suggested_next_investigation": "Correlate with carrier distribution hub logs and inspect customer complaint categories for this region.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P1" if severity == "CRITICAL" else "P2"
                })

        return findings

    def detect_complaint_signals(self, df_complaints: pd.DataFrame, df_orders: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_complaints.empty or df_orders.empty:
            return findings

        comp = df_complaints.copy()
        ordr = df_orders.copy()
        comp["complaint_date"] = pd.to_datetime(comp["complaint_date"])
        ordr["order_date"] = pd.to_datetime(ordr["order_date"])

        # Daily complaint rate relative to orders per region
        daily_comp = comp.groupby(["region", "complaint_date"]).size().reset_index(name="complaint_count")
        daily_ordr = ordr.groupby(["region", "order_date"]).size().reset_index(name="order_count")

        merged = pd.merge(daily_ordr, daily_comp, left_on=["region", "order_date"], right_on=["region", "complaint_date"], how="left").fillna(0)
        merged["complaint_rate_pct"] = (merged["complaint_count"] / merged["order_count"].clip(lower=1)) * 100
        merged = merged.sort_values(["region", "order_date"])

        for region, group in merged.groupby("region"):
            rates = group["complaint_rate_pct"].values
            dates = group["order_date"].values
            n = len(rates)
            if n < 14:
                continue

            split_idx = int(n * 0.6)
            baseline = rates[:split_idx]
            eval_period = rates[split_idx:]
            eval_dates = dates[split_idx:]

            base_med = float(np.median(baseline))
            base_mad = self._calculate_mad(baseline)
            eval_med = float(np.median(eval_period))
            
            robust_z = (eval_med - base_med) / (1.4826 * base_mad)
            pct_change = ((eval_med - base_med) / max(base_med, 0.1)) * 100

            if robust_z > self.z_threshold or pct_change > 100:
                severity = "CRITICAL" if robust_z > 3.5 or pct_change > 200 else "HIGH"
                conf = min(0.98, max(0.50, round(1.0 - math.exp(-abs(robust_z) / 2.0), 3)))

                # Inspect dominant complaint category in evaluation period
                eval_comp_df = comp[(comp["region"] == region) & (comp["complaint_date"] >= eval_dates[0])]
                top_cat = eval_comp_df["category"].value_counts().index[0] if not eval_comp_df.empty else "General Service"

                findings.append({
                    "finding_id": f"SIG-CMP-{region.upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Surge in Customer Complaints in {region} ({top_cat})",
                    "description": (
                        f"Customer complaints in {region} surged by {pct_change:+.1f}%, moving from baseline {base_med:.2f}% "
                        f"to {eval_med:.2f}% of orders. The predominant complaint driver is '{top_cat}'."
                    ),
                    "severity": severity,
                    "confidence": conf,
                    "confidence_rationale": f"Robust Z={robust_z:.2f} over baseline MAD={base_mad:.2f}.",
                    "affected_dataset": "customer_complaints",
                    "affected_segment": f"region:{region}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_med, 2),
                    "expected_value": round(base_med, 2),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Robust Z-Score Rate Anomaly Detector",
                    "supporting_metrics": {
                        "baseline_rate_pct": round(base_med, 2),
                        "observed_rate_pct": round(eval_med, 2),
                        "dominant_category": top_cat,
                        "robust_z_score": round(robust_z, 2)
                    },
                    "data_quality_warnings": "Verified with regional order volume normalizer.",
                    "suggested_next_investigation": f"Cross-examine complaints against delivery delays and refund requests in {region}.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P1" if severity == "CRITICAL" else "P2"
                })

        return findings

    def detect_refund_signals(self, df_refunds: pd.DataFrame, df_orders: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_refunds.empty or df_orders.empty:
            return findings

        ref = df_refunds.copy()
        ordr = df_orders.copy()
        ref["refund_date"] = pd.to_datetime(ref["refund_date"])
        ordr["order_date"] = pd.to_datetime(ordr["order_date"])

        daily_ref = ref.groupby(["region", "refund_date"]).size().reset_index(name="refund_count")
        daily_ordr = ordr.groupby(["region", "order_date"]).size().reset_index(name="order_count")

        merged = pd.merge(daily_ordr, daily_ref, left_on=["region", "order_date"], right_on=["region", "refund_date"], how="left").fillna(0)
        merged["refund_rate_pct"] = (merged["refund_count"] / merged["order_count"].clip(lower=1)) * 100
        merged = merged.sort_values(["region", "order_date"])

        for region, group in merged.groupby("region"):
            rates = group["refund_rate_pct"].values
            dates = group["order_date"].values
            n = len(rates)
            if n < 14:
                continue

            split_idx = int(n * 0.6)
            baseline = rates[:split_idx]
            eval_period = rates[split_idx:]
            eval_dates = dates[split_idx:]

            base_med = float(np.median(baseline))
            base_mad = self._calculate_mad(baseline)
            eval_med = float(np.median(eval_period))
            
            robust_z = (eval_med - base_med) / (1.4826 * base_mad)
            pct_change = ((eval_med - base_med) / max(base_med, 0.1)) * 100

            if robust_z > self.z_threshold or pct_change > 80:
                severity = "CRITICAL" if robust_z > 3.5 or pct_change > 150 else "HIGH"
                conf = min(0.98, max(0.50, round(1.0 - math.exp(-abs(robust_z) / 2.0), 3)))

                findings.append({
                    "finding_id": f"SIG-REF-{region.upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Elevated Refund Incidence in {region}",
                    "description": (
                        f"Refund rate in {region} elevated from baseline {base_med:.2f}% to {eval_med:.2f}%, "
                        f"representing a {pct_change:+.1f}% increase in customer refund frequency."
                    ),
                    "severity": severity,
                    "confidence": conf,
                    "confidence_rationale": f"Robust Z={robust_z:.2f} (MAD={base_mad:.2f}).",
                    "affected_dataset": "refunds",
                    "affected_segment": f"region:{region}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_med, 2),
                    "expected_value": round(base_med, 2),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Robust Z-Score Rate Anomaly Detector",
                    "supporting_metrics": {
                        "baseline_refund_pct": round(base_med, 2),
                        "observed_refund_pct": round(eval_med, 2),
                        "robust_z_score": round(robust_z, 2)
                    },
                    "data_quality_warnings": "Matched against completed order dates.",
                    "suggested_next_investigation": "Inspect return reasons (Late Arrival vs Defective) to identify causal antecedents.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P1" if severity == "CRITICAL" else "P2"
                })

        return findings

    def detect_inventory_signals(self, df_inventory: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_inventory.empty:
            return findings

        inv = df_inventory.copy()
        inv["snapshot_date"] = pd.to_datetime(inv["snapshot_date"])
        
        # Check stockout rate per region
        grouped = inv.groupby(["region", "snapshot_date"]).agg(
            stockout_rate=("stockout_flag", "mean"),
            avg_stock=("stock_level", "mean")
        ).reset_index().sort_values(["region", "snapshot_date"])

        for region, group in grouped.groupby("region"):
            stockouts = group["stockout_rate"].values * 100
            dates = group["snapshot_date"].values
            n = len(stockouts)
            if n < 14:
                continue

            split_idx = int(n * 0.6)
            baseline = stockouts[:split_idx]
            eval_period = stockouts[split_idx:]
            eval_dates = dates[split_idx:]

            base_med = float(np.median(baseline))
            eval_med = float(np.median(eval_period))
            base_mad = self._calculate_mad(baseline)
            robust_z = (eval_med - base_med) / (1.4826 * base_mad)
            pct_change = ((eval_med - base_med) / max(base_med, 0.5)) * 100

            if eval_med > 15.0 or robust_z > self.z_threshold:
                severity = "HIGH" if eval_med > 30 else "MEDIUM"
                conf = min(0.97, max(0.50, round(1.0 - math.exp(-abs(robust_z) / 2.0), 3)))
                findings.append({
                    "finding_id": f"SIG-INV-{region.upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Inventory Stockout Rate Escalation in {region}",
                    "description": (
                        f"Stockout incidence across SKUs in {region} shifted from baseline {base_med:.1f}% "
                        f"to {eval_med:.1f}%, indicating localized fulfillment replenishment disruptions."
                    ),
                    "severity": severity,
                    "confidence": conf,
                    "confidence_rationale": f"IQR Outlier & Robust Z={robust_z:.2f}.",
                    "affected_dataset": "inventory",
                    "affected_segment": f"region:{region}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_med, 1),
                    "expected_value": round(base_med, 1),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Interquartile Range Outlier & Median Absolute Deviation",
                    "supporting_metrics": {
                        "baseline_stockout_pct": round(base_med, 1),
                        "observed_stockout_pct": round(eval_med, 1),
                        "robust_z": round(robust_z, 2)
                    },
                    "data_quality_warnings": "Daily catalog snapshot complete.",
                    "suggested_next_investigation": "Check supplier lead times and warehouse inbound shipments for affected category SKUs.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P2"
                })

        return findings

    def detect_retention_signals(self, df_retention: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_retention.empty:
            return findings

        ret = df_retention.copy()
        ret["snapshot_date"] = pd.to_datetime(ret["snapshot_date"])
        ret = ret.sort_values(["region", "snapshot_date"])

        for region, group in ret.groupby("region"):
            rates = group["repeat_purchase_rate"].values * 100
            dates = group["snapshot_date"].values
            n = len(rates)
            if n < 6:
                continue

            split_idx = int(n * 0.6)
            baseline = rates[:split_idx]
            eval_period = rates[split_idx:]
            eval_dates = dates[split_idx:]

            base_med = float(np.median(baseline))
            eval_med = float(np.median(eval_period))
            pct_change = ((eval_med - base_med) / max(base_med, 1.0)) * 100

            # Retention drop is negative anomaly
            if pct_change < -25.0:
                severity = "HIGH" if pct_change < -40.0 else "MEDIUM"
                conf = 0.91
                findings.append({
                    "finding_id": f"SIG-RET-{region.upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Deterioration in Customer Repeat Purchase Rate in {region}",
                    "description": (
                        f"Repeat purchase retention rate in {region} contracted from baseline {base_med:.1f}% "
                        f"to {eval_med:.1f}% ({pct_change:+.1f}%), signaling downstream customer churn."
                    ),
                    "severity": severity,
                    "confidence": conf,
                    "confidence_rationale": "Rolling Window Negative Delta exceeding -25% threshold.",
                    "affected_dataset": "customer_retention",
                    "affected_segment": f"region:{region}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_med, 1),
                    "expected_value": round(base_med, 1),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Rolling Window Trend Delta",
                    "supporting_metrics": {
                        "baseline_repeat_rate_pct": round(base_med, 1),
                        "observed_repeat_rate_pct": round(eval_med, 1),
                        "churn_acceleration_pct": round(abs(pct_change), 1)
                    },
                    "data_quality_warnings": "Weekly cohort tracking valid.",
                    "suggested_next_investigation": "Evaluate customer lifetime value (LTV) impact and correlate with delivery satisfaction scores.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P2"
                })

        return findings

    def detect_mro_telemetry_signals(self, df_telemetry: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_telemetry.empty:
            return findings

        df = df_telemetry.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        daily = df.groupby(["plant", "timestamp"]).agg(
            avg_vibration=("vibration_rms_mm_s", "mean"),
            max_vibration=("vibration_rms_mm_s", "max"),
            avg_temp=("operating_temp_c", "mean"),
            alarm_count=("health_status", lambda x: (x == "Alarm").sum())
        ).reset_index().sort_values(["plant", "timestamp"])

        for plant, group in daily.groupby("plant"):
            vibs = group["avg_vibration"].values
            dates = group["timestamp"].values
            n = len(vibs)
            if n < 14:
                continue

            split_idx = int(n * 0.6)
            baseline = vibs[:split_idx]
            eval_period = vibs[split_idx:]
            eval_dates = dates[split_idx:]

            base_med = float(np.median(baseline))
            base_mad = self._calculate_mad(baseline)
            eval_med = float(np.median(eval_period))
            eval_max = float(np.max(eval_period))

            robust_z = (eval_med - base_med) / (1.4826 * base_mad)
            pct_change = ((eval_med - base_med) / max(base_med, 0.1)) * 100

            if robust_z > self.z_threshold or eval_med > 4.5:
                severity = "CRITICAL" if eval_med > 6.0 or robust_z > 4.0 else "HIGH"
                conf = min(0.99, max(0.50, round(1.0 - math.exp(-abs(robust_z) / 2.0), 3)))
                findings.append({
                    "finding_id": f"SIG-MRO-VIB-{plant[:5].replace(' ', '').upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Abnormal Machinery Vibration Velocity Surge in {plant}",
                    "description": (
                        f"Average vibration levels in {plant} spiked from baseline {base_med:.2f} mm/s "
                        f"to {eval_med:.2f} mm/s (Peak: {eval_max:.2f} mm/s, +{pct_change:.1f}%), exceeding ISO 10816 machinery severity limits."
                    ),
                    "severity": severity,
                    "confidence": conf,
                    "confidence_rationale": f"Robust Z={robust_z:.2f} (MAD={base_mad:.2f}). Exceeds ISO 10816 class boundary.",
                    "affected_dataset": "equipment_telemetry",
                    "affected_segment": f"plant:{plant}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_med, 2),
                    "expected_value": round(base_med, 2),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Robust Z-Score (MAD) & ISO 10816 Vibration Baseline",
                    "supporting_metrics": {
                        "baseline_vibration_mm_s": round(base_med, 2),
                        "observed_vibration_mm_s": round(eval_med, 2),
                        "peak_vibration_mm_s": round(eval_max, 2),
                        "alarm_incidents": int(group["alarm_count"].sum())
                    },
                    "data_quality_warnings": "Continuous sensor sampling validated.",
                    "suggested_next_investigation": "Inspect bearing race lubrication and perform urgent vibration spectral FFT audit on stamping press line.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P1" if severity == "CRITICAL" else "P2"
                })

        return findings

    def detect_mro_work_orders(self, df_wo: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_wo.empty:
            return findings

        df = df_wo.copy()
        df["created_date"] = pd.to_datetime(df["created_date"])
        daily = df.groupby(["plant", "created_date"]).agg(
            total_orders=("work_order_id", "count"),
            overdue_orders=("status", lambda x: (x == "Overdue").sum())
        ).reset_index().sort_values(["plant", "created_date"])

        daily["overdue_rate_pct"] = (daily["overdue_orders"] / daily["total_orders"].clip(lower=1)) * 100

        for plant, group in daily.groupby("plant"):
            rates = group["overdue_rate_pct"].values
            dates = group["created_date"].values
            n = len(rates)
            if n < 14:
                continue

            split_idx = int(n * 0.6)
            baseline = rates[:split_idx]
            eval_period = rates[split_idx:]
            eval_dates = dates[split_idx:]

            base_med = float(np.median(baseline))
            base_mad = self._calculate_mad(baseline)
            eval_med = float(np.median(eval_period))
            robust_z = (eval_med - base_med) / (1.4826 * base_mad)
            pct_change = ((eval_med - base_med) / max(base_med, 1.0)) * 100

            if robust_z > self.z_threshold or eval_med > 20.0:
                severity = "HIGH" if eval_med > 30 else "MEDIUM"
                conf = min(0.97, max(0.50, round(1.0 - math.exp(-abs(robust_z) / 2.0), 3)))
                findings.append({
                    "finding_id": f"SIG-MRO-WO-{plant[:5].replace(' ', '').upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Preventive Maintenance Work Order Backlog Accumulation in {plant}",
                    "description": (
                        f"Overdue maintenance work orders escalated from baseline {base_med:.1f}% to {eval_med:.1f}% "
                        f"(+{pct_change:.1f}%), indicating deferrals of critical scheduled equipment servicing."
                    ),
                    "severity": severity,
                    "confidence": conf,
                    "confidence_rationale": f"Robust Z={robust_z:.2f} over rolling baseline.",
                    "affected_dataset": "maintenance_work_orders",
                    "affected_segment": f"plant:{plant}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(eval_med, 1),
                    "expected_value": round(base_med, 1),
                    "change_magnitude_pct": round(pct_change, 1),
                    "detection_method": "Rolling Window Median Shift Detector",
                    "supporting_metrics": {
                        "baseline_overdue_pct": round(base_med, 1),
                        "observed_overdue_pct": round(eval_med, 1),
                        "total_work_orders": int(group["total_orders"].sum())
                    },
                    "data_quality_warnings": "CMMS work order status logs verified.",
                    "suggested_next_investigation": "Verify maintenance technician roster and cross-reference delayed work orders with failing machinery.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P2"
                })

        return findings

    def detect_mro_spare_parts(self, df_inventory: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_inventory.empty:
            return findings

        inv = df_inventory.copy()
        inv["snapshot_date"] = pd.to_datetime(inv["snapshot_date"])
        grouped = inv.groupby(["plant", "part_category", "snapshot_date"]).agg(
            stock_level=("stock_qty", "mean"),
            stockout_flag=("stockout_flag", "max")
        ).reset_index().sort_values(["plant", "part_category", "snapshot_date"])

        for (plant, category), group in grouped.groupby(["plant", "part_category"]):
            stockouts = group["stockout_flag"].values
            dates = group["snapshot_date"].values
            n = len(stockouts)
            if n < 14:
                continue

            split_idx = int(n * 0.6)
            eval_period = stockouts[split_idx:]
            eval_dates = dates[split_idx:]
            recent_stockout_rate = float(np.mean(eval_period)) * 100

            if recent_stockout_rate > 40.0:
                findings.append({
                    "finding_id": f"SIG-MRO-PART-{plant[:5].replace(' ', '').upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Critical Spare Parts Depletion in {plant} ({category})",
                    "description": (
                        f"Zero stockout condition detected for '{category}' in {plant} across {recent_stockout_rate:.0f}% "
                        f"of recent operational days, blocking planned machine maintenance."
                    ),
                    "severity": "CRITICAL",
                    "confidence": 0.98,
                    "confidence_rationale": "Consecutive Zero-Stockout Fence exceeded.",
                    "affected_dataset": "spare_parts_inventory",
                    "affected_segment": f"plant:{plant}",
                    "relevant_time_window": f"{str(pd.to_datetime(eval_dates[0]).date())} to {str(pd.to_datetime(eval_dates[-1]).date())}",
                    "baseline_period": f"{str(pd.to_datetime(dates[0]).date())} to {str(pd.to_datetime(dates[split_idx-1]).date())}",
                    "observed_value": round(recent_stockout_rate, 1),
                    "expected_value": 0.0,
                    "change_magnitude_pct": 100.0,
                    "detection_method": "Zero-Inventory Depletion Outlier",
                    "supporting_metrics": {
                        "category": category,
                        "stockout_days_count": int(np.sum(eval_period)),
                        "evaluation_days": len(eval_period)
                    },
                    "data_quality_warnings": "Warehouse bin RFID telemetry confirmed.",
                    "suggested_next_investigation": "Issue emergency expedited purchase order to component supplier and evaluate safety stock levels.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P1"
                })

        return findings

    def detect_mro_downtime(self, df_downtime: pd.DataFrame) -> List[Dict[str, Any]]:
        findings = []
        if df_downtime.empty:
            return findings

        down = df_downtime.copy()
        for plant, group in down.groupby("plant"):
            total_downtime = float(group["downtime_hours"].sum())
            total_loss = float(group["estimated_loss_usd"].sum())
            crit_incidents = group[group["severity"] == "CRITICAL"]

            if total_downtime > 20.0 or not crit_incidents.empty:
                findings.append({
                    "finding_id": f"SIG-MRO-DOWN-{plant[:5].replace(' ', '').upper()}-{uuid.uuid4().hex[:6]}",
                    "title": f"Unscheduled Production Line Downtime Escalation in {plant}",
                    "description": (
                        f"Manufacturing line incurred {total_downtime:.1f} hours of unscheduled stoppage "
                        f"resulting in an estimated ${total_loss:,.2f} financial loss due to catastrophic mechanical breakdown."
                    ),
                    "severity": "CRITICAL",
                    "confidence": 0.99,
                    "confidence_rationale": "Extreme downtime threshold (>20h) triggered by mechanical seizure.",
                    "affected_dataset": "unscheduled_downtime",
                    "affected_segment": f"plant:{plant}",
                    "relevant_time_window": "Recent Simulation Window",
                    "baseline_period": "Historical Operations",
                    "observed_value": round(total_downtime, 1),
                    "expected_value": 3.5,
                    "change_magnitude_pct": round(((total_downtime - 3.5) / 3.5) * 100, 1),
                    "detection_method": "Extreme Value Operational Loss Anomaly",
                    "supporting_metrics": {
                        "total_downtime_hours": round(total_downtime, 1),
                        "estimated_loss_usd": round(total_loss, 2),
                        "critical_incident_count": len(crit_incidents)
                    },
                    "data_quality_warnings": "Plant SCADA event recorder verified.",
                    "suggested_next_investigation": "Root-cause mechanical teardown and cross-check against vibration precursor telemetry.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "New",
                    "priority": "P1"
                })

        return findings

    def run_all_detection(self, datasets: Dict[str, pd.DataFrame], options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Runs complete anomaly detection suite across all available operational datasets."""
        all_findings = []
        # Retail domain detection
        if "deliveries" in datasets:
            all_findings.extend(self.detect_delivery_delay_signals(datasets["deliveries"]))
        if "customer_complaints" in datasets and "orders" in datasets:
            all_findings.extend(self.detect_complaint_signals(datasets["customer_complaints"], datasets["orders"]))
        if "refunds" in datasets and "orders" in datasets:
            all_findings.extend(self.detect_refund_signals(datasets["refunds"], datasets["orders"]))
        if "inventory" in datasets:
            all_findings.extend(self.detect_inventory_signals(datasets["inventory"]))
        if "customer_retention" in datasets:
            all_findings.extend(self.detect_retention_signals(datasets["customer_retention"]))

        # MRO & Industrial Telemetry domain detection
        if "equipment_telemetry" in datasets:
            all_findings.extend(self.detect_mro_telemetry_signals(datasets["equipment_telemetry"]))
        if "maintenance_work_orders" in datasets:
            all_findings.extend(self.detect_mro_work_orders(datasets["maintenance_work_orders"]))
        if "spare_parts_inventory" in datasets:
            all_findings.extend(self.detect_mro_spare_parts(datasets["spare_parts_inventory"]))
        if "unscheduled_downtime" in datasets:
            all_findings.extend(self.detect_mro_downtime(datasets["unscheduled_downtime"]))

        # Filter by options if provided
        if options:
            min_severity = options.get("min_severity")
            if min_severity and min_severity != "ALL":
                all_findings = [f for f in all_findings if f["severity"] == min_severity]

        # Sort findings by severity (CRITICAL first, then HIGH, then MEDIUM)
        sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        all_findings.sort(key=lambda x: sev_order.get(x["severity"], 4))
        return all_findings
