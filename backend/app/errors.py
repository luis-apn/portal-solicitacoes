from flask import jsonify

from app.extensions import db


class AppError(Exception):
    """Erro esperado da aplicação (validação, permissão, regra de negócio).

    Os services lançam AppError e o handler abaixo transforma em resposta JSON.
    Assim todas as respostas de erro têm o mesmo formato:
        {"error": "mensagem", "details": {...}}
    """

    def __init__(self, message, status_code=400, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        body = {"error": error.message}
        if error.details:
            body["details"] = error.details
        return jsonify(body), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Recurso não encontrado."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Método não permitido."}), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        # Desfaz qualquer alteração pela metade e não mostra detalhes do erro ao usuário.
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor."}), 500
