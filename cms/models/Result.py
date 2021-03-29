from cms import db


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(5), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    entered_by = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    obtained_by = db.Column(db.Integer, db.ForeignKey('student.id'))
    course = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return f'Result :  {self.id} , {self.marks}'