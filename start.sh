#!/bin/bash

echo "🚀 Starting Surgical Instrument Tracking Dashboard..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Function to start backend
start_backend() {
    echo "🐍 Starting Python Flask backend..."
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip and setuptools first
    echo "📦 Upgrading pip and setuptools..."
    pip install --upgrade pip setuptools wheel
    
    # Install requirements with --no-deps for problematic packages
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt --no-cache-dir
    
    # Start Flask server
    echo "🚀 Starting Flask server on http://localhost:5000"
    python app.py &
    BACKEND_PID=$!
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "⚛️  Starting React frontend with Vite..."
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing Node.js dependencies..."
        npm install
    fi
    
    # Start Vite development server
    echo "🚀 Starting Vite server on http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
}

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start both servers
start_backend
sleep 5  # Give backend more time to start
start_frontend

echo "✅ Both servers are starting up..."
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait 