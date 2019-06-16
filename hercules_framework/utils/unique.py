import uuid

def unique():
    return str(uuid.uuid4())


def unique_hex():
    return uuid.uuid4().hex
