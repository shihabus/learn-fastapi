from passlib.context import CryptContext

# for password hashing default the algorithm to bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)
