from passlib.context import CryptContext

# for password hashing default the algorithm to bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

# verify password hash
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)