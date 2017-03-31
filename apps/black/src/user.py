class User:

    def __init__(self, id, first_name, surname):
        self.id = id
        self.first_name  = first_name
        self.surname = surname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
            return self.id

    def __repr__(self):
        return '<User %r>' % (self.first_name)
