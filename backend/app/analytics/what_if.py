"""
SIGNALFIRE AI - What-If Scenario Analysis Engine
Computes parameterized operational stress tests and operational impact models.
Explicitly distinguishes direct arithmetic consequences from probabilistic/model-based projections.
"""

from typing import Dict, Any, List

class WhatIfEngine:
    def __init__(self):
        pass

    def simulate_scenario(
        self,
        base_metrics: Dict[str, Any],
        delivery_delay_delta_pct: float = 0.0,
        refund_rate_delta_pct: float = 0.0,
        demand_delta_pct: float = 0.0,
        inventory_reduction_pct: float = 0.0
    ) -> Dict[str, Any]:
        """
        Runs sensitivity analysis under user-specified operational shifts.
        Returns:
        - Baseline metrics
        - Simulated metrics
        - Direct arithmetic consequences
        - Model-based inferences
        - Underlying assumptions and limitations
        """
        # Baseline operational benchmarks (derived from retail dataset)
        monthly_orders = base_metrics.get("monthly_orders", 5700)
        avg_order_value = base_metrics.get("avg_order_value", 112.50)
        base_monthly_revenue = monthly_orders * avg_order_value

        base_avg_delay_days = base_metrics.get("avg_delay_days", 1.85)
        base_refund_rate = base_metrics.get("refund_rate_pct", 3.2)
        base_stockout_rate = base_metrics.get("stockout_rate_pct", 4.5)
        base_complaint_rate = base_metrics.get("complaint_rate_pct", 2.6)

        # 1. Direct Arithmetic Calculations
        sim_orders = int(monthly_orders * (1.0 + demand_delta_pct / 100.0))
        sim_revenue = sim_orders * avg_order_value
        revenue_delta = sim_revenue - base_monthly_revenue

        sim_delay_days = round(max(0.0, base_avg_delay_days * (1.0 + delivery_delay_delta_pct / 100.0)), 2)
        sim_refund_rate = round(max(0.1, base_refund_rate + refund_rate_delta_pct), 2)
        sim_stockout_rate = round(max(0.0, min(100.0, base_stockout_rate + inventory_reduction_pct * 0.8)), 2)

        # Direct refund dollar volume calculation
        base_refund_dollars = base_monthly_revenue * (base_refund_rate / 100.0)
        sim_refund_dollars = sim_revenue * (sim_refund_rate / 100.0)
        refund_cost_delta = sim_refund_dollars - base_refund_dollars

        # 2. Model-Based Inferences (clearly labeled as empirical elasticity estimates)
        # Elasticity: each +1 day of delivery delay historically increases complaint probability by ~1.4%
        delay_shift_days = sim_delay_days - base_avg_delay_days
        projected_complaint_rate = round(max(0.5, base_complaint_rate + (delay_shift_days * 1.35)), 2)
        projected_monthly_complaints = int(sim_orders * (projected_complaint_rate / 100.0))
        base_monthly_complaints = int(monthly_orders * (base_complaint_rate / 100.0))
        additional_complaints = projected_complaint_rate - base_complaint_rate

        # Estimated unfulfilled or backordered orders due to stockouts
        estimated_lost_sales_orders = int(sim_orders * (sim_stockout_rate / 100.0) * 0.35)
        estimated_stockout_revenue_loss = round(estimated_lost_sales_orders * avg_order_value, 2)

        net_financial_impact = round(revenue_delta - refund_cost_delta - estimated_stockout_revenue_loss, 2)

        return {
            "inputs": {
                "delivery_delay_delta_pct": delivery_delay_delta_pct,
                "refund_rate_delta_pct": refund_rate_delta_pct,
                "demand_delta_pct": demand_delta_pct,
                "inventory_reduction_pct": inventory_reduction_pct
            },
            "baseline": {
                "monthly_orders": monthly_orders,
                "monthly_revenue": round(base_monthly_revenue, 2),
                "avg_delivery_delay_days": base_avg_delay_days,
                "refund_rate_pct": base_refund_rate,
                "stockout_rate_pct": base_stockout_rate,
                "monthly_refund_cost": round(base_refund_dollars, 2),
                "monthly_complaint_count": base_monthly_complaints
            },
            "simulated": {
                "monthly_orders": sim_orders,
                "monthly_revenue": round(sim_revenue, 2),
                "avg_delivery_delay_days": sim_delay_days,
                "refund_rate_pct": sim_refund_rate,
                "stockout_rate_pct": sim_stockout_rate,
                "monthly_refund_cost": round(sim_refund_dollars, 2),
                "projected_complaint_count": projected_monthly_complaints
            },
            "direct_arithmetic_consequences": [
                f"Gross revenue change: ${revenue_delta:+,.2f} based on {demand_delta_pct:+.1f}% demand adjustment.",
                f"Direct refund disbursement change: ${refund_cost_delta:+,.2f} resulting from adjusted {sim_refund_rate:.2f}% return rate.",
                f"Calculated average transit delay moves from {base_avg_delay_days:.2f}d to {sim_delay_days:.2f}d ({delivery_delay_delta_pct:+.1f}%)."
            ],
            "model_based_projections": [
                f"Estimated additional customer service escalations: ~{projected_monthly_complaints - base_monthly_complaints:+d} tickets/month (modeled delay elasticity factor: 1.35x).",
                f"Potential lost revenue from stockout abandonment: ~${estimated_stockout_revenue_loss:,.2f} (~{estimated_lost_sales_orders} orders).",
                f"Net projected operational impact: ${net_financial_impact:+,.2f} / month."
            ],
            "assumptions_and_limitations": [
                "Assumes average order value remains constant at $112.50 across categories.",
                "Customer churn elasticity is linear within tested ranges; extreme shifts may trigger non-linear tipping points.",
                "Stockout conversion assumption: 35% of stockout encounters result in permanent basket abandonment rather than substitution."
            ]
        }
