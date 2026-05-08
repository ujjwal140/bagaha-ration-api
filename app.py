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
            <title>Bagaha Seth Mobile ERP</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { box-sizing: border-box; }
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eceff1; padding: 10px; margin: 0; }
                .container { max-width: 600px; margin: auto; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
                
                h2 { color: #2c3e50; text-align: center; font-size: 1.5rem; margin-bottom: 20px; }
                
                /* --- Form Styling --- */
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
                input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; } /* 16px prevents auto-zoom on iPhone */
                .add-btn { background: #27ae60; color: white; border: none; padding: 15px; width: 100%; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
                
                /* --- Table Styling (Mobile Friendly) --- */
                .table-wrapper { overflow-x: auto; margin-top: 25px; border-radius: 8px; border: 1px solid #eee; }
                table { width: 100%; border-collapse: collapse; min-width: 450px; }
                th, td { padding: 12px 10px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
                th { background-color: #f8f9fa; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; }
                .total-col { color: #27ae60; font-weight: bold; }

                /* Mobile specific tweaks */
                @media (max-width: 480px) {
                    body { padding: 5px; }
                    .container { padding: 12px; border-radius: 0; }
                    h2 { font-size: 1.2rem; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>👑 Bagaha Seth ERP</h2>
                
                <div style="background: #fdfdfd; padding: 15px; border-radius: 10px; border: 1px dashed #ccc;">
                    <div class="form-group">
                        <label>Samaan ka Naam</label>
                        <input type="text" id="name" placeholder="Jaise: Chini">
                    </div>
                    <div class="form-group" style="display: flex; gap: 10px;">
                        <div style="flex: 1;">
                            <label>Packing</label>
                            <select id="p_type">
                                <option value="Bori">Bori</option>
                                <option value="Packet">Packet</option>
                                <option value="Box">Box</option>
                                <option value="Kg">Khulla (Kg)</option>
                            </select>
                        </div>
                        <div style="flex: 1;">
                            <label>Count</label>
                            <input type="number" id="p_count" placeholder="2">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Wazan/Pack (kg)</label>
                        <input type="number" id="p_weight" placeholder="50">
                    </div>
                    <button class="add-btn" onclick="addItem()">➕ Maal Tijori Mein Daalo</button>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Pack</th>
                                <th>Qty</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody id="inventory-body"></tbody>
                    </table>
                </div>
            </div>

            <script>
                const API_KEY = 'BAGAHA_SETH_100';

                // 1. Backend se data khinch kar dikhana
                async function loadItems() {
                    const res = await fetch(`/items?api_key=${API_KEY}`);
                    const data = await res.json();
                    let body = document.getElementById('inventory-body');
                    body.innerHTML = '';
                    data.forEach(item => {
                        body.innerHTML += `<tr>
                            <td><b>${item.name}</b></td>
                            <td>${item.packaging_type}</td>
                            <td>${item.packages_count}</td>
                            <td class="total-col">${item.total_base_weight} kg</td>
                        </tr>`;
                    });
                }

                // 2. Button dabate hi data bhejna
                async function addItem() {
                    const name = document.getElementById('name').value;
                    const type = document.getElementById('p_type').value;
                    const count = document.getElementById('p_count').value;
                    const weight = document.getElementById('p_weight').value;

                    if(!name || !count || !weight) { alert("Seth ji, sab details bharo!"); return; }

                    const res = await fetch(`/add?api_key=${API_KEY}&name=${name}&packaging_type=${type}&packages_count=${count}&weight_per_package=${weight}`);
                    if(res.ok) {
                        alert("✅ Maal add ho gaya!");
                        location.reload(); // Page refresh karke naya data dikhao
                    } else {
                        alert("❌ Kuch gadbad hui!");
                    }
                }

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
    
