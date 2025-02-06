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

### 2️⃣ Set Up Airflow
Make sure you have **Docker** installed and running. Then, initialize Airflow using:
```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
```

### 3️⃣ Start the Airflow Services
Run the following command to start Airflow and its components:
```bash
docker-compose up
```
This will start the **PostgreSQL**, **Redis**, and **Airflow webserver, scheduler, and worker**.

### 4️⃣ Access the Airflow Web UI
Once the setup is complete, you can access the **Airflow Web UI** by visiting:
```
http://localhost:8080
```
Login with the default credentials:
- **Username:** `airflow`
- **Password:** `airflow`

### 5️⃣ Trigger the DAG
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
