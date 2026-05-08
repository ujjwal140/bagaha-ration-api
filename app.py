import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# --- CONFIGURATION (PURANI VALUES BARKARAAR HAIN) ---
DB_URL = "postgresql://postgres.ayopsyzeudpawcppwsgg:BagahaRation%402026!@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
SECRET_KEY = "BAGAHA_SETH_100"

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Bagaha Seth ERP Final</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { box-sizing: border-box; }
                body { font-family: sans-serif; background: #eceff1; padding: 10px; margin: 0; }
                .container { max-width: 500px; margin: auto; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
                h2 { color: #2c3e50; text-align: center; margin-bottom: 20px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; }
                input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
                .add-btn { background: #27ae60; color: white; border: none; padding: 15px; width: 100%; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
                .table-wrapper { overflow-x: auto; margin-top: 25px; border-radius: 8px; border: 1px solid #eee; }
                table { width: 100%; border-collapse: collapse; min-width: 400px; }
                th, td { padding: 12px 10px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
                th { background: #f8f9fa; color: #7f8c8d; text-transform: uppercase; font-size: 12px; }
                .total-tag { color: #27ae60; font-weight: bold; background: #e8f5e9; padding: 4px 8px; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>👑 Bagaha Seth ERP</h2>
                
                <div style="background: #fdfdfd; padding: 15px; border-radius: 10px; border: 1px dashed #ccc;">
                    <div class="form-group"><label>Samaan</label><input type="text" id="name" placeholder="Jaise: Chawal"></div>
                    
                    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                        <div style="flex: 1;"><label>Packing</label>
                            <select id="p_type">
                                <option value="Bori">Bori</option>
                                <option value="Packet">Packet</option>
                                <option value="Box">Box</option>
                                <option value="Kg">Kg</option>
                            </select>
                        </div>
                        <div style="flex: 1;"><label>Unit</label>
                            <select id="unit">
                                <option value="kg">kg</option>
                                <option value="Ltr">Ltr</option>
                            </select>
                        </div>
                    </div>

                    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                        <div style="flex: 1;"><label>Count</label><input type="number" id="p_count" value="1"></div>
                        <div style="flex: 1;"><label>Wazan/Pack</label><input type="number" id="p_weight" placeholder="50"></div>
                    </div>

                    <button class="add-btn" onclick="addItem()">➕ Maal Save Karo</button>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead><tr><th>Item</th><th>Pack</th><th>Qty</th><th>Total</th></tr></thead>
                        <tbody id="inventory-body"></tbody>
                    </table>
                </div>
            </div>

            <script>
                async function loadItems() {
                    const res = await fetch('/items?api_key=BAGAHA_SETH_100');
                    const data = await res.json();
                    let body = document.getElementById('inventory-body');
                    body.innerHTML = '';
                    data.forEach(item => {
                        body.innerHTML += `<tr>
                            <td><b>${item.name}</b></td>
                            <td>${item.packaging_type}</td>
                            <td>${item.packages_count}</td>
                            <td><span class="total-tag">${item.total_base_weight} ${item.unit || 'kg'}</span></td>
                        </tr>`;
                    });
                }

                async function addItem() {
                    const n = document.getElementById('name').value;
                    const t = document.getElementById('p_type').value;
                    const u = document.getElementById('unit').value;
                    const c = document.getElementById('p_count').value;
                    const w = document.getElementById('p_weight').value;
                    if(!n || !c || !w) { alert("Seth ji, pura detail bhariye!"); return; }
                    const res = await fetch(`/add?api_key=BAGAHA_SETH_100&name=${n}&packaging_type=${t}&packages_count=${c}&weight_per_package=${w}&unit=${u}`);
                    if(res.ok) { location.reload(); } else { alert("Error!"); }
                }
                loadItems();
            </script>
        </body>
    </html>
    """

@app.route('/items')
def get_items():
    key = request.args.get('api_key')
    if key != SECRET_KEY: return "Access Denied", 403
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
    name = request.args.get('name')
    p_type = request.args.get('packaging_type')
    unit = request.args.get('unit', 'kg')
    p_count = int(request.args.get('packages_count', 0))
    p_weight = float(request.args.get('weight_per_package', 0.0))
    total = p_count * p_weight
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''INSERT INTO ration_items (name, packaging_type, packages_count, weight_per_package, total_base_weight, unit) 
                   VALUES (%s, %s, %s, %s, %s, %s);''', (name, p_type, p_count, p_weight, total, unit))
    conn.commit(); cur.close(); conn.close()
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
