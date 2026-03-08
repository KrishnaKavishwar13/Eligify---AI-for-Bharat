#!/bin/bash

# Eligify Backend - Quick Start Script
# This script helps you get the backend running locally

echo "🚀 Eligify Backend - Quick Start"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "   ✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate
echo "   ✓ Virtual environment activated"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "   ✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   ✓ .env file created"
    echo "   ⚠️  Please edit .env file with your configuration"
fi

# Start server
echo ""
echo "🎉 Starting FastAPI server..."
echo "================================"
echo ""
echo "📍 Server will be available at:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo "   - Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
