---
description: python code for interacting with db
---

# Databases

## Recipes

### psycopg2

**Installation**

`pip install psycopg2`

**Establishing connection**

```python
​
```

import psycopg2 try: connection = psycopg2.connect\(DATABASE\_URL\) cursor = connection.cursor\(\)

```text
# Print PostgreSQL Connection properties
print ( connection.get_dsn_parameters(),"\n")
# Print PostgreSQL version
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record,"\n")
```

except \(Exception, psycopg2.Error\) as error : print \("Error while connecting to PostgreSQL", error\) finally:

```text
#closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
```

​\`\`\`

\`\`\`

