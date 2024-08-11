from models.users import User
from engine.engine import session

# Show users - Simple Query Test
users = session.query(User).all()

for user in users:
    print(f"User ID: {user.Id}, Manager ID: {user.ManagerId}, TypeOfWork ID: {user.TypeOfWorkId}, Role ID: {user.RoleId}")