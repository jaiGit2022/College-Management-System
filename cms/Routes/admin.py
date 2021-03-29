import jwt
import datetime
from flask import Blueprint, request, jsonify
from cms import db, app

from cms.models.Student import Student
from cms.models.Result import Result
from cms.models.Course import Course
from cms.models.Teacher import Teacher
from cms.models.User import User
from flask_login import login_user, current_user, logout_user

from functools import wraps

admin = Blueprint('admin', __name__)


def toke_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print("token : ", token)
        if not token:
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid or expired'})

        return f(*args, **kwargs)

    return decorated


@admin.route('/admin/')
@toke_required
def admin_func():
    return "Token verified"


@admin.route('/admin/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']

    user = User.query.filter(User.name == username).first()
    if user.password == password:
        login_user(user, remember=True)
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})

    return "Unsuccessful Login! Try Again."


@admin.route('/admin/logout')
def logout():
    logout_user()
    return "User Logout Successfully"


@admin.route('/admin/add_courses', methods=['POST'])
def add_course():
    if not current_user.is_authenticated:
        return "Need Login"

    courses = request.get_json()['courses']

    for course in courses:
        data = Course(name=course['name'], crd_hrs=course['crd_hrs'], status=course.get('status', ''))
        try:
            db.session.add(data)
        except:
            return "Problem in adding course"
    db.session.commit()

    return "Courses added successfully"


@admin.route('/admin/add_student', methods=['POST'])
def add_student():
    if not current_user.is_authenticated:
        return "Need Login"
    students = request.get_json()['students']

    for student in students:
        data = Student(name=student['name'], department=student['department'], section=student['section'])
        try:
            db.session.add(data)
        except:
            return "Problem in adding student"
    db.session.commit()

    return "Students added successfully"


@admin.route('/admin/add_teacher', methods=['POST'])
def add_teacher():
    if not current_user.is_authenticated:
        return "Need Login"
    teachers = request.get_json()['teachers']

    for teacher in teachers:
        data = Teacher(name=teacher['name'], department=teacher['department'], specialization=teacher['specialization'],
                       experience=teacher['experience'])
        try:
            db.session.add(data)
        except:
            return "Problem in adding teacher"
    db.session.commit()

    return "Teachers added successfully"


@admin.route('/admin/courses')
def courses():
    if not current_user.is_authenticated:
        return "Need Login"
    res = []
    courses_all = Course.query.all()
    for course in courses_all:
        res.append({"ID": course.id, "Name": course.name, "Credit_Hrs": course.crd_hrs,
                    "Status": course.status, "No of students taken": course.no_of_student_taken,
                    "Assign to": course.assign_to})
    return jsonify(res)


@admin.route('/admin/students')
def students():
    if not current_user.is_authenticated:
        return "Need Login"
    res = []
    students_all = Student.query.all()
    for student in students_all:
        res.append(
            {"ID": student.id, "Name": student.name, "Department": student.department, "Section": student.section})
    return jsonify(res)


@admin.route('/admin/results')
def results():
    if not current_user.is_authenticated:
        return "Need Login"
    res = []
    results = Result.query.all()
    for result in results:
        res.append(
            {"ID": result.id, "Section": result.section, "Marks": result.marks, "Grade": result.grade,
             "Teacher": result.entered_by, "Student": result.obtained_by, "Course": result.course})
    return jsonify(res)


@admin.route('/admin/teachers')
def teachers():
    if not current_user.is_authenticated:
        return "Need Login"
    res = []
    teachers_all = Teacher.query.all()
    for teacher in teachers_all:
        res.append({"ID": teacher.id, "Name": teacher.name, "Department": teacher.department,
                    "Specialization": teacher.specialization, "Experience": teacher.experience})
    return jsonify(res)


@admin.route('/admin/confirmed_courses')
def confirmed_courses():
    if not current_user.is_authenticated:
        return "Need Login"
    res = []
    courses = Course.query.filter(Course.status == "confirmed")
    for course in courses:
        res.append({"ID": course.id, "Name": course.name, "Credit_Hrs": course.crd_hrs,
                    "Status": course.status, "No of students taken": course.no_of_student_taken,
                    "Assign to": course.assign_to})
    return jsonify(res)


@admin.route('/admin/offer_course', methods=["POST"])
def offer_course():
    if not current_user.is_authenticated:
        return "Need Login"
    offer = request.get_json()['offer']
    for obj in offer:
        course = Course.query.get(obj['ID'])
        course.status = "offered"

    try:
        db.session.commit()
    except:
        return "Problem in offering course"

    return "Courses offered successfully"


@admin.route('/admin/assign_course', methods=["POST"])
def assign_course():
    if not current_user.is_authenticated:
        return "Need Login"
    assign = request.get_json()['assign']
    for obj in assign:
        course = Course.query.get(obj['course_id'])
        course.assign_to = obj['teacher_id']

    try:
        db.session.commit()
    except:
        return "Problem in assign course"

    return "Courses assigned successfully"
