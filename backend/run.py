# Ponto de entrada da API.
# Para rodar: flask --app run run --port 5001 --debug
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5001, debug=True)
