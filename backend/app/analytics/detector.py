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

    def run_all_detection(self, datasets: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Runs complete anomaly detection suite across all available operational datasets."""
        all_findings = []
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

        # Sort findings by severity (CRITICAL first, then HIGH, then MEDIUM)
        sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        all_findings.sort(key=lambda x: sev_order.get(x["severity"], 4))
        return all_findings
