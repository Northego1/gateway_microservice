import bcrypt

def hash_password(
        password: str
) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(rounds=10)
    )


