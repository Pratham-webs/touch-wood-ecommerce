import os
import random
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. Database Initialization
def init_db():
    # This creates a file named 'store.db' if it doesn't exist
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    
    # Create the Orders table using standard SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            payment_method TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run the setup the moment the server starts
init_db()

@app.route('/api/products', methods=['GET'])
def get_products():
    # Generating 80 mock products for faster loading
    categories = ["men", "women", "kids", "luxury"]
    products = []
    for i in range(1, 20001): 
        # Inside app.py
    
        products.append({
            "id": i,
            "name": f"Touch Wood Drop #{i}",
            "category": random.choice(categories),
            "price": random.randint(899, 2999),
            "desc": "Premium streetwear. Minimalist design.",
            "rating": round(random.uniform(3.8, 4.9), 1),
            "reviews": random.randint(10, 300)
        })
        
    return jsonify(products)

@app.route('/api/checkout', methods=['POST'])
def process_checkout():
    data = request.json
    # Convert the cart array into a string so it fits in a single database column
    cart_items = str(data.get('cart')) 
    method = data.get('payment_method')

    # 2. Insert the new order into the database
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    
    # SQL query to write the data securely
    cursor.execute('INSERT INTO orders (items, payment_method) VALUES (?, ?)', (cart_items, method))
    conn.commit()
    
    # Grab the auto-generated ID of the order we just saved
    new_order_id = cursor.lastrowid 
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Order permanently saved to SQLite database.",
        "order_id": new_order_id
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)