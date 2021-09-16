FROM apache/airflow:2.1.2-python3.7
###upgrade pip
RUN python3 -m pip install --upgrade pip

USER root

### AIRFLOW SETUP
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
RUN mkdir /usr/local/airflow
RUN chown -R airflow: ${AIRFLOW_USER_HOME}
WORKDIR ${AIRFLOW_USER_HOME}

### INSTALL TOOLS
RUN apt-get update \
	&& apt-get -y install libaio-dev \
	&& apt-get install postgresql-client \
	&& apt-get -y install gdal-bin

# add startup scripts
COPY scripts /opt/startup
RUN chmod -R +x /opt/startup

# add dags and scripts
ADD dags dags/

USER airflow

ENTRYPOINT ["/opt/startup/entrypoint.sh"]