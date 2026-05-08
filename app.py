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
def home():
    return "🔥 Bagaha API is Live!"
@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Bagaha Seth Inventory</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
                .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                h2 { color: #333; text-align: center; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #2ecc71; color: white; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .refresh-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📦 Bagaha Seth Inventory</h2>
                <button class="refresh-btn" onclick="loadItems()">🔄 Hisaab Refresh Karo</button>
                <table>
                    <thead>
                        <tr>
                            <th>Samaan</th>
                            <th>Packing</th>
                            <th>Count</th>
                            <th>Wazan/Pack</th>
                            <th>Total Weight</th>
                        </tr>
                    </thead>
                    <tbody id="inventory-body">
                        </tbody>
                </table>
            </div>

            <script>
                async function loadItems() {
                    const response = await fetch('/items?api_key=BAGAHA_SETH_100');
                    const data = await response.json();
                    let tableBody = document.getElementById('inventory-body');
                    tableBody.innerHTML = '';

                    data.forEach(item => {
                        let row = `<tr>
                            <td><b>${item.name}</b></td>
                            <td>${item.packaging_type || '-'}</td>
                            <td>${item.packages_count || 0}</td>
                            <td>${item.weight_per_package || 0} kg</td>
                            <td><span style="color:green; font-weight:bold;">${item.total_base_weight || 0} kg</span></td>
                        </tr>`;
                        tableBody.innerHTML += row;
                    });
                }
                // Page khulte hi data load ho jaye
                loadItems();
            </script>
        </body>
    </html>
    """
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
    
