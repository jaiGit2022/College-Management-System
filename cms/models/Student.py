from cms import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Student :  {self.id} , {self.name}'