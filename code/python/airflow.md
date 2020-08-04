---
description: Frequently used code for airflow related code snippets

---

# Airflow

## Guidelines

- By using *DockerOperators*/*KubernetesOperators* only we can avoid the technical debt that would existing by using different operators, and the dependency on Airflow development of operators([more on this](https://medium.com/bluecore-engineering/were-all-using-airflow-wrong-and-how-to-fix-it-a56f14cb0753)).

## Recipes

**Activate the execution of a DAG**

`airflow unpause dag_id`

**Setting it up in Amazon linux AMI**

```bash
#!/bin/bash
SLUGIFY_USES_TEXT_UNIDECODE=yes pip install apache-airflow[s3,postgres]

# sudo su
yum install postgresql postgresql-contrib postgresql-server
/etc/init.d/postgresql92 initdb
/etc/init.d/postgresql92 start
# or required version

AIRFLOW_USER=user
AIRFLOW_PASS=pass
AIRFLOW_DB=airflow
AIRFLOW_HOME=~/airflow
AIRFLOW_SQL_ALCHEMY_CONN=postgresql+psycopg2://"$AIRFLOW_USER":"$AIRFLOW_PASS"@localhost:5432/"$AIRFLOW_DB"

echo "CREATE USER ${AIRFLOW_USER} PASSWORD '${AIRFLOW_PASS}'; CREATE DATABASE ${AIRFLOW_DB}; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${AIRFLOW_USER}; ALTER ROLE ${AIRFLOW_USER} SUPERUSER; ALTER ROLE ${AIRFLOW_USER} CREATEDB; ALTER ROLE ${AIRFLOW_USER} WITH LOGIN;" | sudo -u postgres psql

## on /var/lib/pgsql92/data/pg_hba.conf
# put:
#host    all             all             0.0.0.0/0            trust on IPv4 local connection
sudo -u postgres sed -i "s|127.0.0.1/32|0.0.0.0/0|" /var/lib/pgsql92/data/pg_hba.conf # /etc/postgresql/10/main/pg_hba.conf ubuntu

# on /var/lib/pgsql92/data/postgresql.conf
# put:
# listen_addresses = '*'
sudo -u postgres sed -i "s|#listen_addresses = 'localhost'|listen_addresses = '*'|" /var/lib/pgsql92/data/postgresql.conf

#then
sudo /etc/init.d/postgresql92 restart

sudo echo "AIRFLOW_HOME=${AIRFLOW_HOME}" >> /etc/environment 

SLUGIFY_USES_TEXT_UNIDECODE=yes pip install apache-airflow[postgres] # or s3
# pip install -U pip setuptools wheel psycopg2 Cython pytz pyOpenSSL ndg-httpsclient pyasn1 psutil apache-airflow[postgres]
# for venv

airflow initdb
# on AIRFLOW_HOME/airflow.cfg
# put:
# executor = LocalExecutor
# sql_alchemy_conn = postgresql+psycopg2://af_user:af_pass@localhost:5432/airflow
sed -i "s|executor = .*|executor = LocalExecutor|g" "$AIRFLOW_HOME"/airflow.cfg
sed -i "s|sql_alchemy_conn = .*|sql_alchemy_conn = $AIRFLOW_SQL_ALCHEMY_CONN|g" "$AIRFLOW_HOME"/airflow.cfg
sed -i "s|load_examples = .*|load_examples = False|g" "$AIRFLOW_HOME"/airflow.cfg
airflow initdb

#Always run webserver and then scheduler

airflow webserver

airflow scheduler 
```



### Setup a cluster

#### Pre-Requisites

- The following nodes are available with the given host names:

  - master1: Will have the role(s): Web Server, Scheduler
  - master2: Will have the role(s): Web Server
  - worker1: Will have the role(s): Worker
  - worker2: Will have the role(s): Worker

- A Queuing Service is Running. (RabbitMQ, AWS SQS, etc)

  - You can install RabbitMQ by following these instructions: 

    Installing RabbitMQ

    - If you’re using RabbitMQ, it is recommended that it is also setup to be a cluster for High Availability. Setup a Load Balancer to proxy requests to the RabbitMQ instances.

## Comments

- Scale workers vertically by providing higher values to `celeryd_concurrency`

## References

- http://site.clairvoyantsoft.com/setting-apache-airflow-cluster/
- https://github.com/jghoman/awesome-apache-airflow
- https://tech.scribd.com/blog/2020/breaking-up-the-dag-repo.html **
- https://azure.microsoft.com/sv-se/blog/deploying-apache-airflow-in-azure-to-build-and-run-data-pipelines/
- https://gtoonstra.github.io/etl-with-airflow/
- https://medium.com/databand-ai/improving-performance-of-apache-airflow-scheduler-507f4cb6462a
- http://agrajmangal.in/blog/big-data/running-airflow-on-top-of-apache-mesos/
- https://marclamberti.com/blog/how-to-use-dockeroperator-apache-airflow/
- https://www.adaltas.com/en/2020/05/05/tutorial-apache-airflow-aws/
- https://towardsdatascience.com/how-to-deploy-apache-airflow-with-celery-on-aws-ce2518dbf631
- https://www.statworx.com/de/blog/a-framework-to-automate-your-work-how-to-set-up-airflow/
- [Installing Airflow with CeleryExcuter, using PostgreSQL as metadata database and Redis for Celery message broker · GitHub](https://gist.github.com/zacgca/9e0401aa205e7c54cbae0e85afca479d)
- [Apache Airflow Installation on Ubuntu – taufiq ibrahim – Medium](https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14)
- https://www.astronomer.io/guides/airflow-executors-explained/
- https://www.astronomer.io/guides/dynamically-generating-dags/