---
description: Frequently used terraform snippets
---

# Terraform

## One-liners

Validate configurations: `terraform validate`

Start terraform config: `terraform init`

Give format to files within direcoty `terrafom fmt`

Execute terraform `terraform apply --auto-approve`

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

**Create and attach ebs storage**

aws_ebs_volume and aws_instance ideally belong to the same availability_zone

```terraform
resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = "${aws_ebs_volume.example.id}"
  instance_id = "${aws_instance.web.id}"
}

resource "aws_instance" "web" {
  ami               = "ami-21f78e11"
  availability_zone = "us-west-2a"
  instance_type     = "t1.micro"

  tags = {
    Name = "HelloWorld"
  }
}

resource "aws_ebs_volume" "example" {
  availability_zone = "us-west-2a"
  size              = 1
}
```

**Define storage from ec2 creation**

```terraform
variable "EC2_ROOT_VOLUME_SIZE" {
  type    = "string"
  default = "30"
  description = "The volume size for the root volume in GiB"
}
variable "EC2_ROOT_VOLUME_TYPE" {
  type    = "string"
  default = "gp2"
  description = "The type of data storage: standard, gp2, io1"
}
variable "EC2_ROOT_VOLUME_DELETE_ON_TERMINATION" {
  default = true
  description = "Delete the root volume on instance termination."
}

# then

resource "aws_instance" "example" {
  ami           = "${var.AMI_ID}"
  instance_type = "${var.EC2_INSTANCE_SIZE}"
  
  root_block_device {
    volume_size           = "${var.EC2_ROOT_VOLUME_SIZE}"
    volume_type           = "${var.EC2_ROOT_VOLUME_TYPE}"
    delete_on_termination = "${var.EC2_ROOT_VOLUME_DELETE_ON_TERMINATION}"
  }
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

**Stoping/Starting instances with AWS CLI**

```bash
aws ec2 stop-instances --region us-east-2 --instance-ids i-0123456789abcdef

aws ec2 start-instances --region us-east-2 --instance-ids i-0123456789abcdef

#If you need to fetch the instance ID quickly, you can define a TF output and get at it that way:
terraform output id
#    i-0123456789abcdef
```





## References

- [Terraform up and running (local book)](/media/w/6529BB496A1EC696/Yevgeniy Brikman - Terraform  Up and Running (Early Release)-O'Reilly Media (2017).pdf)
- https://learn.hashicorp.com/terraform/getting-started/build
- http://blog.shippable.com/setup-a-container-cluster-on-aws-with-terraform-part-2-provision-a-cluster
- https://towardsdatascience.com/seamlessly-integrated-deep-learning-environment-with-terraform-google-cloud-gitlab-and-docker-faee4b351e94