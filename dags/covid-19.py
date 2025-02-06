from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import pandas as pd
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
import re



with DAG(
        dag_id='covid-19-processing',
        schedule='@daily',
        start_date=datetime(2022, 1, 1),
        catchup=False
) as dag:

    @task
    def fetch_data():
        '''Fetches the COVID-19 data from the Johns Hopkins University repository and ensures it is up to date.'''
        urls = {
            "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
            "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
            "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
        }
        # Add explicit URL validation
        dfs ={}

        for key, url   in urls.items():
            try:
                # Add explicit logging before the request
                print(f"Fetching data from: {url}")
                
                df = pd.read_csv(url)
                dfs[key]=df
                print("successfully fetched {key} data")
            except Exception as e:
                print(f"Error fetching {key} data: {str(e)}")
                raise 
        for key, df in dfs.items():
            df.to_csv(f'/tmp/{key}.csv', index=False)
        return dfs
    
    @task
    def process(dfs):
        '''Process the data and convert dates to standard format.'''
        processed_dfs = {}
        
        for key, df in dfs.items():
            try:
                # Rename columns
                df = df.rename({
                    'Country/Region': 'country',
                    'Province/State': 'state'
                })
                
                # Handle missing states
                df['Province/State'] = df['Province/State'].fillna('N/A')
                
                # Convert date columns
                date_columns = df.columns[4:]  # First 4 columns are metadata
                df.columns = list(df.columns[:4]) + [
                    pd.to_datetime(c).strftime('%Y-%m-%d') 
                    for c in date_columns
                ]
                
                # Save processed file with safe filename
                safe_key = re.sub(r'\W+', '_', key)
                df.to_csv(f'/tmp/processed_{safe_key}.csv', index=False)
                
                processed_dfs[key] = df
                
            except Exception as e:
                print(f"Error processing {key} data: {str(e)}")
                raise
                
        return processed_dfs    
    
    '''creating tables in postgres'''
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''CREATE TABLE IF NOT EXISTS dim_location (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255),
            state VARCHAR(255),
            UNIQUE(country, state)
                );

            CREATE TABLE IF NOT EXISTS fact_covid_cases (
            id SERIAL PRIMARY KEY,
            date DATE,
            country VARCHAR(255),
            state VARCHAR(255),
            confirmed INT,
            deaths INT,
            recovered INT,
            FOREIGN KEY (country, state) REFERENCES dim_location(country, state)
            );''' )

    @task
    def load_to_postgres(dfs):
        '''Simple function to load COVID data to postgres'''
        try:
            # Connect to postgres
            pg_hook = PostgresHook(postgres_conn_id='postgres')
            conn = pg_hook.get_conn()
            cursor = conn.cursor()

            # For each dataset (confirmed, deaths, recovered)
            for key, df in dfs.items():
                print(f"Loading {key} data")

                
                
                # For each row in the dataframe
                for index, row in df.iterrows():
                    # First insert location if it doesn't exist
                    cursor.execute("""
                        INSERT INTO dim_location (country, state)
                        VALUES (%s, %s)
                        ON CONFLICT (country, state) DO NOTHING
                    """, (row['Country/Region'], row['Province/State']))

                    # Get all date columns (they start after the first 4 columns)
                    date_columns = df.columns[4:]
                    
                    # For each date, insert the data
                    for date in date_columns:
                        value = row[date]
                        
                        # Set the right column based on which dataset we're loading
                        if key == 'confirmed':
                            confirmed, deaths, recovered = value, 0, 0
                        elif key == 'deaths':
                            confirmed, deaths, recovered = 0, value, 0
                        else:  # recovered
                            confirmed, deaths, recovered = 0, 0, value

                        cursor.execute("""
                            INSERT INTO fact_covid_cases 
                                (date, country, state, confirmed, deaths, recovered)
                            VALUES 
                                (%s, %s, %s, %s, %s, %s)
                        """, (date, row['Country/Region'], row['Province/State'], 
                            confirmed, deaths, recovered))

            # Save all changes
            conn.commit()
            cursor.close()
            conn.close()
            print("Finished loading data to PostgreSQL")

        except Exception as e:
            print(f"Error: {str(e)}")
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
            raise 


    data = fetch_data()
    processed_data = process(data)
    load_data = load_to_postgres(processed_data)

    data >> processed_data >> create_table >> load_data
