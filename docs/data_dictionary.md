# SIGNALFIRE AI — Data Dictionary & Relational Schema

SIGNALFIRE AI operates on eight interconnected relational tables representing end-to-end retail and supply chain operations, plus a persistent table for analyst investigation tracking.

---

## 1. `sales` (Transaction Line Items)
Records individual product purchases across all sales channels.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `sale_id` | VARCHAR(50) | NO (PK) | Unique transaction line identifier (e.g. `SAL-200001`). |
| `order_id` | VARCHAR(50) | NO (FK) | Reference to parent order in `orders`. |
| `product_id` | VARCHAR(50) | NO | SKU identifier (e.g. `PRD-ELE-01`). |
| `category` | VARCHAR(50) | NO | Product category (`Electronics`, `Apparel`, `Home & Garden`, `Pantry`). |
| `sale_date` | DATE | NO | Calendar transaction date. |
| `region` | VARCHAR(30) | NO | Customer fulfillment region (`North`, `South`, `East`, `West`). |
| `amount` | DECIMAL(12,2)| NO | Line item gross dollar amount. |
| `units_sold` | INTEGER | NO | Quantity of units purchased. |

---

## 2. `orders` (Order Headers)
Records customer order headers, channels, and payment status.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(50) | NO (PK) | Primary key for the order (e.g. `ORD-100001`). |
| `customer_id` | VARCHAR(50) | NO | Customer account identifier. |
| `order_date` | DATE | NO | Timestamp of order checkout. |
| `region` | VARCHAR(30) | NO | Geographical operational territory. |
| `channel` | VARCHAR(30) | NO | Sales acquisition channel (`Direct Web`, `Mobile App`, `Marketplace`). |
| `order_total` | DECIMAL(12,2)| NO | Total basket value. |
| `status` | VARCHAR(30) | NO | Processing status (`Completed`, `Pending`, `Canceled`). |

---

## 3. `deliveries` (Logistics & Fulfillment)
Tracks fulfillment carrier dispatches, promised SLA dates, and actual delivery milestones.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `delivery_id` | VARCHAR(50) | NO (PK) | Tracking identifier (e.g. `DEL-300001`). |
| `order_id` | VARCHAR(50) | NO (FK) | Reference to parent order in `orders`. |
| `carrier` | VARCHAR(50) | NO | Logistics provider (`SwiftFreight`, `MetroExpress`, `AtlasLogistics`, `ApexCourier`). |
| `dispatch_date` | DATE | NO | Date parcel departed fulfillment warehouse. |
| `delivery_date` | DATE | YES | Date parcel reached customer doorstep. |
| `promised_days` | INTEGER | NO | SLA delivery window commitment (typically 2-3 days). |
| `actual_days` | INTEGER | YES | Realized transit duration. |
| `delay_days` | INTEGER | NO | Transit delay in days (`actual_days - promised_days`, clamped at 0). |
| `status` | VARCHAR(30) | NO | Delivery disposition (`Delivered`, `Delayed`, `In Transit`). |
| `region` | VARCHAR(30) | NO | Destination region. |

---

## 4. `customer_complaints` (Service & Support Escalations)
Logs customer support tickets, categories, and severity tiers.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `complaint_id` | VARCHAR(50) | NO (PK) | Support ticket identifier (e.g. `CMP-400001`). |
| `customer_id` | VARCHAR(50) | NO | Submitting customer account. |
| `order_id` | VARCHAR(50) | YES (FK) | Reference order if inquiry relates to a specific transaction. |
| `complaint_date`| DATE | NO | Timestamp when inquiry was submitted. |
| `category` | VARCHAR(50) | NO | Driver (`Delayed Delivery`, `Damaged Packaging`, `Wrong Item Sent`, `Product Defect`). |
| `severity` | VARCHAR(20) | NO | Ticket tier (`Low`, `Medium`, `High`). |
| `region` | VARCHAR(30) | NO | Customer region. |
| `resolution_status` | VARCHAR(30) | NO | Ticket state (`Open`, `Investigating`, `Resolved`). |

