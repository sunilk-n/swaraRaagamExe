from firebase_admin import credentials, initialize_app, get_app

from services.firebase_config import get_firebase_config


def get_firestore_app():
    try:
        app = get_app()
    except ValueError as err:
        cred = credentials.Certificate(get_firebase_config())
        app = initialize_app(credential=cred)

    return app


firebase_app = get_firestore_app()
