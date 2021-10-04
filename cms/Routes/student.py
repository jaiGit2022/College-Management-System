from flask import Blueprint, request, jsonify
from cms import db

from cms.models.Student import Student
from cms.models.Course import Course

student = Blueprint('student', __name__)


@student.route('/student/')
def student_func():
    return "Hello from student"


@student.route('/student/offered_courses')
def offered_courses():
    res = []
    courses = Course.query.filter(Course.status == 'offered').all()
    for course in courses:
        res.append({"ID": course.id, "Name": course.name, "Credit_Hrs": course.crd_hrs,
                    "Status": course.status, "No of students taken": course.no_of_student_taken,
                    "Assign to": course.assign_to})
    return jsonify(res)


@student.route('/student/availed_courses')
def availed_courses():
    res = []
    student_id = request.args.get('student_id')
    courses = Student.query.filter(Student.id == student_id).first().courses
    for course in courses:
        res.append({"ID": course.id, "Name": course.name, "Credit_Hrs": course.crd_hrs,
                    "Status": course.status, "No of students taken": course.no_of_student_taken,
                    "Assign to": course.assign_to})
    return jsonify(res)


@student.route('/student/avail_course', methods=["POST"])
def avail_course():
    avail = request.get_json()['avail']
    for obj in avail:
        course = Course.query.get(obj['course_id'])
        student = Student.query.get(obj['student_id'])
        student.courses.append(course)
        course.no_of_student_taken += 1

        if course.no_of_student_taken >= 10:
            course.status = "confirmed"

    try:
        db.session.commit()
    except Exception:
        return "Problem in availing course"

    return "Courses availed successfully"
