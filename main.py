from flask import Flask, jsonify
import psycopg2
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
def connect_db():

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/data', methods=['GET'])
def get_data():
    connection = connect_db()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {os.getenv("TABLE")};")
        data = cursor.fetchall()
        
        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in data]
        
        cursor.close()
        connection.close()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  