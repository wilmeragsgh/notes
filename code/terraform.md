---
description: Frequently used terraform snippets

---

# Terraform

## One-liners

Validate configurations: `terraform validate`

Start terraform config: `terraform init`

Give format to files within direcoty `terrafom fmt`



## Frecuently used AMI IDs

- **Ubuntu server 18.04 (HVM) 64bits x86**: `ami-0a63f96e85105c6d3`

## Recipes

**Setup AWS instances**

1. Get AWS access key/AWS secret key 
2. execute `aws configure`  using credentials from 1.
3. execute `terraform init` when starting new project at the root of the directory

**Get list of AMI IDs matching criteria**

```terraform
variable "image_name" {
    description = "The name of the image to use"
    default = "ubuntu-*-18.04*"
}

provider "aws" {
    region = "us-east-2"
}

data "aws_ami" "images" {
    owners = ["amazon"]
    most_recent = true
    filter {
      name = "name"
      values = [var.image_name]
    }
}

output "ids" {
    value = "\nName: ${data.aws_ami.images.name}\nId: ${data.aws_ami.images.id}"

```

**Single ec2 with ubuntu 18.04 x86**

```terraform
variable "key_name" {
    description = "Key to use for accessing the instance"
}

variable "sec_group" {
    description = "Security group for the instance"
}

variable "instance_name" {
    description = "Instance's name"
}

provider "aws" {
    region = "us-east-2"
}

resource "aws_instance" "example" {
	ami = "ami-f4f4cf91"
	instance_type = "t2.micro"
	key_name = var.key_name
	vpc_security_group_ids = var.sec_group
	tags = {
		Name = var.instance_name
	}
}

output "public_ip" {
    value = "Created instance (public_dns):  ${aws_instance.example.public_dns}"
}
```

**Create a security group and use it afterwards (Allow income from 8080)**

```terraform
resource "aws_security_group" "http_group" {
    name = "terraform-example-instance"
    ingress {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# add the property 
# vpc_security_group_ids = ["${aws_security_group.http_group.id}"] 
# in the aws_instance
```

**Create a security group for ssh access (Experimental)**

```terraform
resource "aws_security_group" "ssh_group" {
    name = "terraform-example-instance"
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# add the property 
# vpc_security_group_ids = ["${aws_security_group.ssh_group.id}"] 
# in the aws_instance
```



## References

- [Terraform up and running (local book)](/media/w/6529BB496A1EC696/Yevgeniy Brikman - Terraform  Up and Running (Early Release)-O'Reilly Media (2017).pdf)
- https://learn.hashicorp.com/terraform/getting-started/build
- http://blog.shippable.com/setup-a-container-cluster-on-aws-with-terraform-part-2-provision-a-cluster