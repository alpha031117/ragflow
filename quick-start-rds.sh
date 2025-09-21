#!/bin/bash

# Quick start script for RAGFlow with RDS MySQL
# This script sets up the environment and starts RAGFlow

echo "🚀 Starting RAGFlow with AWS RDS MySQL"
echo "======================================"

# Copy environment file
echo "📋 Setting up environment..."
cp docker/ragflow.env docker/.env

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker/docker-compose.yml down 2>/dev/null || true

# Start with the fixed configuration
echo "🐳 Starting RAGFlow services..."
docker-compose -f docker-compose-rds-fixed.yml up -d

# Wait a moment for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check status
echo "📊 Checking service status..."
docker-compose -f docker-compose-rds-fixed.yml ps

# Show logs
echo "📝 RAGFlow logs:"
docker-compose -f docker-compose-rds-fixed.yml logs ragflow --tail=20

echo ""
echo "✅ RAGFlow should be accessible at: http://localhost:9380"
echo "🔍 To see live logs: docker-compose -f docker-compose-rds-fixed.yml logs -f ragflow"
