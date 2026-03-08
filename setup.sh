#!/bin/bash

echo "========================================"
echo "Eligify Project Setup (Linux/Mac)"
echo "========================================"
echo ""

# Check Python
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.10+"
    exit 1
fi
echo "Python found: $(python3 --version)"
echo ""

# Check Node.js
echo "[2/6] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "Node.js found: $(node --version)"
echo ""

# Backend Setup
echo "[3/6] Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi
echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "IMPORTANT: Please edit backend/.env with your configuration!"
fi
cd ..
echo "Backend setup complete!"
echo ""

# Frontend Setup
echo "[4/6] Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed, skipping..."
fi
cd ..
echo "Frontend setup complete!"
echo ""

# Data directories
echo "[5/6] Checking data directories..."
mkdir -p backend/data/persistence
echo "Data directories ready"
echo ""

echo "[6/6] Setup Summary"
echo "========================================"
echo "Backend: eligify-ai-for-bharat/backend"
echo "Frontend: eligify-ai-for-bharat/frontend"
echo ""
echo "NEXT STEPS:"
echo "1. Edit backend/.env with your configuration"
echo "2. Optional: Install Ollama for AI features"
echo "   - Run: curl -fsSL https://ollama.com/install.sh | sh"
echo "   - Run: ollama pull llama3.1:8b"
echo ""
echo "TO START THE PROJECT:"
echo "Backend:  cd backend && source venv/bin/activate && python quick_start.py"
echo "Frontend: cd frontend && npm run dev"
echo ""
echo "========================================"
echo "Setup complete! Happy coding!"
echo "========================================"
