@echo off
echo 🔧 Testing RAGFlow with RDS MySQL Fix
echo =====================================

echo 📋 Step 1: Setting up environment...
copy docker\ragflow.env docker\.env

echo 🛑 Step 2: Stopping existing containers...
docker-compose -f docker\docker-compose.yml down 2>nul

echo 🐳 Step 3: Starting RAGFlow with RDS configuration...
docker-compose -f docker-compose-rds-correct.yml up -d

echo ⏳ Step 4: Waiting for services to start...
timeout /t 20 /nobreak

echo 📊 Step 5: Checking service status...
docker-compose -f docker-compose-rds-correct.yml ps

echo 📝 Step 6: Checking RAGFlow logs...
docker-compose -f docker-compose-rds-correct.yml logs ragflow --tail 10

echo.
echo ✅ If successful, RAGFlow should be at: http://localhost:9380
echo 🔍 To see live logs: docker-compose -f docker-compose-rds-correct.yml logs -f ragflow
