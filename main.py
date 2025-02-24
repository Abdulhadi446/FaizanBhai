from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.txt"

# Load data from data.txt as JSON; initialize with default data if file doesn't exist.
def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "inventory": [
                ["Fabric Type", "Quantity", "Stock Value"],
                ["Cotton", "500 meters", "$2000"],
                ["Silk", "300 meters", "$1200"]
            ],
            "sales": [
                ["Customer", "Fabric Type", "Quantity", "Amount"],
                ["Ali Textiles", "Cotton", "100 meters", "$400"]
            ],
            "purchases": [
                ["Supplier", "Fabric Type", "Quantity", "Amount"],
                ["Zain Suppliers", "Silk", "300 meters", "$1200"]
            ],
            "returns": [
                ["Type", "Reference", "Quantity", "Adjustment"],
                ["Sale Return", "Ali Textiles", "10 meters", "$40"],
                ["Purchase Return", "Zain Suppliers", "5 meters", "$20"]
            ],
            "reports": [
                ["Metric", "Value"],
                ["Gross Profit", "$5000"],
                ["Net Profit", "$3500"]
            ]
        }
        save_data(default_data)
        return default_data
    else:
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        return data

# Save the given data (a dictionary) to the TXT file.
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Routes for each page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inventory")
def inventory():
    data = load_data()
    return render_template("inventory.html", table=data.get("inventory", []))

@app.route("/sales")
def sales():
    data = load_data()
    return render_template("sales.html", table=data.get("sales", []))

@app.route("/purchases")
def purchases():
    data = load_data()
    return render_template("purchases.html", table=data.get("purchases", []))

@app.route("/returns")
def returns():
    data = load_data()
    return render_template("returns.html", table=data.get("returns", []))

@app.route("/reports")
def reports():
    data = load_data()
    return render_template("reports.html", table=data.get("reports", []))

@app.route("/all-data")
def all_data():
    data = load_data()
    return render_template("all_data.html", data=data)

# New Manufacturing Process page
@app.route("/manufacturing")
def manufacturing():
    return render_template("manufacturing.html")

# Update route for saving changes; table_name is one of inventory, sales, purchases, returns, or reports.
@app.route("/update/<table_name>", methods=["POST"])
def update(table_name):
    data = load_data()
    new_table = request.json.get("data", [])
    data[table_name] = new_table
    save_data(data)
    return jsonify({"message": f"{table_name.capitalize()} data saved successfully!"})

if __name__ == "__main__":
    app.run()