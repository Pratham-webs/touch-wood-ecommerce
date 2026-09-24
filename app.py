from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # This allows your frontend (HTML) to communicate with this backend

# 1. The Database Simulation
# In a production environment, this would be an SQLite or PostgreSQL database.
base_catalog = [
    { "id": 1, "name": "Yash Exclusive Raw Denim Jacket", "category": "actors", "price": 2199, "image": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=500&q=80" },
    { "id": 2, "name": "Mamitha's Gen-Z Oversized Graphic Tee", "category": "actors", "price": 699, "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&q=80" },
    { "id": 6, "name": "Infant Hypoallergenic Bamboo Romper", "category": "kids", "price": 499, "image": "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=500&q=80" },
]

# Generate the rest of the 8000 products in backend memory
for i in range(7, 8001):
    base_catalog.append({
        "id": i,
        "name": f"Touch Wood Premium Apparel {i}",
        "category": random.choice(["men", "women", "kids"]),
        "price": random.randint(499, 2999),
        "image": "https://images.unsplash.com/photo-1516826957135-700ede19c6ce?w=500&q=80"
    })

# 2. API Endpoint: Send products to the frontend
@app.route('/api/products', methods=['GET'])
def get_products():
    # We send the data in JSON format, which JavaScript understands natively
    return jsonify({
        "status": "success",
        "total_products": len(base_catalog),
        "data": base_catalog
    })

# 3. API Endpoint: Process the checkout
@app.route('/api/checkout', methods=['POST'])
def process_checkout():
    order_data = request.json
    
    # In a real app, you would save order_data to your database here.
    print("\n--- NEW ORDER RECEIVED ---")
    print(f"Customer Cart: {order_data['cart']}")
    print(f"Payment Method: {order_data['payment_mode']}")
    print("--------------------------\n")
    
    # Generate an order ID
    order_id = f"TW-{random.randint(100000, 999999)}"
    
    return jsonify({
        "status": "success", 
        "message": "Order placed securely via Yelahanka server.", 
        "order_id": order_id
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port)