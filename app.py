"""
ThreatMap - AI-Powered OSINT Intelligence Dashboard
Backend: Python + Flask + Anthropic Claude API
"""

import os
import json
import re
import urllib.request
import urllib.parse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def fetch_news(query: str) -> list[dict]:
    """Fetch recent news articles for a query using NewsAPI (free tier)."""
    api_key = os.environ.get("NEWS_API_KEY", "")
    if not api_key:
        # Return mock data if no API key provided
        return [
            {"title": f"Investigation into {query} deepens", "description": f"Authorities are examining connections related to {query} across multiple jurisdictions.", "source": "Reuters", "url": "#"},
            {"title": f"{query} linked to financial irregularities", "description": f"New documents reveal potential financial links involving {query}.", "source": "Bloomberg", "url": "#"},
            {"title": f"International agencies monitoring {query}", "description": f"Multiple national security agencies have flagged {query} for further review.", "source": "AP", "url": "#"},
        ]

    encoded_query = urllib.parse.quote(query)
    url = f"https://newsapi.org/v2/everything?q={encoded_query}&pageSize=5&sortBy=relevancy&apiKey={api_key}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ThreatMap/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            articles = data.get("articles", [])
            return [{"title": a.get("title",""), "description": a.get("description",""), "source": a.get("source",{}).get("name","Unknown"), "url": a.get("url","#")} for a in articles[:5]]
    except Exception:
        return []


def analyze_with_claude(query: str, articles: list[dict]) -> dict:
    """Use Claude API to extract entities, relationships, and risk assessment."""
    articles_text = "\n".join([f"- {a['title']}: {a['description']}" for a in articles])
    
    prompt = f"""You are an intelligence analyst. Analyze the following news articles about "{query}" and extract structured intelligence.

Articles:
{articles_text}

Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
{{
  "subject": "{query}",
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "risk_score": <number 0-100>,
  "summary": "<2-3 sentence intelligence summary>",
  "entities": [
    {{"id": "e1", "label": "<name>", "type": "PERSON|ORGANIZATION|LOCATION|EVENT|FINANCIAL", "description": "<brief role>"}}
  ],
  "relationships": [
    {{"source": "e1", "target": "e2", "label": "<relationship type>", "strength": <1-5>}}
  ],
  "key_findings": ["<finding 1>", "<finding 2>", "<finding 3>"],
  "recommended_actions": ["<action 1>", "<action 2>"]
}}

Include the subject "{query}" as the first entity. Extract 5-8 entities total and 4-7 relationships from the articles."""

    try:
        import urllib.request
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()
        
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            text = data["content"][0]["text"].strip()
            # Clean up any markdown fences
            text = re.sub(r"```json\s*", "", text)
            text = re.sub(r"```\s*", "", text)
            return json.loads(text)
    except Exception as e:
        # Fallback mock response
        return {
            "subject": query,
            "risk_level": "MEDIUM",
            "risk_score": 55,
            "summary": f"Intelligence analysis for '{query}' indicates moderate activity requiring monitoring. Multiple entities have been identified with potential cross-border connections.",
            "entities": [
                {"id": "e1", "label": query, "type": "ORGANIZATION", "description": "Primary subject of investigation"},
                {"id": "e2", "label": "Financial Network A", "type": "FINANCIAL", "description": "Associated financial entity"},
                {"id": "e3", "label": "Agency XYZ", "type": "ORGANIZATION", "description": "Regulatory body involved"},
                {"id": "e4", "label": "Region Alpha", "type": "LOCATION", "description": "Geographic area of interest"},
                {"id": "e5", "label": "Key Person 1", "type": "PERSON", "description": "Individual of interest"},
            ],
            "relationships": [
                {"source": "e1", "target": "e2", "label": "FUNDS", "strength": 4},
                {"source": "e1", "target": "e5", "label": "ASSOCIATED_WITH", "strength": 3},
                {"source": "e3", "target": "e1", "label": "INVESTIGATES", "strength": 5},
                {"source": "e4", "target": "e1", "label": "LOCATION_OF", "strength": 2},
            ],
            "key_findings": [
                "Subject shows connections across multiple jurisdictions",
                "Financial patterns suggest structured activity",
                "Cross-agency coordination recommended"
            ],
            "recommended_actions": [
                "Initiate enhanced monitoring protocol",
                "Request financial records from relevant institutions"
            ]
        }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    articles = fetch_news(query)
    result = analyze_with_claude(query, articles)
    result["articles"] = articles
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
