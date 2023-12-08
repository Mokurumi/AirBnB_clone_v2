#!/usr/bin/env bash
# This script sets up web servers for deployment of web traffic

# Check if Nginx is installed, install if not
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html

# Add content to the test HTML file
echo "<html><head><title>Test Page</title></head><body>This is a test page.</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Remove existing symbolic link and create a new one
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of directories to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"

sudo sed -i '/location \/hbnb_static\/ {/a \\talias /data/web_static/current/;' "$nginx_config"
sudo sed -i '/location \/hbnb_static\/ {/a \\t}' "$nginx_config"

# Restart Nginx
sudo service nginx restart
