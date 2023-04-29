#!/usr/bin/env bash
# setting up everything 

# Install Nginx if not already installed
if [ ! -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create required directories and files
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html
echo "Hello, World!" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link if it doesn't exist
if [ ! -L /data/web_static/current ]; then
    sudo ln -s /data/web_static/releases/test /data/web_static/current
fi

# Set ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '39i\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
