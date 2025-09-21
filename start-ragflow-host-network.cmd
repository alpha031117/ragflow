@echo off
echo 🚀 Starting RAGFlow with Host Networking for RDS Access
echo =====================================================

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker stop ragflow-server 2>nul
docker rm ragflow-server 2>nul

REM Create necessary directories
echo 📁 Creating log directories...
if not exist "docker\ragflow-logs" mkdir "docker\ragflow-logs"

REM Start RAGFlow with host networking
echo 🐳 Starting RAGFlow with host networking...
docker run -d ^
  --name ragflow-server ^
  --network host ^
  -v "%cd%\conf\service_conf.yaml:/ragflow/conf/service_conf.yaml" ^
  -v "%cd%\docker\ragflow-logs:/ragflow/logs" ^
  -v "%cd%\history_data_agent:/ragflow/history_data_agent" ^
  -e TZ=UTC ^
  -e HF_ENDPOINT=https://huggingface.co ^
  --restart on-failure ^
  infiniflow/ragflow:v0.20.5

REM Wait for startup
echo ⏳ Waiting for RAGFlow to start...
timeout /t 15 /nobreak

REM Check status
echo 📊 Checking container status...
docker ps --filter "name=ragflow-server"

REM Test RDS connectivity from container
echo 🔍 Testing RDS connectivity from container...
docker exec ragflow-server python -c "import socket; sock = socket.create_connection(('legalkaki-rds.c14i40gw8ua8.ap-southeast-5.rds.amazonaws.com', 3306), timeout=5); print('✅ RDS is reachable!'); sock.close()" 2>nul || echo "❌ RDS not reachable from container"

REM Show logs
echo 📝 Recent RAGFlow logs:
docker logs ragflow-server --tail 10

echo.
echo ✅ RAGFlow should be accessible at: http://localhost:9380
echo 🔍 To see live logs: docker logs -f ragflow-server
echo 🛑 To stop: docker stop ragflow-server
