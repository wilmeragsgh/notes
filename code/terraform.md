---
description: Frequently used terraform snippets

---

# Terraform

## Recipes

**Get list of AMI IDs matching criteria**

```terraform
data "aws_ami_ids" "ubuntu" {
  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/ubuntu-*-*-amd64-server-*"]
  }
}
```

**Single ec2 with ubuntu 16**

```terraform
resource "aws_instance" "example" {
	ami = "ami-40d28157"
	instance_type = "t2.micro"
	user_data = <<-EOF
				#!/bin/bash
				echo "Hello, World" > index.html
				nohup busybox httpd -f -p 8080 &
				EOF
	tags {
		Name = "terraform-example"
	}
}
```



## References

- [Terraform up and running (local book)](/media/w/6529BB496A1EC696/Yevgeniy Brikman - Terraform  Up and Running (Early Release)-O'Reilly Media (2017).pdf)
- https://learn.hashicorp.com/terraform/getting-started/build
- http://blog.shippable.com/setup-a-container-cluster-on-aws-with-terraform-part-2-provision-a-cluster