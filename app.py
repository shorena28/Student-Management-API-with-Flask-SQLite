from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Float, nullable=False)


with app.app_context():
    if not os.path.exists('students.sqlite'):
        db.create_all()


@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name, "grade": s.grade} for s in students])


@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({"id": student.id, "name": student.name, "grade": student.grade})


@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    if 'name' not in data or 'grade' not in data:
        return jsonify({"error": "Missing data"}), 400
    new_student = Student(name=data['name'], grade=data['grade'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully!"}), 201


@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted!"})


@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    student.name = data.get('name', student.name)
    student.grade = data.get('grade', student.grade)
    db.session.commit()
    return jsonify({"message": "Student updated!"})

if __name__ == '__main__':
    app.run(debug=True)


