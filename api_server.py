#!/usr/bin/env python3
"""
MBC20 Token Analyzer API
Simple Flask API for Pro/Enterprise subscribers
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
CORS(app)

# Simple API key storage (upgrade to database in production)
API_KEYS = {
    # Pro users: 1000 req/month
    "pro_demo_key_123": {"tier": "pro", "limit": 1000, "used": 0},
    # Enterprise users: unlimited
    "ent_demo_key_456": {"tier": "enterprise", "limit": -1, "used": 0}
}

DATA_DIR = "/home/ubuntu/.openclaw/workspace"

def check_api_key(f):
    """API key authentication decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')

        if not key:
            return jsonify({"error": "Missing API key"}), 401

        if key not in API_KEYS:
            return jsonify({"error": "Invalid API key"}), 401

        # Check rate limits for Pro users
        if API_KEYS[key]["tier"] == "pro":
            # Reset monthly counter (simplified - in production use database)
            # For demo, just track usage
            API_KEYS[key]["used"] += 1
            if API_KEYS[key]["used"] > API_KEYS[key]["limit"]:
                return jsonify({"error": "Monthly API limit exceeded"}), 429

        request.user_info = API_KEYS[key]
        return f(*args, **kwargs)

    return decorated

def load_json_data(filename):
    """Load JSON data from workspace"""
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/v1/tokens/top', methods=['GET'])
@check_api_key
def get_top_tokens():
    """Get top 20 tokens by volume"""
    token_stats = load_json_data('token_stats.json')

    if not token_stats:
        return jsonify({"error": "No data available"}), 404

    # Sort by mint count
    sorted_tokens = sorted(
        token_stats.items(),
        key=lambda x: x[1]['mint_count'],
        reverse=True
    )[:20]

    result = []
    for tick, stats in sorted_tokens:
        result.append({
            "token": tick,
            "mint_count": stats['mint_count'],
            "total_amount": stats['total_amount'],
            "unique_minters": stats['unique_authors'],
            "avg_amount": stats['avg_amt'],
            "last_activity": stats['last_seen']
        })

    return jsonify({
        "data": result,
        "tier": request.user_info['tier'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/tokens/anomalies', methods=['GET'])
@check_api_key
def get_anomalies():
    """Get detected anomalies"""
    anomalies = load_json_data('anomalies.json')

    if not anomalies:
        return jsonify({"data": []})

    return jsonify({
        "data": anomalies,
        "count": len(anomalies),
        "tier": request.user_info['tier'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/tokens/<ticker>', methods=['GET'])
@check_api_key
def get_token_details(ticker):
    """Get detailed stats for a specific token"""
    token_stats = load_json_data('token_stats.json')

    if not token_stats or ticker.upper() not in token_stats:
        return jsonify({"error": "Token not found"}), 404

    stats = token_stats[ticker.upper()]

    return jsonify({
        "data": {
            "token": ticker.upper(),
            "mint_count": stats['mint_count'],
            "total_amount": stats['total_amount'],
            "unique_minters": stats['unique_authors'],
            "authors": stats['authors'][:10],  # Limit to 10
            "first_seen": stats['first_seen'],
            "last_seen": stats['last_seen'],
            "avg_amount": stats['avg_amt']
        },
        "tier": request.user_info['tier'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/alerts', methods=['GET'])
@check_api_key
def get_alerts():
    """Get recent alerts (Pro/Enterprise only)"""
    anomalies = load_json_data('anomalies.json')

    if not anomalies:
        return jsonify({"data": []})

    # Only return high-severity alerts
    high_priority = [a for a in anomalies if a['type'] in ['high_volume', 'multi_author']]

    return jsonify({
        "data": high_priority,
        "count": len(high_priority),
        "tier": request.user_info['tier'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/usage', methods=['GET'])
@check_api_key
def get_usage():
    """Get API usage statistics"""
    return jsonify({
        "tier": request.user_info['tier'],
        "limit": request.user_info['limit'],
        "used": request.user_info['used'],
        "remaining": max(0, request.user_info['limit'] - request.user_info['used']) if request.user_info['limit'] > 0 else "unlimited",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/report/latest', methods=['GET'])
def get_latest_report():
    """Get latest analysis report (public endpoint)"""
    report_path = os.path.join(DATA_DIR, 'token_analysis_report.md')

    try:
        with open(report_path, 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/markdown'}
    except FileNotFoundError:
        return jsonify({"error": "No report available"}), 404

# Run development server
if __name__ == '__main__':
    # Check dependencies
    try:
        import flask
        import flask_cors
    except ImportError:
        print("Installing dependencies...")
        os.system('pip3 install flask flask-cors')
        print("Dependencies installed. Please restart.")

    print("\n=== MBC20 Token Analyzer API ===")
    print(f"Server starting on http://0.0.0.0:5000")
    print(f"Demo API keys:")
    print(f"  Pro: pro_demo_key_123")
    print(f"  Enterprise: ent_demo_key_456")
    print(f"\nEndpoints:")
    print(f"  GET /health")
    print(f"  GET /api/v1/tokens/top")
    print(f"  GET /api/v1/tokens/anomalies")
    print(f"  GET /api/v1/tokens/<ticker>")
    print(f"  GET /api/v1/alerts")
    print(f"  GET /api/v1/usage")
    print(f"  GET /api/v1/report/latest")

    app.run(host='0.0.0.0', port=5000, debug=False)
