import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
# 🔐 Master Key
SECRET_KEY = "BAGAHA_SETH_100"

def get_db_connection():
    # Mumbai Pooler Path (Port 6543)
    return psycopg2.connect(
        host="aws-1-ap-south-1.pooler.supabase.com",
        database="postgres",
        user="postgres.ayopsyzeudpawcppwsgg",
        password="BagahaRation@2026!",
        port=6543
    )

@app.route('/')
def home():
    return "🔥 Bagaha API is Live! Use /items?api_key=BAGAHA_SETH_100"

@app.route('/items')
def get_items():
    # Browser se chabi uthayega
    key = request.args.get('api_key')
    if key != SECRET_KEY:
        return "❌ Access Denied: Galat Chabi!", 403
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ration_items;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
