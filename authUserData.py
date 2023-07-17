import csv
import pandas as pd
from pyrebase import pyrebase


class VerifiedUserList:
    def __init__(self, filename):
        self.filename = filename
        # Initialize Firebase
        self.firebase_config = {
            # Enter your Firebase configuration here
            "apiKey": "AIzaSyB5YGX_Zn3doP8f6KhpjnCf8KEyL_CP0Xc",
            "authDomain": "axpatina-db.firebaseapp.com",
            "projectId": "axpatina-db",
            "storageBucket": "axpatina-db.appspot.com",
            "messagingSenderId": "1046461147879",
            "appId": "1:1046461147879:web:428c5f2a61a71639e7d042",
            "measurementId": "G-9MV2J5ZG25",
            'databaseURL': "https://axpatina-db-default-rtdb.firebaseio.com/"
        }
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.storage = self.firebase.storage()

    def create_verified_list(self, emails):
        with open(self.filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(emails)

    def add_email(self, email):
        with open(self.filename, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([email])

    def upload_list_to_firebase(self):
        self.storage.child(self.filename).put(self.filename)

    def download_list_from_firebase(self):
        self.storage.child(self.filename).download(self.filename, self.filename)

    def check_email(self, email):
        self.download_list_from_firebase()
        df = pd.read_csv(self.filename)
        return email in df.values

    def check_password(self, email, password):
        self.download_list_from_firebase()
        df = pd.read_csv(self.filename)
        user_row = df[df["Email"] == email]
        if not user_row.empty:
            return user_row["Password"].values[0] == password
        return False
