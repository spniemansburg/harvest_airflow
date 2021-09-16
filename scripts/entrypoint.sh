#!/usr/bin/env bash
: "${POSTGRES_HOST:="$AIRFLOW_DB_HOST"}"
: "${POSTGRES_PORT:="5432"}"
: "${POSTGRES_USER:="$AIRFLOW_DB_USER"}"
: "${POSTGRES_PASSWORD:="$AIRFLOW_DB_PASS"}"
: "${POSTGRES_DB:="airflow"}"
: "${AIRFLOW__CORE__EXECUTOR:="LocalExecutor"}"
: "${AIRFLOW__CORE__LOAD_EXAMPLES:="False"}"

# Defaults and back-compat
: "${AIRFLOW__CORE__SQL_ALCHEMY_CONN:="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"}"

export AIRFLOW__CORE__SQL_ALCHEMY_CONN
export AIRFLOW__CORE__EXECUTOR
export AIRFLOW__CORE__LOAD_EXAMPLES

# Initialize db
airflow db upgrade

# FIRST TIME
#airflow users create -r Admin -u "$SECURITY__ADMIN_USERNAME" -e "$SECURITY__ADMIN_EMAIL" -f "$SECURITY__ADMIN_FIRSTNAME" -l "$SECURITY__ADMIN_LASTNAME" -p "$SECURITY__ADMIN_PASSWORD"

# Run scheduler 
airflow scheduler &

# Run webserver
exec airflow webserver