import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("db_private_tokens\\axpatina-db-firebase-adminsdk-o5ifs-77954c9d02.json")
firebase_admin.initialize_app(cred)

firebase_admin.initialize_app(cred, {
    'storageBucket': "axpatina-db.appspot.com"
})

