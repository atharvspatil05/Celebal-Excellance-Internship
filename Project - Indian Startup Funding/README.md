# Indian Startup Funding Intelligence Pipeline

An end-to-end **Data Engineering project** based on Medallion
Architecture, Azure Data Factory, Azure Data Lake Storage Gen2, Azure
Databricks, PySpark, Delta Lake, and SQL analytics.

## Project Overview

This project transforms Indian startup funding data into a structured,
query-ready analytical layer.

It addresses three main analytical gaps:

-   Sector-wise funding velocity and year-over-year change
-   City-level funding patterns beyond the major Tier-1 cluster
-   Investor portfolio activity and funding-stage distribution over time

The architecture follows:

``` text
Kaggle CSV
    ↓
Python + ADLS Gen2
    ↓
Bronze — Raw Delta
    ↓
Silver — Cleansed Delta
    ↓
Gold — Business Analytics
    ↓
SQL Insights / Reports
```

## Scope

### In Scope

-   End-to-end ingestion and analytics
-   Bronze / Silver / Gold Medallion Architecture
-   SCD Type 2 historical tracking
-   SQL-based analytics
-   PySpark transformations
-   Azure cloud orchestration

### Out of Scope

-   Real-time / streaming data
-   Predictive / ML modelling
-   External API integration
-   Dashboarding / visualisation

## Dataset

**Source:** Kaggle --- Indian Startup Funding Dataset.

Key fields include:

  Field               Description
  ------------------- ----------------------------
  Date                Funding date
  Startup Name        Startup name
  Industry Vertical   Industry / sector
  Sub-Vertical        Sub-sector
  City                Startup location
  Investor Names      Participating investors
  Investment Type     Funding / investment stage
  Amount (USD)        Investment amount

### Data Quality

The pipeline addresses:

-   Null handling
-   Amount standardisation
-   INR / USD inconsistencies
-   City-name normalisation
-   Duplicate records
-   Date parsing
-   Data-type standardisation

## Architecture

### Bronze

The Bronze layer preserves raw source data as received.

-   Schema-on-read
-   Append-only approach
-   No business transformations
-   Delta Lake on ADLS Gen2

### Silver

The Silver layer produces a trusted, typed dataset.

Transformations include:

-   Null handling
-   Type casting
-   Deduplication
-   Date parsing
-   City normalisation

Typical PySpark operations:

``` python
filter()
withColumn()
cast()
groupBy()
agg()
```

### Gold

The Gold layer contains business-ready aggregations and historical
snapshots.

Techniques include:

-   `GROUP BY`
-   `SUM`
-   `AVG`
-   `COUNT`
-   `RANK()`
-   `ROW_NUMBER()`
-   `JOIN`
-   CTEs
-   `CASE WHEN`
-   SCD Type 2 `MERGE`

## Azure Technology Stack

  Component                      Purpose
  ------------------------------ ----------------------------------------------
  Python 3.x                     CSV ingestion and pre-upload standardisation
  Azure Data Lake Storage Gen2   Raw CSV landing zone / Bronze storage
  Azure Data Factory             Pipeline orchestration
  Azure Databricks               Spark execution and notebook processing
  PySpark                        DataFrame transformations
  Delta Lake                     ACID storage across medallion layers
  Databricks SQL                 Gold-layer analytics
  IAM / Service Principal        Cross-service authentication

## Pipeline Flow

``` text
Source CSV
    ↓
ADLS Gen2
    ↓
ADF Copy Activity
    ↓
Bronze Delta
    ↓
Silver Transformation
    ↓
Gold Transformation
    ↓
Analytical Gold Tables
    ↓
SQL Insights
```

## Gold Analytical Outputs

The project specification defines five analytical outputs.

### 1. `top_funded_sectors`

**Question:** Which sectors attracted the highest cumulative investment?

**Technique:** `GROUP BY + SUM + ORDER BY`

### 2. `city_funding_rank`

**Question:** Which cities beyond Tier-1 are emerging as startup hubs?

**Technique:**

``` sql
RANK() OVER (ORDER BY total_funding)
```

