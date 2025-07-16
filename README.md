# Simple Message API - CI/CD Demo

A simple FastAPI application demonstrating modern CI/CD practices with Python, featuring automated testing, code quality checks, and GitHub Actions.

## Features

- **FastAPI Application**: Simple REST API with message CRUD operations
- **Modern Python Tooling**: Uses `uv` for dependency management, `ruff` for linting/formatting, `pytest` for testing
- **Comprehensive CI Pipeline**: GitHub Actions workflow with code quality, testing, security scanning, and build stages
- **API Endpoints**:
  - `GET /` - Health check
  - `POST /messages` - Create a new message
  - `GET /messages/{id}` - Get message by ID
  - `DELETE /messages/{id}` - Delete message by ID
  - `GET /messages` - List all messages

## 📋 Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Local Development

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd ci_cd
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

3. **Run the application**:
   ```bash
   uv run uvicorn app:app --reload
   ```

4. **Access the API**:
   - Application: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - OpenAPI spec: http://localhost:8000/openapi.json

### Development Commands

```bash
# Install dependencies
uv sync --dev

# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .

# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=app --cov-report=term-missing

# Start development server
uv run uvicorn app:app --reload
```

## 🧪 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/

# Create a message
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!"}'

# Get a message
curl http://localhost:8000/messages/1

# List all messages
curl http://localhost:8000/messages

# Delete a message
curl -X DELETE http://localhost:8000/messages/1
```

### Using Python requests

```python
import requests

# Create a message
response = requests.post(
    "http://localhost:8000/messages",
    json={"message": "Hello from Python!"}
)
message_id = response.json()["id"]

# Get the message
response = requests.get(f"http://localhost:8000/messages/{message_id}")
print(response.json())

# Delete the message
requests.delete(f"http://localhost:8000/messages/{message_id}")
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) includes:

### 1. Code Quality
- **Ruff linting**: Checks code style and potential issues
- **Ruff formatting**: Ensures consistent code formatting

### 2. Testing
- **Multi-version testing**: Tests on Python 3.12 and 3.13
- **Comprehensive test suite**: Unit tests for all endpoints
- **Coverage reporting**: Tracks test coverage with Codecov integration

### 3. Security Scanning
- **Safety check**: Scans for known security vulnerabilities in dependencies
- **Bandit**: Static security analysis for Python code

### 4. Build
- **Package building**: Creates distributable Python package
- **Application validation**: Ensures the app can be imported and started


For full details/explanation of the pipeline config see the 
[docs/CI_PIPELINE_EXPLAINED.md](docs/CI_PIPELINE_EXPLAINED.md) file.
## Run Script

Run the complete app with linting and tests with:

```bash
./end_to_end.sh
```

This script will:
1. Install dependencies
2. Run code quality checks
3. Execute tests
4. Start the FastAPI server

## 📁 Project Structure

```
ci_cd/
├── app.py                 # FastAPI application
├── pyproject.toml         # Project configuration and dependencies
├── requirements.txt       # Alternative dependency file
├── demo.sh               # Demo script
├── README.md             # This file
├── tests/
│   ├── __init__.py
│   └── test_app.py       # Test suite
└── .github/
    └── workflows/
        └── ci.yml        # GitHub Actions CI pipeline
```

## 🔧 Configuration

### pyproject.toml
- Project metadata and dependencies
- Ruff configuration for linting and formatting
- Pytest configuration

### GitHub Actions
- Triggers on push to `main`/`develop` and pull requests
- Runs on Ubuntu latest
- Uses matrix strategy for multi-version testing

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📝 License

This repository is for educational purposes only. Commercial use is prohibited.

See [LICENSE](LICENSE) file for details.