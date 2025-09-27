# database models

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    completed = db.Column(db.Boolean, nullable = False, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)



    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "completed":self.completed,
            "description":self.description,
            "user_id": self.user_id
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120)  , nullable = False)
    tasks = db.relationship('Tasks', backref='owner', lazy=True)


    def __init__(self, username, password):
        self.username = username
        self.password = password



# flask db init       # Run once to setup migration folder (if not already done)
# flask db migrate    # Everytime we make changes to the database model run this
# flask db upgrade    # Apply migration
