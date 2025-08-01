from datetime import datetime, timezone


def now():
    """Get the current UTC time."""
    return datetime.now(timezone.utc)
