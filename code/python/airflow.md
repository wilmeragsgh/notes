---
description: Frequently used code for airflow related code snippets

---

# Airflow

## Guidelines

- By using *DockerOperators*/*KubernetesOperators* only we can avoid the technical debt that would existing by using different operators, and the dependency on Airflow development of operators([more on this](https://medium.com/bluecore-engineering/were-all-using-airflow-wrong-and-how-to-fix-it-a56f14cb0753)).

## How-to

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

## Links

- http://site.clairvoyantsoft.com/setting-apache-airflow-cluster/
- https://github.com/jghoman/awesome-apache-airflow
- https://tech.scribd.com/blog/2020/breaking-up-the-dag-repo.html
- https://azure.microsoft.com/sv-se/blog/deploying-apache-airflow-in-azure-to-build-and-run-data-pipelines/
- https://gtoonstra.github.io/etl-with-airflow/
- https://medium.com/databand-ai/improving-performance-of-apache-airflow-scheduler-507f4cb6462a
- http://agrajmangal.in/blog/big-data/running-airflow-on-top-of-apache-mesos/
- https://marclamberti.com/blog/how-to-use-dockeroperator-apache-airflow/
- https://www.adaltas.com/en/2020/05/05/tutorial-apache-airflow-aws/
- https://towardsdatascience.com/how-to-deploy-apache-airflow-with-celery-on-aws-ce2518dbf631