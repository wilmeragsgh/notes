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

