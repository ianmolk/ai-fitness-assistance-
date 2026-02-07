from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.column(db.String(120), unqiue= True, nullable=False)
    password = db.column(db.String(200), nullable=False)


    def __repr__(self):return f"<User {self.email}>"

    
