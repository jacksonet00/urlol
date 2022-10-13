from app import db, app
from models import User, Alias, Shortcut
from models import SearchableWebsite
from bcrypt import hashpw, gensalt

with app.app_context():
    Shortcut.query.delete()
    Alias.query.delete()
    User.query.delete()

    hashed_password = hashpw('misamisa'.encode('utf8'), gensalt())
    default_user = User(email='light@gmail.com', password=hashed_password)

    # default_alias = Alias(
    #     name='mm', url='https://www.google.com/search?q=misa%20misa&tbm=isch&hl=en&sa=X&ved=0CAEQv7IFahcKEwiwiYLioMr6AhUAAAAAHQAAAAAQBg&biw=1629&bih=894&dpr=2.2', user_id=default_user_id)

    # default_shortcut = Shortcut(
    #     prefix='w', website=SearchableWebsite.WIKIPEDIA, user_id=default_user_id)

    db.session.add(default_user)
    # db.session.add(default_alias)
    # db.session.add(default_shortcut)

    db.session.commit()
