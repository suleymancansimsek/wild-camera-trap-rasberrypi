# firebase_utils.py
import firebase_admin
from firebase_admin import credentials, storage, db
from config import firebase_config

def initialize_firebase():
    cred = credentials.Certificate(firebase_config['credential_path'])
    firebase_admin.initialize_app(cred, {
        'storageBucket': firebase_config['storage_bucket'],
        'databaseURL': firebase_config['database_url'],
    })
    return storage.bucket(), db.reference('/')
