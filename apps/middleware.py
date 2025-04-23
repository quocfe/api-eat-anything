from functools import wraps
from flask import request, abort

VALID_TOKEN = "123456"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            abort(401, description="Missing Authorization header")

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            abort(401, description="Invalid Authorization header format")

        token = parts[1]

        if token != VALID_TOKEN:
            abort(403, description="Invalid token")

        return f(*args, **kwargs)

    return decorated
