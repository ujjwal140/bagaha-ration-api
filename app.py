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

# 2. # 2. 🆕 Naya samaan dalne ka rasta (Smart Logic Ke Sath)
@app.route('/add')
def add_item():
    key = request.args.get('api_key')
    if key != SECRET_KEY:
        return "❌ Access Denied", 403
    
    # 1. Link se naye dabbon (variables) ka data nikalna
    new_name = request.args.get('name')
    pack_type = request.args.get('packaging_type')
    
    # Text ko Number mein badalna zaroori hai math karne ke liye
    try:
        pack_count = int(request.args.get('packages_count', 0))
        weight_per_pack = float(request.args.get('weight_per_package', 0.0))
    except ValueError:
        return "⚠️ Error: Ginti aur Wazan mein sirf number aayega!", 400
    
    if not new_name or pack_count == 0:
        return "⚠️ Error: Samaan ka naam aur Packages Count likhna zaroori hai!", 400

    # 2. 🧠 TERA LOGIC YAHAN HAI (Total weight nikalna)
    total_weight = pack_count * weight_per_pack

    conn = get_db_connection()
    cur = conn.cursor()
    
    # 3. SQL Command: Tijori ke 5 naye racks mein data daalna
    cur.execute('''
        INSERT INTO ration_items 
        (name, packaging_type, packages_count, weight_per_package, total_base_weight) 
        VALUES (%s, %s, %s, %s, %s);
    ''', (new_name, pack_type, pack_count, weight_per_pack, total_weight))
    
    conn.commit() # 🔒 Samaan rakh kar save karna
    cur.close()
    conn.close()

    return f"✅ Jaadu Ho Gaya! {pack_count} {pack_type} (Total: {total_weight} kg) {new_name} Add Hua!"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
