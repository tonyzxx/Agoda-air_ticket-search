# Agoda Air Ticket Search and Notification
- Found air ticket under price threshold and sent mail to your mail box

## Build Docker Image

```
sh build.sh
```

## Run with Docker Image

```
docker run -v $(pwd):/app --rm ticket-search:1.0.2 python3 main.py
```
