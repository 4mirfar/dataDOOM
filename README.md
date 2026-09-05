# DataDOOM

**Production-Style Data Pipeline for Financial Market Data**

DataDOOM is a production-oriented data engineering project that ingests financial market data from external APIs, validates and processes the data, stores raw records in PostgreSQL, and orchestrates the pipeline with Apache Airflow.

The project is designed around real-world data engineering concerns such as **incremental ingestion, idempotency, data validation, retries, backfills, observability, and reproducibility** rather than a simple one-off ETL script.

---

## Architecture

```text
                 ┌─────────────────────┐
                 │   External APIs      │
                 │     CoinGecko        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Python Ingestion  │
                 │                     │
                 │  • Extraction       │
                 │  • Validation       │
                 │  • Incremental      │
                 │    Filtering        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     PostgreSQL      │
                 │                     │
                 │      Raw Layer      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       dbt           │
                 │                     │
                 │  Staging Models     │
                 │  Analytics Models   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Analytics / BI      │
                 └─────────────────────┘

                         ▲
                         │
                 ┌───────┴────────┐
                 │ Apache Airflow │
                 │ Orchestration  │
                 └────────────────┘
```

---

## Project Goals

DataDOOM is built to demonstrate how a reliable data pipeline should behave in production-like environments.

The pipeline focuses on:

* Incremental data ingestion
* Idempotent processing
* Data validation and quality checks
* Retry and failure handling
* PostgreSQL-based raw data storage
* Workflow orchestration with Airflow
* Analytics-ready transformations with dbt
* Automated testing
* Logging and observability
* Reproducible infrastructure with Docker
* Backfill and recovery capabilities

---

## Tech Stack

| Component       | Technology      |
| --------------- | --------------- |
| Language        | Python          |
| Database        | PostgreSQL      |
| Orchestration   | Apache Airflow  |
| Transformation  | dbt             |
| Validation      | Pydantic        |
| HTTP Client     | HTTPX           |
| Data Processing | Pandas / Polars |
| Infrastructure  | Docker          |
| Testing         | Pytest          |
| Data Source     | CoinGecko API   |

---

## Current Pipeline

The current implementation ingests cryptocurrency market data for:

* Bitcoin
* Ethereum

from the CoinGecko API.

A typical ingestion run follows:

```text
API Request
    ↓
Extract Market Data
    ↓
Validate Records
    ↓
Check Incremental State
    ↓
Filter New Records
    ↓
Insert into PostgreSQL
```

---

## Key Engineering Features

### 1. Incremental Ingestion

DataDOOM does not blindly insert every API response into the database.

Before loading a record, the pipeline checks the latest timestamp already stored for the corresponding source and symbol.

```text
API
 │
 ├── Existing timestamp
 │        ↓
 │      Skip
 │
 └── New timestamp
          ↓
        Insert
```

This prevents unnecessary processing and allows the pipeline to operate continuously.

---

### 2. Idempotent Loading

The PostgreSQL raw table uses a composite uniqueness constraint:

```sql
UNIQUE (source, symbol, timestamp)
```

Records are inserted using:

```sql
ON CONFLICT (source, symbol, timestamp)
DO NOTHING;
```

This means rerunning the same ingestion job does not create duplicate records.

For example:

```text
Run 1 → 2 records inserted
Run 2 → 0 records inserted
Run 3 → 0 records inserted
```

The pipeline therefore remains safe to retry.

---

### 3. Data Validation

Incoming API records are validated using Pydantic before they reach the database.

Example validation rules include:

* Symbol must exist
* Current price cannot be negative
* Timestamp must be valid
* Duplicate records inside an API response are rejected

Invalid records are rejected without stopping the entire ingestion process.

Example:

```text
Fetched       : 10
Valid         : 8
Rejected      : 2
New records   : 5
Inserted      : 5
```

---

### 4. Retry Handling

External APIs can fail.

The CoinGecko client therefore implements retry logic with exponential backoff.

```text
Attempt 1
   ↓
Failure
   ↓
Wait 1s
   ↓
Attempt 2
   ↓
Failure
   ↓
Wait 2s
   ↓
Attempt 3
   ↓
Success / Failure
```

This prevents transient API failures from immediately causing the entire pipeline to fail.

---

### 5. Raw Data Layer

The first database layer stores the original API response as JSONB.

```sql
CREATE TABLE raw_market_data (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (source, symbol, timestamp)
);
```

Keeping the original payload provides a reliable raw source for downstream transformations and makes the ingestion layer independent from analytical schemas.

---

## Project Structure

```text
DataDOOM/
│
├── src/
│   ├── config/
│   │   ├── settings.py
│   │   └── logging.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── init_db.py
│   │
│   └── ingestion/
│       ├── api_client.py
│       ├── loader.py
│       ├── state.py
│       ├── validation.py
│       ├── schemas.py
│       ├── incremental.py
│       └── run_ingestion.py
│
├── tests/
│   ├── test_connection.py
│   ├── test_validation.py
│   └── test_incremental.py
│
├── dags/
│   └── market_ingestion.py
│
├── dbt/
│   └── ...
│
├── docker/
│   └── ...
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/amirh-far/DataDOOM.git
cd DataDOOM
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=market_data
POSTGRES_USER=pipeline_user
POSTGRES_PASSWORD=pipeline_password
```

### 5. Start PostgreSQL

```bash
docker compose up -d
```

### 6. Initialize the database

```bash
python -m src.database.init_db
```

