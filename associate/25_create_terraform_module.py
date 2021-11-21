#!/usr/bin/env python3
import os

from sys import argv
from subprocess import run

def create_and_go_to_folder(folder: str):
    os.makedirs(folder, exist_ok=True)
    os.chdir(folder)

def create(filename: str = None, data: str = None) -> None:
    print(f"creating {filename}...")
    with open(filename, 'w') as writer:
        writer.write(data)
    print(f'displaying contents of {filename}...')
    with open(filename) as reader:
        print(reader.read())

def create_module_main_tf():
    create(
        'main.tf',
        '''provider "aws" {
    region = var.region
}

resource "aws_vpc" "this" {
    cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "this" {
    vpc_id = aws_vpc.this.id
    cidr_block = "10.0.1.0/24"
}

data "aws_ssm_parameter" "this" {
    name = "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
}''')

def create_module_variables_tf():
    create(
        'variables.tf',
        '''variable "region" {
    type = "string"
    default = "us-east-1"
}''')

def create_module_outputs_tf():
    create(
        'outputs.tf',
        '''output "subnet_id" {
    value = aws_subnet.this.id
}

output "ami_id" {
    value = data.aws_ssm_parameter.this.value
}''')

def create_project_main_tf():
    create(
        'main.tf',
        '''provider "aws" {
    region = var.main_region
}

module "vpc" {
    source = "./modules/vpc"
    region = var.main_region
}

resource "aws_instance" "my-instance" {
    ami = module.vpc.ami_id
    subnet_id = module.vpc.subnet_id
    instance_type = "t2.micro"
}''')

def create_project_variables_tf():
    create(
        'variables.tf',
        '''variable "main_region" {
    type = string
    default = "us-east-1"
}'''
    )

def create_project_outputs_tf():
    create(
        'outputs.tf',
        '''output "PrivateIP" {
    description = "Private IP of EC2 instance"
    value = aws_instance.my-instance.private_ip
}''')

def terraform(command: str) -> None:
    print(
        run(
            f'terraform {command}', shell=True,
            #capture_output=True
        )
    )

def directory():
    return f'{argv[1]}/modules/vpc'

if __name__ == "__main__":
    print(f"Creating structure {directory()}")
    create_and_go_to_folder(directory())
    print(os.getcwd())
    create_module_main_tf()
    create_module_variables_tf()
    create_module_outputs_tf()
    print(os.getcwd())
    os.chdir('../..')
    print(os.listdir())
    print('Writing Main Terraform Project Code')
    create_project_main_tf()
    create_project_variables_tf()
    create_project_outputs_tf()
    terraform('fmt -recursive')
    terraform('init')
    terraform('validate')
    terraform('plan')