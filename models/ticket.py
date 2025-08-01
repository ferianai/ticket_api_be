from instance.database import db


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Ticket {self.id} for {self.event_name} at {self.location} on {self.time}>"