### 7. Run the ingestion pipeline

```bash
python -m src.ingestion.run_ingestion
```

Example output:

```text
Starting ingestion
Requesting CoinGecko | attempt=1/3
CoinGecko request successful | status=200
Fetched 2 records
Validation complete | valid=2 | rejected=0
Incremental filtering | new=2
Loading complete | inserted=2
Ingestion completed successfully
```

Running it again should produce:

```text
Fetched 2 records
Validation complete | valid=2 | rejected=0
Incremental filtering | new=0
Loading complete | inserted=0
```

This demonstrates the incremental and idempotent behavior of the pipeline.

---

## Testing

Run the test suite with:

```bash
pytest
```

The tests currently cover:

* Database connectivity
* Valid record validation
* Invalid price rejection
* Duplicate record detection
* Incremental record selection
* Existing record filtering

The project will progressively expand its test coverage as additional pipeline components are implemented.

---

## Airflow

Apache Airflow is responsible for orchestrating the ingestion workflow.

The DAG represents the pipeline as a dependency graph:

```text
Extract
   ↓
Validate
   ↓
Incremental Filter
   ↓
Load
```

Airflow provides:

* Scheduling
* Task-level execution
* Retries
* Failure visibility
* Dependency management
* Backfills
* Historical run tracking

The business logic remains inside the Python application while Airflow is responsible for **orchestration rather than data processing logic**.

---

## dbt

The raw PostgreSQL data will be transformed using dbt into structured analytical models.

The planned transformation layer is:

```text
Raw PostgreSQL
      ↓
dbt Staging
      ↓
Cleaned Market Data
      ↓
Analytics Models
      ↓
BI / Analytics
```

dbt will also provide SQL-based data quality tests and model documentation.

---

## Data Quality Strategy

DataDOOM treats data quality as a first-class part of the pipeline.

Planned checks include:

```text
Schema Validation
       ↓
Null Checks
       ↓
Duplicate Detection
       ↓
Timestamp Validation
       ↓
Range Validation
       ↓
Database Constraints
       ↓
dbt Tests
```

The goal is to detect bad data as early as possible instead of allowing invalid records to propagate downstream.

---

## Reliability

The pipeline is designed around several failure scenarios.

### API failure

```text
API Failure
    ↓
Retry
    ↓
Retry
    ↓
Success
```

### Duplicate execution

```text
Same record
    ↓
Incremental check
    ↓
Skip
```

### Database conflict

```text
Duplicate record
    ↓
UNIQUE constraint
    ↓
ON CONFLICT DO NOTHING
```

### Partial failure

Airflow allows failed tasks to be retried independently rather than requiring the entire workflow to be manually restarted.

---

## Roadmap

### Phase 1 — Foundation

* [x] Repository structure
* [x] Dockerized PostgreSQL
* [x] Configuration management
* [x] Database schema
* [x] API client

### Phase 2 — Ingestion

* [x] API extraction
* [x] Raw data storage
* [x] Incremental ingestion
* [x] Idempotent loading
* [x] Retry mechanism
* [x] Structured logging

### Phase 3 — Data Quality

* [x] Pydantic validation
* [x] Duplicate detection
* [x] Validation tests
* [x] Incremental tests
* [ ] Expanded data-quality framework
* [ ] Data-quality metrics

### Phase 4 — Orchestration

* [x] Airflow setup
* [ ] Production DAG
* [ ] Scheduling
* [ ] Task retries
* [ ] Backfills
* [ ] Failure handling

### Phase 5 — Transformation

* [ ] dbt integration
* [ ] Staging models
* [ ] Analytics models
* [ ] SQL tests
* [ ] Data lineage

### Phase 6 — Productionization

* [ ] Containerized Airflow environment
* [ ] Monitoring
* [ ] Alerting
* [ ] Pipeline metrics
* [ ] Improved logging
* [ ] Documentation
* [ ] Performance optimization

### Phase 7 — Scale

Potential future extensions:

* [ ] Object storage with S3/MinIO
* [ ] Parquet data lake layer
* [ ] Partitioned tables
* [ ] Batch optimization
* [ ] Spark for large-scale processing

These technologies will only be introduced where they solve an actual engineering problem rather than being added for the sake of the stack.

---

## Design Principles

DataDOOM follows several principles:

**Correctness over complexity**

The pipeline should first be reliable before introducing distributed systems or unnecessary infrastructure.

**Idempotency by design**

A failed task should be safe to retry.

**Raw data preservation**

The original API payload should remain available for downstream processing.

**Separation of concerns**

```text
Python → ingestion & business logic
PostgreSQL → persistence
Airflow → orchestration
dbt → transformation
```

**Observable pipelines**

Every important stage should expose meaningful metrics such as:

```text
records fetched
records validated
records rejected
records skipped
records inserted
execution duration
```

---

## Why This Project?

DataDOOM is intentionally designed as a **production-style engineering project**, not simply an API-to-database script.

The project demonstrates practical concepts used in modern data and AI infrastructure:

* Reliable data ingestion
* Data quality
* ETL/ELT architecture
* Workflow orchestration
* Database design
* Failure recovery
* Incremental processing
* Reproducible infrastructure
* Analytics-ready data modeling

These capabilities are particularly relevant to building reliable **ML and AI systems**, where model quality depends heavily on the quality and reliability of the underlying data pipelines.



#### For finding user pass for airflow
docker compose exec airflow-apiserver cat /opt/airflow/simple_auth_manager_passwords.json.generated
