# =========================================
# 🧠 BACKEND API: CRUD + Security Logic
# Render par deploy hone wala Flask server
# =========================================

from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# 🔐 Secret API Key
SECRET_KEY = "BAGAHA_SETH_100"

# Supabase PostgreSQL connection
conn = psycopg2.connect(
    host="postgresql://postgres.ayopsyzeudpawcppwsgg:[YOUR-PASSWORD]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres",
    database="postgres",
    user="postgres",
    password="BagahaRation@2026!",
    port=6543
)

# 🔐 Har request mein API Key check hoga
def check_key(req):
    api_key = req.headers.get("x-api-key")

    if api_key != SECRET_KEY:
        return False

    return True

# =========================================
# 📖 GET: Bacha hua stock dekhne ke liye
# =========================================
@app.route("/items", methods=["GET"])
def get_items():

    if not check_key(request):
        return jsonify({"message": "Access Denied"}), 401

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")

    items = cursor.fetchall()

    return jsonify(items)

# =========================================
# ➕ POST: Naya item add karne ke liye
# =========================================
@app.route("/items", methods=["POST"])
def add_item():

    if not check_key(request):
        return jsonify({"message": "Access Denied"}), 401

    data = request.json

    name = data["name"]
    stock = data["stock"]

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO items (name, stock) VALUES (%s, %s)",
        (name, stock)
    )

    conn.commit()

    return jsonify({"message": "Item Added"})

# =========================================
# ✏️ PUT: Stock minus/update karne ke liye
# =========================================
@app.route("/items/<int:id>", methods=["PUT"])
def update_stock(id):

    if not check_key(request):
        return jsonify({"message": "Access Denied"}), 401

    data = request.json

    minus_stock = data["stock"]

    cursor = conn.cursor()

    # Current stock nikalo
    cursor.execute(
        "SELECT stock FROM items WHERE id=%s",
        (id,)
    )

    result = cursor.fetchone()

    if result is None:
        return jsonify({"message": "Item Not Found"})

    current_stock = result[0]

    # 🔍 If/Else check: stock available hai ya nahi
    if minus_stock > current_stock:

        return jsonify({
            "message": "Stock Not Available"
        })

    else:

        # Stock minus karo
        new_stock = current_stock - minus_stock

        cursor.execute(
            "UPDATE items SET stock=%s WHERE id=%s",
            (new_stock, id)
        )

        conn.commit()

        return jsonify({
            "message": f"Stock Updated. Remaining = {new_stock}"
        })

# =========================================
# ❌ DELETE: Kharab item delete karne ke liye
# =========================================
@app.route("/items/<int:id>", methods=["DELETE"])
def delete_item(id):

    if not check_key(request):
        return jsonify({"message": "Access Denied"}), 401

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM items WHERE id=%s",
        (id,)
    )

    conn.commit()

    return jsonify({
        "message": "Item Deleted"
    })

# Flask server start
if __name__ == "__main__":
    app.run(debug=True)
