from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

# Database configuration
DB_FILE = "students.db"

# Create table if not exists
def create_table():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob DATE,
                amount_due REAL
            )
        ''')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)

# Create a new student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (first_name, last_name, dob, amount_due)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, dob, amount_due))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Student created successfully!'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Retrieve all students
@app.route('/students', methods=['GET'])
def get_students():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        rows = cursor.fetchall()
        conn.close()

        students = []
        for row in rows:
            student = {
                'student_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'dob': row[3],
                'amount_due': row[4]
            }
            students.append(student)

        return jsonify(students), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Retrieve a specific student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            student = {
                'student_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'dob': row[3],
                'amount_due': row[4]
            }
            return jsonify(student), 200
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Update a student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students
            SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
            WHERE student_id = ?
        ''', (first_name, last_name, dob, amount_due, student_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Student updated successfully!'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Student deleted successfully!'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
