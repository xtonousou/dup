# dup (under development)
A (dockerized) tool to check for newer Docker images of your running containers and notify you

## Installation

### Docker

You can either run it with docker:

```bash
docker run xtonousou/dup:latest \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v ./dup.env:/app/dup.env:ro \
    -v ./dup.creds.env:/app/dup.creds.env:ro \
    --restart unless-stopped
```

Or with compose:

```bash
docker compose up -d
```
