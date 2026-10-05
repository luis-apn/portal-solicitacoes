from app.errors import AppError
from app.models import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()

    # A mesma mensagem para "usuário não existe" e "senha errada",
    # para não revelar quais usuários existem no sistema.
    if user is None or not user.check_password(password):
        raise AppError("Usuário ou senha inválidos.", 401)

    return user
