# COVID-19 Data Pipeline — Apache Airflow

An automated ETL pipeline that ingests, cleanses, and loads **950K+ data points** from the Johns Hopkins COVID-19 time-series datasets into a star-schema PostgreSQL database, orchestrated by Apache Airflow on a daily schedule.

## Architecture

```
Johns Hopkins CSVs ──► fetch_data ──► process ──► create_table ──► load_to_postgres
 (confirmed,                │            │              │                  │
  deaths,              Download 3    Clean columns,  Create dim &     Insert into
  recovered)           CSV files     reformat dates  fact tables      PostgreSQL
```

**Data source:** [JHU CSSE COVID-19 Dataset](https://github.com/CSSEGISandData/COVID-19) — 3 global time-series CSVs (confirmed, deaths, recovered), each with ~289 country/region rows and ~1,100 date columns.

## Pipeline Details

| Aspect | Detail |
|---|---|
| **DAG** | `covid-19-processing` |
| **Schedule** | `@daily` |
| **Tasks** | 4 (fetch → process → create tables → load) |
| **Data volume** | ~950K+ data points per run |
| **Storage model** | Star schema — `dim_location` + `fact_covid_cases` |
| **Executor** | CeleryExecutor with Redis broker |

### Task Breakdown

1. **`fetch_data`** — Downloads confirmed, deaths, and recovered CSV datasets from Johns Hopkins.
2. **`process`** — Renames columns, fills missing province/state values, and converts date headers to `YYYY-MM-DD` format.
3. **`create_table`** — Creates `dim_location` (dimension) and `fact_covid_cases` (fact) tables with referential integrity.
4. **`load_to_postgres`** — Iterates through each dataset and date column, inserting records into the star-schema model.

## Tech Stack

- **Apache Airflow 2.7.0** — Workflow orchestration
- **PostgreSQL 13** — Data warehouse
- **Redis** — Celery broker for task distribution
- **Pandas** — Data manipulation and cleansing
- **Docker Compose** — Containerized multi-service deployment

## Getting Started

### Prerequisites

- Docker & Docker Compose
- At least 4 GB RAM allocated to Docker

### Run

```bash
git clone https://github.com/Hesham942/airflow-covid19-pipeline.git
cd airflow-covid19-pipeline
docker-compose up -d
```

The Airflow UI will be available at `http://localhost:8080` (default credentials: `airflow` / `airflow` — local development only).

Enable and trigger the `covid-19-processing` DAG from the UI.

## Project Structure

```
airflow-covid19-pipeline/
├── dags/
│   └── covid-19.py          # DAG definition with 4 tasks
├── logs/                     # Airflow task logs
├── plugins/                  # Airflow plugins
├── .env                      # Airflow image & UID config
└── docker-compose.yaml       # Multi-container setup
```

## Database Schema

```sql
-- Dimension table
dim_location (id, country, state)

-- Fact table
fact_covid_cases (id, date, country, state, confirmed, deaths, recovered)
```
