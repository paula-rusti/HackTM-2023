docker build --platform linux/amd64 . -t registry.digitalocean.com/piemakers/ingester:latest
docker push registry.digitalocean.com/piemakers/ingester:latest