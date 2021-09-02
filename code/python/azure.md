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

**List files/folders in blob**

```python
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#Create a Blob Storage Account client

connect_str = <connectionstring>
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
#Create a container client

container_name="dummy"
container_client=blob_service_client.get_container_client(container_name)
#This will list all blobs in the container inside dir1 folder/directory

blob_list = container_client.list_blobs(name_starts_with="dir1/")
for blob in blob_list:
	print("\t" + blob.name)
```

