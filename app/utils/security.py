import bcrypt

def get_password_hash(password:str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )


