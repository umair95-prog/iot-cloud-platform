output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.iot_platform_server.public_ip
}

output "fastapi_url" {
  description = "FastAPI dashboard URL"
  value       = "http://${aws_instance.iot_platform_server.public_ip}:8000"
}

output "grafana_url" {
  description = "Grafana URL"
  value       = "http://${aws_instance.iot_platform_server.public_ip}:3000"
}

output "prometheus_url" {
  description = "Prometheus URL"
  value       = "http://${aws_instance.iot_platform_server.public_ip}:9090"
}