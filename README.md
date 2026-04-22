# News Sentiment Analysis Dashboard - Azure cloud
# 🌍 Real-Time News Sentiment Intelligence Dashboard

An enterprise-grade, serverless web application that ingests live news headlines and uses Artificial Intelligence to analyze market sentiment and bias in real-time. 

Built with an event-driven architecture on **Microsoft Azure**, this application demonstrates end-to-end cloud engineering, from API data ingestion to AI processing, NoSQL storage, and dynamic frontend visualization.

---

## 🏗️ Architecture & Tech Stack

This project was intentionally designed using decoupling and cloud-native principles:

* **Frontend:** Vanilla JavaScript, HTML5, CSS3 (Tailwind CSS) - *Lightweight, dynamic DOM manipulation without framework overhead.*
* **Backend Orchestration:** Azure Functions (Python) - *Serverless, highly scalable REST API.*
* **AI Engine:** Azure AI Language Service - *Enterprise-grade NLP for sentiment analysis with confidence scoring.*
* **Database:** Azure Cosmos DB for NoSQL - *Globally distributed database for persisting search history and sentiment trends.*
* **Data Ingestion:** NewsAPI - *Live aggregation of global news publications.*

---

## ✨ Key Features

* **Real-Time AI Processing:** dynamically batches and sends news headlines to Azure Cognitive Services, receiving granular Positive, Neutral, and Negative confidence scores.
* **Algorithmic Negativity Bias:** Implements custom heuristic logic to prioritize and flag negative market sentiments, a standard requirement in financial and risk-analysis dashboards.
* **Persistent Cloud Storage:** Automatically archives every search query, associated articles, and timestamped AI results into a Cosmos DB NoSQL container for historical trend analysis.
* **Interactive UI:** Features a dynamic article-limit slider, real-time Doughnut charts (Chart.js), and individual article sentiment tagging.
* **Data Extraction:** Built-in tool to export the AI's analysis directly into a formatted CSV file for stakeholder use.

---

## ⚙️ Local Setup & Deployment

If you wish to run this architecture locally, follow these steps:

### 1. Prerequisites
* Python 3.10+
* Azure Functions Core Tools installed
* Accounts for [Azure](https://azure.microsoft.com/) and [NewsAPI](https://newsapi.org/)

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/News-Sentiment-Analysis-Dashboard.git
cd News-Sentiment-Analysis-Dashboard
python -m venv .venv
source .venv/Scripts/activate  # (or .venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
