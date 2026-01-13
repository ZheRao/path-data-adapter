# 1. Postmortem: Blank Pay Period Names (Power BI) — Commented-Out Export

## Symptom
- Power BI shows blank / missing Pay Period names for 2026.
- Upstream pay period mapping appears updated, but the “OtherTables/PayPeriods.csv” used for cross-table mapping is stale.

## Root Cause
In the payroll pipeline, the export that refreshes Power BI’s PayPeriods mapping file was commented out:

```python
# data.loc[:,["PPName", "PPNum", "Cycle", "FiscalYear"]].drop_duplicates().to_csv(
#     self.gold_path["payroll"].parent / "OtherTables" / "PayPeriods.csv",
#     index=False
# )
return data
```

As a result, the transformation produced correct data, but the downstream mapping artifact was not regenerated.

## Summary

**Impact**

- Power BI mapping table didn’t include 2026 pay periods.
- Dashboard displayed blanks for pay period name fields that depend on the mapping.

**Fix**

- Re-enable export of PayPeriods.csv.

## Principle

**No silent artifacts**: any file written for Power BI must be owned by one function and validated immediately after write.