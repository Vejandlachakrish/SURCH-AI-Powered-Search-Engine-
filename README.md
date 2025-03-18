# SURCH - AI-Powered Search Engine

## Overview

SURCH is an **AI-driven search engine** that mimics Google-like functionality, utilizing **Flask (Python), Elasticsearch, FAISS (Vector Search), and React.js** to provide intelligent, real-time search results.

## Features

✅ **Web Crawling & Indexing** - Uses Scrapy & BeautifulSoup to extract and store data.  
✅ **AI-Powered Query Processing** - Implements BERT, BM25, and spell correction for accurate results.  
✅ **Personalized Search Experience** - Reinforcement learning for user-specific ranking.  
✅ **Scalable & Dockerized Deployment** - Runs smoothly using Docker & Kubernetes.

## 📂 Project Structure

```bash
surch-search-engine/
│── 📂 backend/                # Flask API for search processing
│   ├── 📂 crawler/            # Web crawler (Scrapy, BeautifulSoup)
│   ├── 📂 indexer/            # Indexing service (BM25, BERT, FAISS)
│   ├── 📂 query_processor/    # Query processing (spell correction, NLP)
│   ├── 📂 ranking_engine/     # Hybrid ranking (BM25 + BERT + Learning to Rank)
│   ├── 📂 personalization/    # AI-based personalization (Reinforcement Learning)
│   ├── 📜 app.py              # Main Flask API entry point
│   ├── 📜 Dockerfile          # Docker setup for backend
│   ├── 📜 requirements.txt    # Python dependencies
│
│── 📂 frontend/               # React-based UI for search
│   ├── 📂 src/
│   ├── 📜 package.json
│   ├── 📜 Dockerfile
│
│── 📂 database/               # Elasticsearch, FAISS, Redis setup
│   ├── 📜 elasticsearch.yml   # Elasticsearch config
│   ├── 📜 Dockerfile
│
│── 📂 deployment/             # Docker and Kubernetes setup
│   ├── 📜 docker-compose.yml  # Defines all services
│   ├── 📜 k8s-deployment.yaml # Kubernetes deployment file (optional)
│
│── 📂 config/                 # Configuration files
│   ├── 📜 settings.py
│
│── 📜 README.md               # Instructions for running the project
│── 📜 .env                    # Environment variables
│── 📜 .gitignore              # Ignore unnecessary files
```

## 🛠️ Prerequisites

Before you start, ensure you have the following installed:

1️⃣ **[Docker](https://www.docker.com/products/docker-desktop/)** (for running services)  
2️⃣ **Python 3.11+** (Install from [here](https://www.python.org/downloads/))  
3️⃣ **Node.js (v20.18.0 or later)** (Install from [here](https://nodejs.org/en/download/))  
4️⃣ **Git** (for cloning the repository)

## 🚀 Installation & Running the Project

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/surch-search-engine.git
cd surch-search-engine
```

### **2️⃣ Install Dependencies**

#### **🔹 Backend (Flask API)**

```bash
cd backend
pip install -r requirements.txt
```

#### **🔹 Frontend (React UI)**

```bash
cd ../frontend
npm install
```

### **3️⃣ Start the Project**

#### **🔹 Start Elasticsearch & Other Services**

```bash
cd deployment
docker-compose up -d
```

#### **🔹 Start Backend**

```bash
cd ../backend
python app.py
```

#### **🔹 Start Frontend**

```bash
cd ../frontend
npm start
```

## 🛠 Troubleshooting

🔹 **If Port 3000 is Already in Use**

```bash
netstat -ano | findstr :3000  # Find process ID (PID)
taskkill /PID <PID_NUMBER> /F  # Replace <PID_NUMBER> with the actual ID
```

🔹 **Elasticsearch Issues? Check the Cluster Health:**

```bash
curl -X GET "http://localhost:9200/_cluster/health?pretty" --user elastic:changeme
```

✅ If status is 🟢 GREEN → Everything is fine!  
🟡 If status is YELLOW → Elasticsearch is running but not fully replicated.  
🔴 If status is RED → Restart Elasticsearch:

```bash
cd deployment
docker-compose up -d elasticsearch
```

## 📝 Notes

- **Ensure Elasticsearch is running before starting the backend.**
- **Scrapy will keep crawling continuously unless manually stopped.**
- **If frontend throws `Failed to fetch`, ensure backend (`app.py`) is running.**

## 🤝 Contributing

If you’d like to contribute, feel free to submit a **Pull Request**. Make sure to test your changes before submitting.

## 📜 License

MIT License © 2025 Your Name

---

🔥 **Now you are ready to run SURCH!** Happy coding! 🚀
