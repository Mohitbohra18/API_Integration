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
git clone <"https://github.com/Mohitbohra18/API_Integration.gitl"> api-integration-project
cd api-integration-project
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


# 🛰️ API Integration Project — Global Trend Internship Submission

A professional Python-based **API Integration Project** built as part of the **Global Trend Internship Application**.  
This application demonstrates REST API integration, caching, error handling, CLI tooling, testing, and clean software engineering practices.

---

## 📌 Project Overview

This application integrates with the **JSONPlaceholder API** to fetch:

- `/posts` — Blog posts  
- `/users` — User information  

It supports powerful filtering, caching, and robust error handling through a well-structured CLI.

---

## 🚀 Features

### ✔ API Integration
- Fetch posts and users using the `requests` library  
- Retry logic with exponential backoff  
- Timeout handling (10 seconds)  
- JSON validation  
- Logging for debugging  

### ✔ Caching System
- File-based cache (`cache/`)  
- In-memory cache layer  
- Automatic TTL expiration (5 minutes)  
- Force-refresh option (`--force`)  

### ✔ Command Line Interface (CLI)
- `list posts` with filters:  
  - `--user-id=`  
  - `--limit=`  
  - `--search=`  
- `get post <id>` → Includes detailed author info  
- `list users` with `--limit` & `--search`  
- `get user <id>` → Includes post count  
- `--verbose` for debug-level logs  
- Auto-generated `--help`  

### ✔ Error Handling
Handles:  
- Network failures  
- API timeouts  
- 4xx / 5xx HTTP errors  
- Invalid JSON  
- Malformed API data  
- Corrupted cache files  
- Invalid CLI arguments  

### ✔ Developer Experience
- Fully modular architecture  
- PEP8 compliance + type hints  
- Colored output using `colorama`  
- `.env` config support  
- Complete test suite (`pytest`)  

---

## 🗂️ Project Structure

```bash
api-integration-project/
│
├── src/
│ ├── api_client.py
│ ├── cache_manager.py
│ ├── data_filter.py
│ ├── cli.py
│ ├── utils.py
│ └── init.py
│
├── tests/
│ ├── test_api_client.py
│ └── test_data_filter.py
│
├── cache/
├── screenshots/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 📸 Sample Output Screenshots

### 1. Listing Posts
![Listing Posts](screenshots\image-5.png)

### 2. View Post Details
![Post Details](screenshots\image-1.png)

### 3. Error Handling Example
![Error Handling](screenshots\image-3.png)

### 4. Filtering Posts
![Filtering](screenshots\image-2.png)



