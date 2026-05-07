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
    # Ye HTML tera asli "App" ka chehra hai
    return """
    <html>
        <body style="font-family: Arial; text-align: center; background-color: #f4f4f9; padding: 50px;">
            <h1 style="color: #333;">👑 Bagaha Seth Inventory</h1>
            <p>Apni tijori ka saaman yahan dekhein:</p>
            
            <button onclick="loadData()" style="padding: 15px 30px; font-size: 18px; background-color: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                📦 Tijori Kholo
            </button>
            
            <ul id="itemList" style="list-style: none; padding: 0; margin-top: 30px; font-size: 22px; color: #555;"></ul>
            
            <script>
                // Ye script tere backend se data mangti hai aur screen par sajati hai
                function loadData() {
                    document.getElementById('itemList').innerHTML = "⏳ Engine saaman nikal raha hai...";
                    
                    fetch('/items?api_key=BAGAHA_SETH_100')
                    .then(response => response.json())
                    .then(data => {
                        let listHtml = "";
                        data.forEach(item => {
                            listHtml += `<li style="background: white; margin: 10px auto; padding: 15px; width: 80%; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><b>${item.name}</b> : ${item.quantity} kg</li>`;
                        });
                        document.getElementById('itemList').innerHTML = listHtml;
                    })
                    .catch(error => {
                        document.getElementById('itemList').innerHTML = "❌ Error aagaya seth!";
                    });
                }
            </script>
        </body>
    </html>
    """
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
    
