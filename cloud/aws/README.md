# AWS



## S3

**Move data from a source region bucket to a new region (and bucket) **

```bash
aws s3 sync s3://oldbucket s3://newbucket --source-region us-west-1 --region us-west-2
```





**Expanding size of a running EC2**

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html



**Create snapshot of volume**

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-creating-snapshot.html