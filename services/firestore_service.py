from firebase_admin import firestore
from services.firebase_app import firebase_app

firestore_db = firestore.client(app=firebase_app)
