# Deployment Guide

## Local Docker Compose Setup
```bash
make infra
make migrate
make seed
make dev
```

## Production Deployment
Use `docker-compose.prod.yml` or Kubernetes manifests in `infrastructure/kubernetes`.
Ensure PostgreSQL, Neo4j, Redis, MinIO, and Temporal are provisioned with TLS and managed credentials.
