from cms import db


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Teacher :  {self.id} , {self.name}'
