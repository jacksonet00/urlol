from app import login_manager
from models import User


@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user
