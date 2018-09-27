from main.models import db_session, User

def create_user(first_name, last_name, email, password):
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = password

    db_session.add(user)
    db_session.commit()

    return user