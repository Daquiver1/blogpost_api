"""Functions associated with uuid"""
import uuid


def generate_uuid():
    """Generate uuid for user id."""
    return str(uuid.uuid4())
