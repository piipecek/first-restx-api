from website import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(200))
    
    def get_roles(self):
        return [] # po integraci s db tu přibudou system_names rolí
    
    @staticmethod
    def get_all():
        return db.session.scalars(db.select(User)).all()
    
    @staticmethod
    def get_by_email(email) -> "User":
        return db.session.scalars(db.select(User).where(User.email == email)).first()
    
    @staticmethod
    def get_by_id(id):
        return db.session.get(User, id)