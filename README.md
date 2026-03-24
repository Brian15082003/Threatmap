# ThreatMap — AI-Powered OSINT Intelligence Dashboard

A real-time intelligence platform that uses AI to analyze public data, extract entities and relationships, and visualize them as an interactive graph network.

Built as a demonstration of AI-native tooling for intelligence analysis — combining web scraping, LLM-powered entity extraction, and graph visualization.

---

## What It Does

1. User enters a target query (person, organization, keyword)
2. App fetches relevant news articles from public sources
3. Claude AI extracts entities, relationships, and risk signals
4. Results are visualized as an interactive knowledge graph
5. Side panel shows risk score, key findings, and recommended actions

---

## Tech Stack

- **Backend**: Python, Flask
- **AI**: Anthropic Claude API (claude-sonnet-4)
- **News Data**: NewsAPI (free tier)
- **Graph Visualization**: D3.js force-directed graph
- **Frontend**: Vanilla JS + CSS (no framework needed)

---

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/threatmap.git
cd threatmap
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
```bash
export ANTHROPIC_API_KEY=your_key_here
export NEWS_API_KEY=your_key_here   # optional — works without it using mock data
```

Get a free Anthropic API key at: https://console.anthropic.com
Get a free NewsAPI key at: https://newsapi.org

### 4. Run the app
```bash
python app.py
```

Open http://localhost:5000 in your browser.

---

## Usage

- Type any name, organization, or topic in the search bar
- Press Enter or click ANALYZE
- The AI extracts entities and relationships from recent news
- Drag nodes around the graph to explore connections
- Hover over nodes to see details

---

## Architecture

```
User Query
    ↓
NewsAPI (fetch relevant articles)
    ↓
Claude AI (extract entities, relationships, risk)
    ↓
Flask API (/analyze endpoint)
    ↓
D3.js Force Graph (visualize knowledge network)
```

---

## Project Structure

```
threatmap/
├── app.py              # Flask backend + Claude API integration
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend (D3.js graph + UI)
└── README.md
```

---

## Why This Project

This was built to demonstrate AI-native thinking for intelligence use cases — specifically the pattern of: **ingest unstructured data → AI extraction → structured graph output → actionable insights**. 

The same pattern applies to real OSINT platforms, financial fraud detection, and national security monitoring systems.

---

## Author

Brian Dias  
briandias177@gmail.com
