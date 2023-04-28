#!/usr/bin/env bash
#Settinng up server

# Install Nginx if it is not already installed
if [ $(dpkg-query -W -f='${Status}' nginx 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  sudo apt-get update
  sudo apt-get -y install nginx
fi

# Create the necessary folders if they don't exist
sudo mkdir -p /data/web_static/{releases,test,shared}

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
    <title>Testing Nginx</title>
  </head>
  <body>
    <p>Testing Nginx configuration</p>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/listen 80 default_server;/a \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
