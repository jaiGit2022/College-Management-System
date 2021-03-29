from cms import db

Enrollments = db.Table('enrollment',
                       db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
                       db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True)
                       )
