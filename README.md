# COVID-19 Case Data Cleansing & Modeling with Apache Airflow

## 🚀 Project Overview
I have recently completed my learning journey in **Apache Airflow** and applied my knowledge by working on a project: **COVID-19 Case Data Cleansing & Modeling**. This project is part of my hands-on learning approach to ensure I am on the right track while reinforcing my skills through practical implementation.

## 📌 Project Goals
- Ingest raw COVID-19 case data.
- Cleanse and preprocess the dataset.
- Transform the data into a structured format suitable for analysis.
- Automate the workflow using Apache Airflow.

## 🔧 Tech Stack
- **Apache Airflow** (for workflow automation)
- **Docker** (for containerized execution)
- **PostgreSQL** (for data storage)
- **Pandas** (for data manipulation)

## 📂 Repository Structure
```
📦 airflow-covid19-data-pipeline
 ┣ 📂 dags                 # Airflow DAGs (data pipeline workflows)
 ┣ 📂 scripts              # Custom scripts for data processing
 ┣ 📂 logs                 # Airflow logs
 ┣ 📂 plugins              # Airflow plugins (if any)
 ┣ 📄 .env                 # Environment variables (Airflow image & UID)
 ┣ 📄 airflow.cfg          # Airflow configuration file
 ┣ 📄 docker-compose.yaml  # Docker configuration for Airflow setup
 ┗ 📄 README.md            # Project documentation
```

## 🛠 How to Run the Project Locally
If you want to test or run this project on your own machine, follow these steps:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/hesham942/airflow-covid19-data-pipeline.git
cd airflow-covid19-data-pipeline
```

### 2️⃣ Setting Up Apache Airflow
During my learning process, I set up Airflow using **Docker Compose**. Instead of manually creating folders like `dags/`, `scripts/`, and others, I followed these steps to automate the setup:

1. I copied the **Docker Compose** file from my instructor and placed it in my project directory.
2. I created a `.env` file in the same directory with the following content:

```bash
AIRFLOW_IMAGE_NAME=apache/airflow:2.7.0
AIRFLOW_UID=50000
```

3. I ran the following command to start Airflow and automatically generate the required folders:

```bash
docker-compose up -d
```

This command automatically created the necessary folders (`dags/`, `logs/`, `plugins/`, etc.), so I didn't have to set them up manually.

### 3️⃣ Access the Airflow Web UI
Once the setup is complete, you can access the **Airflow Web UI** by visiting:
```
http://localhost:8080
```
Login with the default credentials:
- **Username:** `airflow`
- **Password:** `airflow`

### 4️⃣ Trigger the DAG
In the Airflow UI, enable and trigger the **COVID-19 Case Data Pipeline DAG** to start the workflow.

## 📈 Expected Output
- The pipeline fetches COVID-19 case data.
- Cleans and structures the data.
- Stores the transformed data in PostgreSQL for further analysis.

## 🏆 Key Takeaways
- **Gained hands-on experience** with Airflow DAGs and task dependencies.
- **Improved data engineering skills** by automating ETL pipelines.
- **Built a reusable Airflow setup** using Docker and PostgreSQL.

---
