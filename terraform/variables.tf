variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-north-1"
}

variable "ami_id" {
  description = "Ubuntu AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name"
  type        = string
}

variable "allowed_ip" {
  description = "Public IP allowed to access SSH, Grafana and Prometheus"
  type        = string
}