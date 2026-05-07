import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)
# 🔐 Master Key
SECRET_KEY = "BAGAHA_SETH_100"

def get_db_connection():
    return psycopg2.connect(
        host="aws-1-ap-south-1.pooler.supabase.com",
        database="postgres",
        user="postgres.ayopsyzeudpawcppwsgg",
        password="BagahaRation@2026!",
        port=6543
    )

@app.route('/')
def home():
    return "🔥 Bagaha API is Live!"

# 1. Samaan dekhne ka rasta
@app.route('/items')
def get_items():
    key = request.args.get('api_key')
    if key != SECRET_KEY:
        return "❌ Access Denied", 403
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM ration_items;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# 2. 🆕 Naya samaan dalne ka rasta
@app.route('/add')
def add_item():
    key = request.args.get('api_key')
    if key != SECRET_KEY:
        return "❌ Access Denied", 403
        
    # Link se naam aur quantity nikalna
    new_name = request.args.get('name')
    new_qty = request.args.get('quantity')
    
    if not new_name or not new_qty:
        return "⚠️ Error: Samaan ka naam (?name=...) aur quantity (&quantity=...) dono dena zaroori hai!", 400

    conn = get_db_connection()
    cur = conn.cursor()
    # SQL Command: Tijori mein naya saaman daalo
    cur.execute('INSERT INTO ration_items (name, quantity) VALUES (%s, %s);', (new_name, new_qty))
    conn.commit() # 🔒 Samaan rakh kar save karna!
    cur.close()
    conn.close()
    
    return f"✅ Jaadu Ho Gaya! Naya Samaan Add Hua: {new_name} (Quantity: {new_qty})"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
