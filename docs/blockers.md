# PATH Sales Metrics – Data Contract Constraints

This document records metrics that are **currently not computable** with the available PATH data, due to missing or undefined semantic fields. These constraints must be resolved explicitly to avoid heuristic assumptions and ensure reporting accuracy.


## 1. Sales Mix by Customer Type (%)

**Target Metric**
- Retail / Direct  
- Contract-price Wholesale  
- Open Market  

**Proposed Solution**

> **Establish and maintain a `customer_name → customer_type` mapping in collaboration with Phil (~70 customers).**

**Blocking Constraint**

This metric is **not achievable** unless a deterministic indicator of customer or pricing type per sales order (or per sales line) is provided.

At least one of the following must exist in the data:
- Explicit `customer_type` field
- A maintained `customer_name → customer_type` mapping table


## 2. Sales Order Fulfillment Success Rate

**Target Metric**
Percentage of orders delivered with:
- No rejections
- No shortages
- No claims

**Proposed Solution**
> Instead of modifying records after partial rejection  
> **add a new record labeled `rejection`**

**Additional Data Labels (to be confirmed)**
- `normal`
- `rejection`
- `shortage` 
- `claims` 

> **Historical Concern (Phil)**
> - **When only spreadsheets are available, net amounts are preferred**
> - **In a centralized database, original transactions should be preserved where possible**
> - **Rejections introduce Order ID collisions and may require a new Order ID strategy**

**Blocking Constraint**

This metric is **not achievable** unless PATH explicitly defines:
1. What constitutes a *rejection*
2. What constitutes a *shortage*
3. What constitutes a *claim*

And unless each of these concepts:
- Exists as a structured field or event in the data
- Is traceable to a sales order (or order line)
- Has a clear lifecycle state (e.g. occurred / resolved / overridden)

> **Note**: Without event-level modeling (e.g. separate rejection records), fulfillment success cannot be derived reliably from aggregated or modified sales records.