---

## 5. `refunds` (Returns & Disbursements)
Captures returned items, dollar refunds, and explicit return reasons.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `refund_id` | VARCHAR(50) | NO (PK) | Refund event identifier (e.g. `REF-500001`). |
| `order_id` | VARCHAR(50) | NO (FK) | Linked order. |
| `product_id` | VARCHAR(50) | NO | Returned product SKU. |
| `refund_date` | DATE | NO | Processing date of disbursement. |
| `amount` | DECIMAL(12,2)| NO | Refunded dollar value. |
| `reason` | VARCHAR(100)| NO | Customer return motive (`Late Arrival`, `Damaged on Arrival`, `Defective Product`). |
| `region` | VARCHAR(30) | NO | Customer territory. |

---

## 6. `inventory` (Warehouse Stock Snapshots)
Daily stock level snapshots across regional distribution hubs.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `inventory_id` | VARCHAR(50) | NO (PK) | Snapshot identifier (e.g. `INV-600001`). |
| `product_id` | VARCHAR(50) | NO | Stocked SKU. |
| `snapshot_date` | DATE | NO | Snapshot date. |
| `region` | VARCHAR(30) | NO | Regional warehouse location. |
| `stock_level` | INTEGER | NO | Current units on-hand. |
| `reorder_threshold` | INTEGER | NO | Replenishment trigger level. |
| `stockout_flag` | INTEGER | NO | Binary flag (`1` = out-of-stock, `0` = available). |

---

## 7. `suppliers` (Vendor Scorecard)
Vendor manufacturing and supply reliability benchmarks.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | VARCHAR(50) | NO (PK) | Vendor identifier (e.g. `SUP-101`). |
| `supplier_name`| VARCHAR(100)| NO | Partner name. |
| `product_id` | VARCHAR(50) | NO | Sourced SKU. |
| `category` | VARCHAR(50) | NO | Product category. |
| `lead_time_days`| INTEGER | NO | Standard manufacturing lead time. |
| `defect_rate_pct`| DECIMAL(5,2)| NO | Historical parts defect percentage. |
| `reliability_score`| DECIMAL(5,2)| NO | Comprehensive vendor scorecard (0-100). |

---

## 8. `customer_retention` (Cohort Longitudinal Retention)
Weekly active customer cohort metrics tracking loyalty and churn.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `cohort_id` | VARCHAR(50) | NO (PK) | Cohort identifier (e.g. `COH-700001`). |
| `snapshot_date` | DATE | NO | Weekly evaluation timestamp. |
| `region` | VARCHAR(30) | NO | Geographic cohort. |
| `active_customers` | INTEGER | NO | Count of unique active transacting accounts. |
| `repeat_purchase_rate` | DECIMAL(6,4)| NO | Fraction of customers completing a second purchase (0.0 to 1.0). |
| `churn_rate` | DECIMAL(6,4)| NO | Churn fraction (0.0 to 1.0). |

---

## 9. `investigations` (Analyst Decision Tracking)
Persistent investigation workspace records tracking operational resolutions.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `investigation_id` | VARCHAR(50) | NO (PK) | Audit ticket identifier (e.g. `INV-A1B2C3`). |
| `finding_id` | VARCHAR(100)| NO | Associated statistical finding. |
| `title` | VARCHAR(255)| NO | Investigation title. |
| `status` | VARCHAR(50) | NO | State (`New`, `Investigating`, `Confirmed`, `Dismissed`, `Resolved`). |
| `priority` | VARCHAR(20) | NO | Escalation tier (`P1`, `P2`, `P3`). |
| `suspected_cause` | VARCHAR(500)| YES | Hypothesized operational root-cause. |
| `verified_conclusion` | VARCHAR(1000)| YES | Confirmed empirical conclusion after log audit. |
| `notes` | VARCHAR(2000)| YES | Follow-up actions and partner SLA tickets. |
| `created_at` | TIMESTAMP | NO | Creation timestamp. |
| `updated_at` | TIMESTAMP | NO | Last modification timestamp. |
