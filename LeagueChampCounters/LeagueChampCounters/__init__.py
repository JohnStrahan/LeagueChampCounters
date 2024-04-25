from logging import captureWarnings
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

@app.route('/')
def index():
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
   
    query = "SELECT champion_name FROM champs_and_counters"
    cursor.execute(query)
    data = cursor.fetchall()
   
    cursor.close()
    connection.close()

    return render_template('index.html', data = data)

@app.route('/get_champion_data', methods=['POST'])
def get_champion_data():
    
    champion_name = request.form['champion_name']
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query_champion = "SELECT counter_1, counter_2, counter_3 FROM champs_and_counters WHERE champion_name = %s"
    cursor.execute(query_champion, (champion_name,))
    
    result = cursor.fetchone()

    connection.close()
    
    if result is not None:
        counters = [value if value is not None else "No data" for value in result]
        additional_data = ", ".join(counters)
    else:
        additional_data = "No additional data available"

    return jsonify({'additional_data': additional_data})

if __name__ == '__main__':
    app.run(debug=True)