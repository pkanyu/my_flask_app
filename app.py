from flask import Flask, jsonify, request
import os



secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URI')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}, {'id': 3, 'name': 'Item 3'}]

@app.route('/')
def home():
    return "Welcome to my Flask REST API!"

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/api/items/add', methods=['POST'])
def create_item():
    data = request.json
    new_item = create_new_item(data)
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        data = request.json
        item.update(data)
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = get_item_by_id(item_id)
    if item:
        items = [i for i in items if i['id'] != item_id]
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

def create_new_item(data):
    item_id = len(items) + 1
    new_item = {'id': item_id, 'name': data['name']}
    items.append(new_item)
   
    return new_item  # Make sure to return the new item

def get_item_by_id(item_id):
    # Example implementation to fetch an item by its ID
    for item in items:
        if item['id'] == item_id:
            return item
    return None

if __name__ == '__main__':
    app.run(debug=False)
