@echo off
REM Windows batch script to start RAGFlow with RDS MySQL

echo 🚀 Starting RAGFlow with AWS RDS MySQL
echo ======================================

REM Copy environment file
echo 📋 Setting up environment...
copy docker\ragflow.env docker\.env

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose -f docker\docker-compose.yml down 2>nul

REM Start RAGFlow with host networking (bypasses Docker network issues)
echo 🐳 Starting RAGFlow with host networking...
docker run -d ^
  --name ragflow-server ^
  --network host ^
  -v "%cd%\docker\ragflow-logs:/ragflow/logs" ^
  -v "%cd%\conf\service_conf.yaml:/ragflow/conf/service_conf.yaml" ^
  -v "%cd%\history_data_agent:/ragflow/history_data_agent" ^
  -e TZ=UTC ^
  -e HF_ENDPOINT=https://huggingface.co ^
  --restart on-failure ^
  infiniflow/ragflow:v0.20.5

REM Wait for startup
echo ⏳ Waiting for RAGFlow to start...
timeout /t 15 /nobreak

REM Check if container is running
echo 📊 Checking container status...
docker ps --filter "name=ragflow-server"

REM Show recent logs
echo 📝 Recent RAGFlow logs:
docker logs ragflow-server --tail 20

echo.
echo ✅ RAGFlow should be accessible at: http://localhost:9380
echo 🔍 To see live logs: docker logs -f ragflow-server
