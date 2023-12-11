# Installation

- Clone this repo

- Install [docker](https://docs.docker.com/engine/install/) if you haven't already.

- Run the following on root to build the docker image:

```bash
docker compose -f docker-compose.yml build
```

- Finally mount the container:

```bash
docker compose up -d
```

The container waits 10 seconds so the database can be initialized correctly. Move the value if you need more time.