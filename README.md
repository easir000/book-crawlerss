
# 📘 Book Crawler Project

A production-grade system to crawl, monitor, and serve data from [https://books.toscrape.com](https://books.toscrape.com).

- ✅ Part 1: Async web crawler with MongoDB  
- ✅ Part 2: Daily scheduler with change detection & reporting  
- ✅ Part 3: Secure RESTful API with auth, filtering, and pagination  

---

## 🛠️ Requirements

- Python: `>=3.10`
- Docker: For MongoDB (recommended)
- OS: Windows, macOS, or Linux

---

## 📦 Installation

### 1. Clone the Repository

git clone https://github.com/easir000/book-crawlerss.git
cd book-crawler


### 2. Create & Activate Virtual Environment

python -m venv myenv


#### Windows ():

myenv\Scripts\Activate.ps1


#### macOS/Linux:

source myenv/bin/activate


### 3. Install Dependencies

pip install -r requirements.txt


> 💡 Optional: `pip install -e .` if you use `pyproject.toml`.

---

## ⚙️ Configuration

### 1. Create `.env`

cp .env.example .env


#### Edit `.env`:
env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=books_db

# Crawler
CRAWL_CONCURRENCY=10

# API
API_KEY=xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0;


> 🔐 Never commit `.env` to Git!

---

Below is the complete MongoDB schema design for your Book Crawler project, including both collections: `books` and `change_log`.

---

### 🗃️ Collection 1: `books`

Stores the full, structured, and raw representation of each book.

```json
{
  "_id": ObjectId("665d1a2b3c4d5e6f7a8b9c0d"),
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "title": "A Light in the Attic",
  "description": "Some poetic description...",
  "category": "Poetry",
  "price_excl_tax": 39.99,
  "price_incl_tax": 39.99,
  "availability_raw": "In stock (22 available)",
  "availability_count": 22,
  "num_reviews": 0,
  "image_url": "https://books.toscrape.com/media/cache/.../image.jpg",
  "rating": 3,
  "raw_html": "<!DOCTYPE html>...",
  "crawled_at": ISODate("2024-06-01T10:00:00Z"),
  "status": "success",
  "fingerprint": "a1b2c3d4e5f67890..."  // SHA-256 hash of key fields
}
```

#### 🔑 Indexes
- Unique Index: `{"url": 1}` → ensures no duplicates
- Compound Index: `{"category": 1, "price_incl_tax": 1, "rating": 1}` → accelerates API queries

---

### 📝 Collection 2: `change_log`

Tracks all detected changes (new books or field updates) with audit details.

```json
{
  "_id": ObjectId("665d1b3c4d5e6f7a8b9c0e1f"),
  "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "change_type": "updated",  // or "new"
  "detected_at": ISODate("2024-06-02T02:15:00Z"),
  "changes": {
    "price_incl_tax": {
      "old": 39.99,
      "new": 22.65
    },
    "availability_count": {
      "old": 22,
      "new": 15
    }
  },
  "details": {
    "title": "A Light in the Attic",
    "category": "Poetry"
  }
}
```

> 💡 For `"change_type": "new"`, the `changes` field may be omitted or empty, and `details` contains initial book metadata.

#### 🔑 Indexes
- TTL Index (Optional): `{"detected_at": 1}` with expireAfterSeconds (e.g., 2592000 for 30 days)
- Standard Index: `{"detected_at": -1}` → for efficient querying of recent changes

---

### ✅ Summary of Collections

| Collection | Purpose | Key Fields |
|----------|--------|-----------|
| `books` | Primary storage of book data | `url`, `title`, `price_incl_tax`, `rating`, `raw_html`, `fingerprint` |
| `change_log` | Audit trail of changes | `book_url`, `change_type`, `changes`, `detected_at` |

This schema supports:
- Deduplication (via `url` uniqueness)
- Efficient querying (via compound indexes)
- Change detection (via `fingerprint`)
- Auditability (via `change_log`)
- Fallback parsing (via `raw_html`)

All requirements for Part 1 (Crawler) and Part 2 (Change Detection) are fully satisfied.

## 🗄️ MongoDB Setup (via Docker)

> ✅ No auth needed for local development.
**
ensure that this line is commented from .env file when running docker 
MONGODB_URL=mongodb://localhost:27017
**

### Option A: Use `docker-compose.yml` (Please use it)
Create `docker-compose.yml` in your project root:
yaml
# docker-compose.yml
version: '3.8'
services:
  mongodb:
    image: mongo:6.0
    container_name: mongo-book
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongo-book-data:/data/db
    networks:
      - book-crawler-net

volumes:
  mongo-book-

networks:
  book-crawler-net:
    driver: bridge


Then run:

docker-compose up -d


> 📌 Data persists in Docker volume `mongo-book-data`.

---

## ▶️ Running the Project

### ✅ Part 1: Run the Crawler (One-Time)

python -m crawler.main

> ⏱️ First run: 5–10 minutes (1,000 books).  
> 🔁 Resumes from last category on failure.

---

### 🕒 Part 2: Scheduler & Change Detection

#### A. One-Time Job (Testing)

python -m scheduler.tasks

- Detects new/updated books
- Generates `reports/change_report_YYYY-MM-DD.json`
- Logs alerts to `alerts.log`

#### B. Daily Scheduler (Production)
Runs every day at 2:00 AM :

python -m scheduler.main


---

### 🌐 Part 3: Start the API Server

uvicorn app.api.main:app --reload --port 8000


#### Endpoints:
| Endpoint | Description |
|--------|------------|
| `GET /books` | Filter, sort, paginate |
| `GET /books/{id}` | Get book by ID |
| `GET /changes` | Changes in last 24h |
| `GET /health` | Health check |

#### Authentication:

curl -H "X-API-Key: xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0l" http://localhost:8000/books

## 🧪 Testing

### Run API Tests

| `pytest tests/test_api.py -v` | `pytest tests/test_crawler.py -v` | `pytest tests/test_change_detection.py -v` | ` pytest tests/test_api.py::test_books_pagination -v ` |
| Docker Compose | `docker-compose up -d` |

✅ Expected:

test_invalid_api_key PASSED
test_books_endpoint PASSED


> 📌 Ensure MongoDB is running and `.env` is configured.

---

## 📁 Project Structure

book-crawler/
├── .env.example
├── requirements.txt
├── docker-compose.yml        # ← Docker setup
├── README.md
├── app/
│   ├── models/               # Pydantic models
│   └── api/                  # FastAPI
├── crawler/                  # Async crawler
├── scheduler/                # Daily tasks
├── reports/                  # JSON change reports
├── alerts.log                # Price drop alerts
└── tests/                    # API tests


---

## 📎 Deliverables

- ✅ Postman Collection: `book-crawler-api.postman_collection.json`
- ✅ Sample MongoDB Document:
  json
  {
    "url": "https://books.toscrape.com/.../index.html",
    "title": "A Light in the Attic",
    "category": "Poetry",
    "price_incl_tax": 51.77,
    "rating": 3,
    "raw_html": "<!DOCTYPE html>...",
    "crawled_at": "2024-06-05T12:00:00Z",
    "fingerprint": "a1b2c3d4..."
  }
  
- ✅ Logs: Generated by running any command

---

## 🐳 Docker-Only Deployment (Optional)

To run everything in Docker (crawler, scheduler, API, MongoDB):

1. Ensure you have `Dockerfile` and `docker-compose.yml` (see full setup in project docs)
2. Build and start:
   
   docker-compose build
   docker-compose up -d
   
3. Access API at `http://localhost:8000`

---

## 🚀 Summary of All Commands

| Task | Command |
|-----|--------|
| Setup | `python -m venv myenv` → `pip install -r requirements.txt` |
| MongoDB | `docker run -d --name mongo-book -p 27017:27017 -v mongo-book-data:/data/db mongo:6.0` |
| Crawler | `python -m crawler.main` |
| One-Time Scheduler | `python -m scheduler.tasks` |
| Daily Scheduler | `python -m scheduler.main` |
| API Server | `uvicorn app.api.main:app --reload --port 8000` |
| API Tests | `pytest tests/test_api.py -v` | `pytest tests/test_crawler.py -v` | `pytest tests/test_change_detection.py -v` | ` pytest tests/test_api.py::test_books_pagination -v ` |
| Docker Compose | `docker-compose up -d` |

---

> ✨ You’re ready to crawl, monitor, and serve!  
> This project meets all requirements for a scalable, fault-tolerant, and production-ready web crawling system.

Here is a complete, valid Postman Collection  for your Book Crawler API, ready to import into Postman for testing all endpoints with authentication, filtering, pagination, and error cases.

---

###  `book-crawler-api.postman_collection.`

 "info": {
    "name": "Book Crawler API",
    "_postman_id": "book-crawler-api",
    "description": "RESTful API for books.toscrape.com data with authentication and change tracking.",
    "schema": "https://schema.getpostman.com//collection/v2.1.0/collection."
  },
  "item": [
    {
      "name": "GET /books (All Books)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "{{api_key}}" }
        ],
        "url": {
          "raw": "{{base_url}}/books",
          "host": ["{{base_url}}"],
          "path": ["books"]
        }
      }
    },
    {
      "name": "GET /books (Filtered by Category)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "{{api_key}}" }
        ],
        "url": {
          "raw": "{{base_url}}/books?category=Travel",
          "host": ["{{base_url}}"],
          "path": ["books"],
          "query": [{ "key": "category", "value": "Travel" }]
        }
      }
    },
    {
      "name": "GET /books (Price Range + Sort)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "{{api_key}}" }
        ],
        "url": {
          "raw": "{{base_url}}/books?min_price=20&max_price=50&sort_by=price",
          "host": ["{{base_url}}"],
          "path": ["books"],
          "query": [
            { "key": "min_price", "value": "20" },
            { "key": "max_price", "value": "50" },
            { "key": "sort_by", "value": "price" }
          ]
        }
      }
    },
    {
      "name": "GET /books (Pagination)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "{{api_key}}" }
        ],
        "url": {
          "raw": "{{base_url}}/books?page=2&size=10",
          "host": ["{{base_url}}"],
          "path": ["books"],
          "query": [
            { "key": "page", "value": "2" },
            { "key": "size", "value": "10" }
          ]
        }
      }
    },
    {
      "name": "GET /books/{id}",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "{{api_key}}" }
        ],
        "url": {
          "raw": "{{base_url}}/books/665d1a2b3c4d5e6f7a8b9c0d",
          "host": ["{{base_url}}"],
          "path": ["books", "665d1a2b3c4d5e6f7a8b9c0d"]
        }
      }
    },
    {
      "name": "GET /changes",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "{{api_key}}" }
        ],
        "url": {
          "raw": "{{base_url}}/changes",
          "host": ["{{base_url}}"],
          "path": ["changes"]
        }
      }
    },
    {
      "name": "GET /books (Invalid API Key)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "X-API-Key", "value": "invalid-key" }
        ],
        "url": {
          "raw": "{{base_url}}/books",
          "host": ["{{base_url}}"],
          "path": ["books"]
        }
      }
    }
  ],
  "variable": [
    { "key": "base_url", "value": "http://localhost:8000" },
    { "key": "api_key", "value": "xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0l" }
  ]
}

---

###  How to Use
1. Save the above as `book-crawler-api.postman_collection.`.
2. In Postman:
   - Click Import → Upload Files → Select the  file.
3. The collection will appear with:
   - All endpoints pre-configured
   - Environment variables (`base_url`, `api_key`) editable in the collection settings
4. Update `api_key` if yours differs (matches your `.env`).

---

### ✅ Test Coverage
| Test Case | Purpose |
|---------|--------|
| All Books | Basic list retrieval |
| Category Filter | Validate filtering |
| Price + Sort | Test query params & sorting |
| Pagination | Verify `page`/`size` |
| Get by ID | Single book detail |
| Changes | Recent updates |
| Invalid Key | 403 error handling |
