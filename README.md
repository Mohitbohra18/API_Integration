# API Integration Project (Global Trend Internship)

**Project:** API Integration — JSONPlaceholder client  
**Author:** Candidate for Global Trend Internship  
**Language:** Python 3.8+  
**Purpose:** Demonstrates REST API integration, caching, CLI, error handling, and testability.

---

## Features

- Fetch data from JSONPlaceholder `/posts` and `/users` endpoints.
- In-memory and file-based JSON cache with TTL (default 5 minutes).
- CLI with commands:
  - `list posts [--user-id=X] [--limit=N] [--search=keyword]`
  - `get post <id>`
  - `list users [--limit=N] [--search=name]`
  - `get user <id>`
- Robust error handling (retries, timeouts, invalid JSON, file I/O errors).
- `--force` to bypass cache.
- `--verbose` to enable debug logging.
- Colored terminal output (`colorama`).
- Request/response timing and simple stats output.
- Configuration via `.env` file.
- Unit tests for API client (mocked) and data filtering.
- Clean modular code with docstrings and type hints.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git (optional)

### Installation
```bash
git clone <repo-url> api-integration-project
cd api-integration-project
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
