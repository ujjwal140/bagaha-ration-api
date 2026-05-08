import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# --- CONFIGURATION ---
DB_URL =  "postgresql://postgres.ayopsyzeudpawcppwsgg:BagahaRation%402026!@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
SECRET_KEY = "BAGAHA_SETH_100"

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Bagaha Seth ERP Pro</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { box-sizing: border-box; }
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 10px; margin: 0; }
                .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
                h2 { color: #1a237e; text-align: center; margin-bottom: 20px; font-size: 24px; }
                .form-section { background: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
                label { display: block; margin-bottom: 5px; font-weight: 600; font-size: 13px; color: #555; }
                input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 10px; font-size: 16px; margin-bottom: 12px; transition: 0.3s; }
                input:focus { border-color: #3f51b5; outline: none; box-shadow: 0 0 0 2px rgba(63,81,181,0.1); }
                .add-btn { background: #2e7d32; color: white; border: none; padding: 16px; width: 100%; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 8px; }
                .add-btn:disabled { background: #a5d6a7; cursor: not-allowed; }
                .table-wrapper { margin-top: 10px; border-radius: 12px; overflow: hidden; border: 1px solid #eee; }
                table { width: 100%; border-collapse: collapse; background: white; }
                th { background: #f8f9fa; padding: 12px; text-align: left; font-size: 11px; color: #888; text-transform: uppercase; border-bottom: 2px solid #eee; }
                td { padding: 14px 12px; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
                .total-tag { color: #2e7d32; font-weight: bold; background: #e8f5e9; padding: 4px 8px; border-radius: 6px; font-size: 13px; }
                .sell-btn { background: #ff9800; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; }
                .loading-overlay { display: none; text-align: center; color: #3f51b5; font-weight: bold; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>👑 Bagaha Seth ERP</h2>
                
                <div id="status-msg" class="loading-overlay">⏳ Thahariye seth, kaam ho raha hai...</div>

                <div class="form-section">
                    <label>Samaan ka Naam</label>
                    <input type="text" id="name" placeholder="Chawal, Tel, etc.">
                    
                    <div style="display: flex; gap: 10px;">
                        <div style="flex: 1;"><label>Packing</label>
                            <select id="p_type">
                                <option value="Bori">Bori</option>
                                <option value="Packet">Packet</option>
                                <option value="Box">Box</option>
                                <option value="Khula (Loose)">Khula (Loose)</option>
                            </select>
                        </div>
                        <div style="flex: 1;"><label>Unit</label>
                            <select id="unit">
                                <option value="kg">kg</option>
                                <option value="Ltr">Ltr</option>
                            </select>
                        </div>
                    </div>

                    <div style="display: flex; gap: 10px;">
                        <div style="flex: 1;"><label>Count</label><input type="number" id="p_count" value="1"></div>
                        <div style="flex: 1;"><label>Wazan/Pack</label><input type="number" id="p_weight" placeholder="50"></div>
                    </div>

                    <button class="add-btn" id="save-btn" onclick="addItem()">💾 Maal Save Karo</button>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead><tr><th>Item</th><th>Qty</th><th>Total</th><th>Action</th></tr></thead>
                        <tbody id="inventory-body"></tbody>
                    </table>
                </div>
            </div>

            <script>
                function showLoad(show) {
                    document.getElementById('status-msg').style.display = show ? 'block' : 'none';
                    document.getElementById('save-btn').disabled = show;
                    document.getElementById('save-btn').innerText = show ? 'Saving...' : '💾 Maal Save Karo';
                }

                async function loadItems() {
                    try {
                        const res = await fetch('/items?api_key=BAGAHA_SETH_100');
                        const data = await res.json();
                        let body = document.getElementById('inventory-body');
                        body.innerHTML = '';
                        data.forEach(item => {
                            body.innerHTML += `<tr>
                                <td><b>${item.name}</b><br><small style="color:gray;">${item.packaging_type}</small></td>
                                <td><b>${item.packages_count}</b></td>
                                <td><span class="total-tag">${item.total_base_weight} ${item.unit || 'kg'}</span></td>
                                <td><button class="sell-btn" onclick="sellItem(${item.id}, ${item.packages_count}, '${item.name}')">🛒 Bika</button></td>
                            </tr>`;
                        });
                    } catch(e) { console.error("Error loading", e); }
                }

                async function addItem() {
                    const n = document.getElementById('name').value;
                    const t = document.getElementById('p_type').value;
                    const u = document.getElementById('unit').value;
                    const c = document.getElementById('p_count').value;
                    const w = document.getElementById('p_weight').value;
                    
                    if(!n || !c || !w) { alert("Seth ji, pura detail bhariye!"); return; }
                    
                    showLoad(true);
                    const res = await fetch(`/add?api_key=BAGAHA_SETH_100&name=${n}&packaging_type=${t}&packages_count=${c}&weight_per_package=${w}&unit=${u}`);
                    showLoad(false);
                    
                    if(res.ok) {
                        document.getElementById('name').value = '';
                        document.getElementById('p_weight').value = '';
                        loadItems(); 
                    } else { alert("Error saving!"); }
                }

                async function sellItem(id, current_qty, item_name) {
                    let qty = prompt(`'${item_name}' abhi ${current_qty} pada hai. Kitna bika?`, "1");
                    if (qty) {
                        showLoad(true);
                        const res = await fetch(`/sell/${id}?api_key=BAGAHA_SETH_100&qty=${qty}`);
                        showLoad(false);
                        if(res.ok) { loadItems(); }
                    }
                }

                loadItems();
            </script>
        </body>
    </html>
    """

# --- BACKEND ROUTES (SAME AS BEFORE) ---
@app.route('/items')
def get_items():
    key = request.args.get('api_key')
    if key != SECRET_KEY: return "Denied", 403
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM ration_items ORDER BY id DESC;')
    data = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(data)

@app.route('/add')
def add_item():
    key = request.args.get('api_key')
    if key != SECRET_KEY: return "Denied", 403
    name, p_type, unit = request.args.get('name'), request.args.get('packaging_type'), request.args.get('unit', 'kg')
    p_count, p_weight = int(request.args.get('packages_count', 0)), float(request.args.get('weight_per_package', 0.0))
    total = p_count * p_weight
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute('INSERT INTO ration_items (name, packaging_type, packages_count, weight_per_package, total_base_weight, unit) VALUES (%s, %s, %s, %s, %s, %s);', (name, p_type, p_count, p_weight, total, unit))
    conn.commit(); cur.close(); conn.close()
    return "OK"

@app.route('/sell/<int:item_id>')
def sell_item(item_id):
    key = request.args.get('api_key')
    if key != SECRET_KEY: return "Denied", 403
    sell_count = int(request.args.get('qty', 1))
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM ration_items WHERE id = %s;', (item_id,))
    item = cur.fetchone()
    if item:
        new_count = item['packages_count'] - sell_count
        if new_count <= 0: cur.execute('DELETE FROM ration_items WHERE id = %s;', (item_id,))
        else:
            new_total = new_count * item['weight_per_package']
            cur.execute('UPDATE ration_items SET packages_count = %s, total_base_weight = %s WHERE id = %s;', (new_count, new_total, item_id))
    conn.commit(); cur.close(); conn.close()
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
