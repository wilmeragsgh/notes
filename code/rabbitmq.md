---
description: Frequently used code for rabbitmq related code snippets
---

# RabbitMQ



## Recipes

**Docker-compose usage**

When using a Docker image like the following:

```dockerfile
rabbitmq-server:
  image: "rabbitmq:3-management"
  hostname: "rabbitmq-host"
  environment:
    RABBITMQ_ERLANG_COOKIE: "SWQOKODSQALRPCLNMEQG"
    RABBITMQ_DEFAULT_USER: "test"
    RABBITMQ_DEFAULT_PASS: "test"
    RABBITMQ_DEFAULT_VHOST: "/"
  ports:
    - "15672:15672"
    - "5672:5672"
```

The host name for the service from other container would be `rabbitmq-server` and credentials would need to be passed to it, as follows:

```python
import pika
credentials = pika.PlainCredentials('test','test')
conn_params = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(conn_params)
# publish
try:
    channel = connection.channel()
    channel.exchange_declare(exchange="name", exchange_type="fanout")
    channel.basic_publish(
        exchange="name", routing_key="", body=payload_json
    )
finally:
    connection.close()
# many consumer 
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.exchange_declare(exchange="name", exchange_type="fanout")
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange="name", queue=queue_name)
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=False
)
channel.start_consuming()
```





## References

- https://codeburst.io/get-started-with-rabbitmq-on-docker-4428d7f6e46b
- http://site.clairvoyantsoft.com/installing-rabbitmq/
- https://www.rabbitmq.com/tutorials/tutorial-one-python.html
- https://groups.google.com/forum/#!topic/rabbitmq-users/OVrBuAme9VI

