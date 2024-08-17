from waitress import serve
from BonReader.wsgi import (
    application,
)  # Adjust this import to your project's WSGI application


def run_server():
    """Run the Django application using Waitress."""
    serve(application, host="localhost", port=8080)


if __name__ == "__main__":
    run_server()
