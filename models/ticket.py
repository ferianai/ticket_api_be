from instance.database import db
from shared.crono import now


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, default=now, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

    # Ensure unique constraint for event_name, location, and time
    __table_args__ = (
        db.UniqueConstraint(
            "event_name", "location", "time", name="uq_event_location_time"
        ),
    )

    def __repr__(self):
        return f"<Ticket {self.id} for {self.event_name} at {self.location} on {self.time}>"
