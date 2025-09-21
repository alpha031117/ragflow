# Running RAGFlow with AWS RDS MySQL

## Overview

This guide shows how to run RAGFlow using your AWS RDS MySQL instance instead of the default local MySQL container.

## Prerequisites

✅ AWS RDS MySQL instance is running and accessible  
✅ Database `rag_flow` exists on RDS  
✅ Security groups allow connection on port 3306  
✅ Docker and Docker Compose are installed

## Steps

### 1. Copy Environment File

```bash
# Copy the environment file to the correct location
cp docker/ragflow.env docker/.env
```

### 2. Start RAGFlow Services (without MySQL)

```bash
# Start RAGFlow with RDS configuration
docker-compose -f docker-compose-rds.yml up -d

# Or if you prefer to see logs in real-time:
docker-compose -f docker-compose-rds.yml up
```

### 3. Check Container Status

```bash
# Check if containers are running
docker-compose -f docker-compose-rds.yml ps

# Check RAGFlow logs
docker-compose -f docker-compose-rds.yml logs ragflow
```

### 4. Access RAGFlow

Once started successfully, access RAGFlow at:

- **Main Interface**: http://localhost:9380
- **Alternative**: http://localhost (if port 80 is configured)

## Troubleshooting

### If Connection Still Fails:

1. **Check Container Network Access**:

```bash
# Test RDS connectivity from within the container
docker exec ragflow-server ping legalkaki-rds.c14i40gw8ua8.ap-southeast-5.rds.amazonaws.com
```

2. **Check Environment Variables**:

```bash
# Verify environment variables in container
docker exec ragflow-server env | grep MYSQL
```

3. **Check Configuration**:

```bash
# Check the actual configuration file used by RAGFlow
docker exec ragflow-server cat /ragflow/conf/service_conf.yaml
```

### Common Issues:

- **DNS Resolution**: Container might not be able to resolve RDS hostname
- **Network Isolation**: Docker network might block external connections
- **Firewall**: Host firewall might block container's outbound connections

### Solutions:

1. **Add DNS Resolution**:

```bash
# Add to docker-compose-rds.yml under ragflow service:
extra_hosts:
  - "legalkaki-rds.c14i40gw8ua8.ap-southeast-5.rds.amazonaws.com:43.217.205.15"
```

2. **Use Bridge Network Mode**:

```bash
# Add to docker-compose-rds.yml under ragflow service:
network_mode: bridge
```

## Configuration Files Used

- **Environment**: `docker/ragflow.env` → `docker/.env`
- **Docker Compose**: `docker-compose-rds.yml`
- **Service Config**: `docker/service_conf.yaml.template`

## Database Configuration

The following environment variables configure the RDS connection:

- `MYSQL_HOST=legalkaki-rds.c14i40gw8ua8.ap-southeast-5.rds.amazonaws.com`
- `MYSQL_USER=admin`
- `MYSQL_PASSWORD=legalkaki`
- `MYSQL_DBNAME=rag_flow`
- `MYSQL_PORT=3306`
