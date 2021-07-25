---
description: Frequently used code for requests related code snippets
---

# requests

## Authentication

**Basic**

```python
import requests

from requests.auth import HTTPBasicAuth
requests.get('URL', auth=HTTPBasicAuth('username', 'password'))
#or
import base64
requests.get('URL', headers={"Authorization":"Basic %s" % base64.b64encode("username:password".encode("ascii"))}) # when base 64 encoding is required
```

**Bearer**

```python
import requests
requests.get("URL",headers={"Authorization":"Bearer %s" % token})
```

**Try/catch requests**

```python
url='http://www.google.com/blahblah'

try:
    r = requests.get(url,timeout=3)
    r.raise_for_status()
except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
```



## Other utils

### References

https://devhints.io/httpie

https://testdriven.io/blog/asynchronous-tasks-with-falcon-and-celery/

https://www.python-httpx.org/ (Seems really interesting for async requests)
