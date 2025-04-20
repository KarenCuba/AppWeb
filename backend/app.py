from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database='tareas',
        user='postgres',
        password='postgres'
    )
    return conn

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title FROM tasks;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'id': row[0], 'title': row[1]} for row in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (title) VALUES (%s) RETURNING id;', (title,))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': task_id, 'title': title}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0')