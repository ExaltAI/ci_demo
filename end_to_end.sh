#!/bin/bash

# End-to-end script to installs deps, lints the code, runts tests and boots up
# API server
set -e

echo "🚀 FastAPI CI/CD Demo Starting..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}📋 Step: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_error "uv is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

print_step "Installing dependencies with uv"
uv sync --dev
print_success "Dependencies installed"

print_step "Running code quality checks with ruff"
echo "Running linter..."
uv run ruff check .
print_success "Linting passed"

echo "Running formatter check..."
uv run ruff format --check .
print_success "Format check passed"

print_step "Running tests with pytest"
uv run pytest tests/ -v
print_success "All tests passed"

print_step "Starting FastAPI application"
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "Available endpoints:"
echo "  GET    /              - Health check"
echo "  POST   /messages      - Create message"
echo "  GET    /messages/{id} - Get message by ID"
echo "  DELETE /messages/{id} - Delete message by ID"
echo "  GET    /messages      - List all messages"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""

# Start the server
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000
