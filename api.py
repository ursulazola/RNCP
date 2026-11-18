from flask import Flask, jsonify, request
import pandas as pd
import sqlite3
from functools import wraps
import os
import secrets

####
from dotenv import load_dotenv
load_dotenv(override=True)

VALID_KEYS = {k.strip() for k in os.environ['API_KEY'].split(',') if k.strip()}
#####

app = Flask(__name__)


def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key", "")
        key_b = key.encode("utf-8")
        if not key or not any(
            secrets.compare_digest(key_b, k.encode("utf-8")) for k in VALID_KEYS
        ):
            return jsonify(error="Clé API invalide ou absente"), 401
        return f(*args, **kwargs)
    return wrapper

@app.route("/health", methods=["GET"])
@require_api_key
def get_data():
    
    if __name__ == "__main__":
     return jsonify({"message" : "L'API fonctionne."}), 200
    else : 
     return jsonify({ "message" : "L'API ne fonctionne pas."}), 400


@app.route("/sales-by-country", methods=["GET"])
@require_api_key
def get_data_2():
    conn = sqlite3.connect("tables_finales.db")

    df = pd.read_sql("SELECT * FROM sales_by_country;", conn)
    conn.close()

    return jsonify(df.to_dict(orient="records"))

@app.route("/sales-by-category", methods=["GET"])
@require_api_key
def get_data_3():
    conn = sqlite3.connect("tables_finales.db")

    df = pd.read_sql("SELECT * FROM sales_by_category;", conn)
    conn.close()

    return jsonify(df.to_dict(orient="records"))
    

if __name__ == "__main__":
    app.run(debug=False)