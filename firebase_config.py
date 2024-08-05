import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("braude-92cfa-firebase-adminsdk-mzjxo-76c997880d.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()