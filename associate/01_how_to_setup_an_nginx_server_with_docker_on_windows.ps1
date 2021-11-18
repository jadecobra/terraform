projectName="nginx-docker-container"
mkdir $projectName
cd $projectName

cat << EOF > main.tf
terraform {
    required_providers {
        docker = {
            source = "kreuzwerker/docker"
            version = ">= 2.13.0"
        }
    }
}

provider "docker" {
    host = "npipe:////.//pipe//docker_engine"
}

resource "docker_image" "nginx" {
    name = "nginx:latest"
    keep_locally = false
}

resource "docker_container" "nginx" {
    image = docker_image.nginx.latest
    name = "tutorial"
    ports {
        internal = 80
        external = 8000
    }
}
EOF

open -a Docker
terraform init
terraform plan
terraform apply

curl localhost:8000
python -m webbrowser localhost:8000

terraform destroy