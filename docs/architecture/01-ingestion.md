# Ingestion - How Data Enters

## 1. Overview

This document describes the ingestion workflow for PATH-generated data, from external delivery via email to durable storage in the **Silver** data layer.  
The goal of this pipeline is the **capture raw PATH data**, ensure **reproducibility**, and establish a clean handoff point for downstream transformation logic.

**High-level flow**
External system  
    → Email  
    → Power Automate  
    → OneDrive  
    → Python Ingestion  
    → Silver (internal data layer)

---

**Regular job**
- Receive email (beginning of day) - *`.csv` file land in OneDrive*
- Code processing (end of day) - *system grab `.csv` file and push it to our internal database*

## 2. Data Source: PATH system

**2.1 Source Description**
- **System**: PATH
- **Data type**: Auto-generated CSV extract
- **Frequency**: Daily
- **Delivery mechanism**: Email attachment

**2.2 Source Report in PATH**
- `Report` → `Sales Report` → `Template→zheSO`
- Configuration:
    - Name: zheSO
    - Description: PATH-SalesOrder
    - `Auto Send Emails` → `Daily` → `CSV`
    - Start Date: None
    - End Date: None
    - Email(s): zhe.rao@monettefarms.ca
    - → `Save Report Template`

**2.3 Source Data Composition**
- **Sales Orders**: placeholder
- **Purchase Orders**: ***not available yet*** - due to inability to export the records

> key fact: no aggregated data is included, only transactional data with lowest granularity is needed

**2.4 File Naming Convention**

```text
<report-title>-<year>-<month>-<day>.csv
```

Example:

```text
zheSO-2026-1-6.csv
```

**Caution**
> Naming is controlled by **PATH**, but is used as **metadata**.   
The ingestion pipeline **assumes this naming convention**; changes in PATH naming may require ingestion logic updates.


## 3. Email-Based Delivery & Automation (Landing Layer via Power Automate)

**3.1 Email Trigger**

- Action: `When a new email arrives (V3)`
- **Connector**: OneDrive for Business
- Configurations
    - `From`: system@wsapath.com
    - `Include Attachments`: Yes
    - `Folder`: PATH

**3.2 Save Attached File**

- Action: `Create file` - *OneDrive for Business*
- **Connector**: OneDrive for Business
- Configurations
    - `Folder Path`: /Desktop/Work Files/Projects/7-PATH
    - `File Name`: `Dynamic Content` - `Attachments Name`
    - `File Content`: `Dynamic Content` - `For each` - `Current item`


## 4. Python-Based Ingestion to Silver Layer


