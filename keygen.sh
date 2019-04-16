#!/bin/bash
aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > /home/ubuntu/MyKeyPair.pem
sudo ssh-keygen -y -f /home/ubuntu/MyKeyPair.pem | cat > /home/ubuntu/.ssh/authorized_keys
sudo systemctl restart ssh

