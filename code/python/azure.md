---
description: Frequently used code for azure related code snippets
---

# Azure

**Download blobs locally**

```python
from azure.storage.blob import BlobServiceClient
import os

conn_str = ""
container_name = ""
blob_name = ""
local_path = ""

download_file_path = os.path.join(local_path, blob_name)
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
with open(download_file_path, "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())
```

