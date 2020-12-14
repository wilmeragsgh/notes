---
description: Frequently used code for Elasticsearch

---

# Elasticsearch

> Using httpie library for the requests

**Create an Index**

```bash
http PUT HOST:PORT/{index-name}/_alias/{alias-name}
```

**Check if index exists**

```bash
http GET HOST:PORT/{index-name}
# The resultant status code would tell if found(200, or 404)
```

**Get index with a given alias**

```bash
http GET HOST:PORT/_alias/{alias-name}
```

**Delete an Index**

```bash
http DELETE HOST:PORT/{index-name}
```



## References

- https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html#indices-aliases-api-add-alias-ex