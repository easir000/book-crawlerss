# 📘 Book Crawler Project

A production-grade web crawling, monitoring, and API system for `https://books.toscrape.com`.

- **Part 1**: Async web crawler with MongoDB storage  
- **Part 2**: Daily scheduler with change detection & reporting  
- **Part 3**: Secure RESTful API with authentication & filtering  

---

## 🛠️ Requirements

- **Python**: `>=3.10`
- **MongoDB**: `>=5.0` (local or Docker)
- **OS**: Windows, macOS, or Linux

---

## 📦 Installation

### 1. Clone the Repository

git clone https://github.com/your-username/book-crawler.git
cd book-crawler


### 2. Create a Virtual Environment

python -m venv myenv


#### Activate it:
- **Windows ()**:
  
  myenv\Scripts\Activate.ps1
  
- **macOS/Linux**:
  
  source myenv/bin/activate
  

### 3. Install Dependencies

pip install -r requirements.txt


> **Note**: If you modified `pyproject.toml`, also run:
> 
> pip install -e .
> 

---

## ⚙️ Configuration

### 1. Create `.env` File
Copy the example and fill in your values:

cp .env.example .env


#### Example `.env`:
env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=books_db

# Crawler
CRAWL_CONCURRENCY=10

# API
API_KEY=xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0u


> 🔐 **Keep `API_KEY` secret** — never commit it to Git.

---

## 🗄️ MongoDB Setup

### Option A: Run MongoDB via Docker (Recommended)

docker run -d -p 27017:27017 --name mongo-book mongo


### Option B: Install Locally
Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community)

---

## ▶️ Running the Project

### ✅ Part 1: Run the Crawler (One-Time)
Crawls all books and stores them in MongoDB.


python -m crawler.main


> 💡 On first run, this takes **5–10 minutes** (1,000 books, 50 categories).  
> Subsequent runs skip already-crawled categories (resumable).

---

### 🕒 Part 2: Run the Scheduler

#### A. One-Time Change Detection (Recommended for testing)

python -m scheduler.tasks

- Crawls all books
- Detects new/updated records
- Generates `reports/change_report_YYYY-MM-DD.json`
- Logs alerts to `alerts.log`

#### B. Start Daily Scheduler (Production)
Runs automatically every day at **2:00 AM Bangladesh Time (BDT)**.


python -m scheduler.main


> 🌍 Timezone: `Asia/Dhaka` (UTC+6). Adjust in `scheduler/main.py` if needed.

---

### 🌐 Part 3: Start the API Server


uvicorn app.api.main:app --reload --port 8000


#### API Endpoints:
| Endpoint | Description |
|--------|------------|
| `GET /books` | List books (filter, sort, paginate) |
| `GET /books/{id}` | Get book by ID |
| `GET /changes` | View recent changes (last 24h) |
| `GET /health` | Health check |

#### Authentication:
- Include header: `X-API-Key: <your-api-key>`
- Example with `curl`:
  
  curl -H "X-API-Key: xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0u" http://localhost:8000/books
  

#### Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testing

### Run API Tests

pytest tests/test_api.py -v


### Expected Output:

test_invalid_api_key PASSED
test_books_endpoint PASSED


> ✅ Ensure MongoDB is running and `.env` is configured before testing.

---

## 📁 Project Structure

book-crawler/
├── .env.example
├── requirements.txt
├── README.md
├── app/
│   ├── models/          # Pydantic models (Book, BookResponse)
│   └── api/             # FastAPI app & routes
├── crawler/             # Async web crawler
├── scheduler/           # Daily tasks & change detection
├── reports/             # Auto-generated change reports
├── alerts.log           # Significant change alerts
└── tests/               # API tests


---

## 📎 Deliverables Included

- ✅ **Postman Collection**: `book-crawler-api.postman_collection.json`
- ✅ **Sample MongoDB Document**:
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
  
- ✅ **Screenshots/Logs**: Run any command above to generate logs.

---

## 🚀 Next Steps

- Import the **Postman collection** to test all endpoints
- View **daily reports** in `reports/`
- Monitor **alerts** in `alerts.log`
- Deploy API with **Nginx + Gunicorn** for production

---



Certainly. Below is a **complete, production-ready Docker setup for MongoDB** tailored to your Book Crawler project.

---

### ✅ Step-by-Step: Run MongoDB via Docker

#### 1. **Install Docker**
- **Windows**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **macOS**: Install via Homebrew: `brew install --cask docker`
- **Linux**: Follow [official instructions](https://docs.docker.com/engine/install/)

Ensure Docker is running before proceeding.

---

#### 2. **Create a Dedicated Docker Network (Optional but Recommended)**
This isolates your services and enables clean networking.


docker network create book-crawler-net


---

#### 3. **Run MongoDB Container**


docker run -d \
  --name mongo-book \
  --network book-crawler-net \
  -p 27017:27017 \
  -v mongo-book-/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=securepassword123 \
  mongo:6.0


> 💡 **Explanation**:
> - `-d`: Run in detached mode (background)
> - `--name mongo-book`: Container name (used in `.env`)
> - `--network book-crawler-net`: Join custom network
> - `-p 27017:27017`: Map host port to container
> - `-v mongo-book-/data/db`: Persistent volume (data survives container restart)
> - `-e ...`: Set admin credentials (optional for local dev, but good practice)

> 🛑 **For local development only**, you can skip auth by omitting the `-e` lines.  
> But if you include them, update your `.env` accordingly (see Step 4).

---

#### 4. **Update Your `.env` File**

##### Option A: **Without Authentication** (Simplest for local dev)
env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=books_db


##### Option B: **With Authentication** (More secure)
env
MONGODB_URL=mongodb://admin:securepassword123@localhost:27017/books_db?authSource=admin
MONGODB_DB_NAME=books_db


> 🔐 If you used `-e MONGO_INITDB_ROOT_USERNAME` and `-e MONGO_INITDB_ROOT_PASSWORD`, use **Option B**.

---

#### 5. **Verify MongoDB Is Running**


# Check container status
docker ps

# Expected output:
# CONTAINER ID   IMAGE       COMMAND                  ...   STATUS       PORTS                      NAMES
# abc123         mongo:6.0   "docker-entrypoint.s…"   ...   Up 2 hours   0.0.0.0:27017->27017/tcp   mongo-book



# Test connection (requires `mongosh`)
docker exec -it mongo-book mongosh --eval "db.runCommand({ ping: 1 })"


---

#### 6. **(Optional) Use `docker-compose.yml` for Simpler Management**

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
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: securepassword123
    networks:
      - book-crawler-net

volumes:
  mongo-book-

networks:
  book-crawler-net:
    driver: bridge


Then run:

docker-compose up -d


To stop:

docker-compose down


> ✅ This is the **most maintainable approach** for local development.

---

### 🧪 Final Test
Run your crawler:

python -m crawler.main


You should see books being saved without MongoDB connection errors.

---

### 📌 Summary

| Action | Command |
|------|--------|
| Start MongoDB | `docker run ...` (or `docker-compose up -d`) |
| Stop MongoDB | `docker stop mongo-book` (or `docker-compose down`) |
| View Data | Use [MongoDB Compass](https://www.mongodb.com/products/compass) → connect to `mongodb://localhost:27017` |
