from database.database import sessionLocal

from models.user_model import User

from core.security import hash_password


db = sessionLocal()


user = User(
    username="nithesh",
    hashed_password=hash_password("123456")
)


db.add(user)
db.commit()

db.close()

print("User created")