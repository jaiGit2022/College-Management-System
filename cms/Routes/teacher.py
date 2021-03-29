from flask import Blueprint, request, jsonify
from cms import db
from cms.models.Result import Result
from cms.models.Course import Course

teacher = Blueprint('teacher', __name__)


@teacher.route('/teacher/')
def teacher_func():
    return "Hello from teacher"


@teacher.route('/teacher/courses/')
def assign_courses():
    teacher_id = request.args.get('teacher_id')
    res = []
    courses_all = Course.query.filter(Course.assign_to == teacher_id)
    for course in courses_all:
        res.append({"ID": course.id, "Name": course.name, "Credit_Hrs": course.crd_hrs,
                    "Status": course.status, "No of students taken": course.no_of_student_taken,
                    "Assign to": course.assign_to})
    return jsonify(res)


@teacher.route('/teacher/add_marks', methods=['POST'])
def add_marks():
    data = request.get_json()['marks']
    for val in data:
        obj = Result(section=val['section'], marks=val['marks'], grade=val['grade'], entered_by=val['teacher_id'],
                     obtained_by=val['student_id'], course=val['course_id'])
        try:
            db.session.add(obj)
        except:
            return "Problem in adding marks"
    db.session.commit()

    return "Marks added successfully"
