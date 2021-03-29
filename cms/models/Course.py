from cms import db
from .Enrollment import Enrollments


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    crd_hrs = db.Column(db.Integer)
    no_of_student_taken = db.Column(db.Integer, default=0)
    status = db.Column(db.String(10))

    assign_to = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    enrollments = db.relationship('Student', secondary=Enrollments, backref=db.backref('courses'))

    def __repr__(self):
        return f'Course :  {self.id} , {self.name}'
