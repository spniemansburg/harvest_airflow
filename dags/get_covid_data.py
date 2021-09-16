# dependencies
import requests
import time
import json
import pandas as pd
import psycopg2 as pg
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta, date

#############################################################################
# Extract / Transform
#############################################################################
def fetchDataToLocal():
    """
    we use the python requests library to fetch the nyc in json format, then
    use the pandas library to easily convert from json to a csv saved in the
    local data directory
    """

    # fetching the request
    url = "https://data.rivm.nl/covid-19/COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.json"
    response = requests.get(url)

    # convert the response to a pandas dataframe, then save as csv to the data
    # folder in our project directory
    df = pd.DataFrame(json.loads(response.content))

    # save to csv
    df.to_csv("/data_share/covid_data.csv",index=False)
    
#############################################################################
# Load
#############################################################################
def sqlLoad():
    """
    we make the connection to postgres using the psycopg2 library, create
    the schema to hold our covid data, and insert from the local csv file
    """

    # attempt the connection to postgres
    # Use environment variables for credentials
    try:
        pg_conn = pg.connect(
            database=,
            user=,
            password=,
            host=
        )
    except Exception as error:
        print(error)

    #perform COPY and print result
    cursor = pg_conn.cursor()
    sql = '''
    COPY raw_rivm.covid_data (version, date_of_report, date_of_statistics, region_level, region_code, region_name, birth_year, vaccination_partly, vaccination_completed, age_group)
    FROM '{}'
    DELIMITER ',' CSV HEADER;
    '''

    # Time how long copy takes
    start_time = time.time()
    cursor.execute(sql)
    pg_conn.commit()
    cursor.close()
    print("COPY duration: {} seconds".format(time.time() - start_time))

default_args = {
    "owner": "airflow",
    "start_date": datetime.today() - timedelta(days=1)
}

with DAG(
    "covid_data",
    default_args=default_args,
    schedule_interval = "30 4 * * *",
    ) as dag:

    fetchDataToLocal = PythonOperator(
                task_id="fetch_data_to_local",
                python_callable=fetchDataToLocal
    )

    # Create covid_data table
    createTable = PostgresOperator(
                task_id="create_table",
                postgres_conn_id="postgres_default",
                sql="""
                    CREATE TABLE IF NOT EXISTS raw_rivm.covid_data (
                            version int,
                            date_of_report timestamp,
                            date_of_statistics date,
                            region_level text,
                            region_code text,
                            region_name text,
                            birth_year text,
                            vaccination_partly text,
                            vaccination_completed text,
                            age_group text
                    );
                    TRUNCATE TABLE raw_rivm.covid_data;
                    """
    )

    # Run sqlLoad function
    sqlLoad = PythonOperator(
    )

    # Clean up; remove covid_data.csv
    removeData = BashOperator(
    )

    fetchDataToLocal >> createTable >> sqlLoad >> removeData