### 3. `sector_yoy_snapshot`

**Question:** How has EdTech / FinTech funding shifted post-COVID?

**Technique:** SCD Type 2 `MERGE + CTE`

### 4. `investor_deal_count`

**Question:** Who are the most active investors by volume?

**Technique:** `JOIN + GROUP BY + COUNT`

Example output generated during development:

    Rank Investor                    Deal Count
  ------ ------------------------- ------------
       1 Y Combinator                        84
       2 Mirae Asset                         83
       3 Info Edge                           82
       4 Accel                               80
       5 IFC                                 78
       6 Kalaari Capital                     77
       6 Sequoia Capital India               77
       8 Prosus Ventures                     75
       9 Tiger Global Management             74
      10 Nexus Venture Partners              73
      10 Ribbit Capital                      73
      12 Zodius Capital                      72
      13 Kedaara Capital                     70
      14 Peak XV                             69
      15 Blume Ventures                      67
      15 Elevation Capital                   67
      15 Omidyar Network                     67
      15 SoftBank Vision Fund                67
      19 Tiger Global                        66
      20 Falcon Edge                         65

> Investor-name variants are retained as represented in the analytical
> output.

### 5. `avg_deal_by_stage`

**Question:** What is the average deal size at Seed vs Series A vs
Series B?

**Technique:** `AVG() + CASE WHEN + GROUP BY`

## SCD Type 2

SCD Type 2 is used for historical tracking in the Gold layer.

Conceptually:

``` text
Existing Version
      ↓
End-date old version
      ↓
Insert new version
      ↓
Current historical snapshot
```

This preserves historical changes instead of overwriting previous
values.

## Suggested Repository Structure

``` text
Indian-Startup-Funding-Intelligence-Pipeline/
│
├── README.md
├── data/
│   └── startup_funding.csv
├── notebooks/
│   ├── bronze_ingestion
│   ├── bronze_to_silver
│   └── silver_to_gold
├── sql/
│   ├── top_funded_sectors.sql
│   ├── city_funding_rank.sql
│   ├── sector_yoy_snapshot.sql
│   ├── investor_deal_count.sql
│   └── avg_deal_by_stage.sql
├── adf/
│   └── pipeline/
└── docs/
    └── architecture/
```

Update notebook and folder names to match the final Azure/Databricks
implementation.

## Implementation Workflow

1.  Prepare the startup funding CSV.
2.  Upload the source file to ADLS Gen2.
3.  Ingest the raw data into the Bronze Delta layer.
4.  Apply Silver PySpark transformations.
5.  Create Gold analytical tables.
6.  Apply SCD Type 2 logic where required.
7.  Orchestrate the workflow with Azure Data Factory.
8.  Query the Gold layer using Databricks SQL.

## Validation Checklist

-   [ ] Source CSV available in ADLS Gen2
-   [ ] Bronze Delta table created
-   [ ] Silver transformation succeeds
-   [ ] Null handling verified
-   [ ] Data types verified
-   [ ] Duplicates handled
-   [ ] City values normalised
-   [ ] Gold tables created
-   [ ] SCD Type 2 logic verified
-   [ ] All five analytical outputs available
-   [ ] ADF pipeline validates
-   [ ] ADF pipeline runs successfully
-   [ ] Gold SQL queries return expected results

## Security

Never commit credentials to source control.

Do not expose:

-   Databricks access tokens
-   Passwords
-   Client secrets
-   Service-principal credentials
-   Azure Key Vault secrets

For production deployments, use an appropriate secret-management
solution such as Azure Key Vault.

## Business Questions

The final Gold layer supports:

1.  Which sectors received the most cumulative funding?
2.  Which cities are emerging as startup hubs?
3.  How has sector funding changed year-over-year?
4.  Which investors are most active by deal count?
5.  How does average deal size differ across funding stages?

## Project Status

This project implements the architecture specified in the **Indian
Startup Funding Intelligence Pipeline --- Technical Use Case Document
v1.0** and is designed as an end-to-end Azure Data Engineering portfolio
project.

## Author

**Atharv Patil**


