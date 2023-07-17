import os

from firebase_admin import credentials, auth
from firebase_admin import db
import pyrebase
from datetime import datetime, timedelta
from Record import Record

firebase_config = {
    "apiKey": "AIzaSyB5YGX_Zn3doP8f6KhpjnCf8KEyL_CP0Xc",
    "authDomain": "axpatina-db.firebaseapp.com",
    "projectId": "axpatina-db",
    "storageBucket": "axpatina-db.appspot.com",
    "messagingSenderId": "1046461147879",
    "appId": "1:1046461147879:web:428c5f2a61a71639e7d042",
    "measurementId": "G-9MV2J5ZG25",
    'databaseURL': "https://axpatina-db-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()


class User:
    def __init__(self, email, password):
        self.email = email.replace('.', ',')  # replace . with , in the email
        self.password = password
        self.uid = None
        self.follow_list = None

    def upload_image_DB(self, local_image_path):
        user = self.verify_user()
        if user is None:
            return  # User verification failed, exit the function

        uid = user['localId']
        try:
            # Path in Firebase Storage where the image will be saved
            storage_path = f"user_profile_pictures/{uid}/image.jpg"

            # Upload the image
            storage.child(storage_path).put(local_image_path)

            # Update 'image' field in the Firebase database
            db.child("Users").child(uid).update({'image': storage_path})

            print(f"Successfully uploaded the image to: {storage_path}")
        except Exception as e:
            print(f"An error occurred while uploading the image: {str(e)}")

    def download_image_DB(self, download_path):
        user = self.verify_user()
        if user is None:
            return  # User verification failed, exit the function

        uid = user['localId']
        try:
            # Path in Firebase Storage where the image is saved
            storage_path = f"user_profile_pictures/{uid}/image.jpg"

            # Get file extension from Firebase Storage path
            _, ext = os.path.splitext(storage_path)

            # Add file extension to local path
            download_path_with_ext = download_path + ext

            # Download the image
            storage.child(storage_path).download(download_path_with_ext)

            print(f"Successfully downloaded the image to: {download_path_with_ext}")

            # Update 'image' field in the Firebase database
            db.child("Users").child(uid).update({'image': download_path_with_ext})

            return download_path_with_ext  # Return the path of the downloaded image
        except Exception as e:
            print(f"An error occurred while downloading the image: {str(e)}")

    def update_user_data(self, update_data):
        user = self.verify_user()
        if user is None:
            return  # User verification failed, exit the function

        uid = user['localId']
        try:
            db.child("Users").child(uid).update(update_data)
            print(f"Successfully updated the user data in the DB under UID: {uid}")
        except Exception as e:
            print(f"An error occurred while updating the user data in the DB: {str(e)}")

    def verify_user(self):
        try:
            user = auth.sign_in_with_email_and_password(self.email.replace(',', '.'), self.password)
            if user is not None:
                # Retrieve and set user details from the database
                self.uid = user['localId']  # Set the uid of the User object
                user_data = db.child("Users").child(self.uid).get().val()  # Assuming user data is available in DB
                self.name = user_data['name']
                self.process_stand = user_data['processStand']
                self.user_image = user_data['image']
                self.follow_list = user_data.get('follow_list', [])  # Get the follow list for the user
                if 'follow_list' not in user_data:
                    db.child("Users").child(self.uid).update({'follow_list': self.follow_list})  # Initialize in DB
            return user  # User is verified, return the user object
        except Exception as e:
            print(f"Failed to verify user: {str(e)}")  # Print the error
            return None  # User verification failed

    def register_user(self):
        try:
            # First, create the user in Firebase Authentication
            user = auth.create_user_with_email_and_password(self.email.replace(',', '.'), self.password)

            uid = user['localId']  # Get the UID of the newly created user
            self.uid = uid  # Assign the UID to the User instance

            # Prepare the user info to be stored in the database
            user_info = {
                'name': self.name,
                'processStand': self.process_stand,
                'email': self.email,
                'image': self.user_image,
                'last_name_change': str(datetime.now()),  # Store current datetime as the last name change
                'follow_list': self.follow_list or []  # Initialize the follow_list to an empty list
            }

            # Store the user info in the database
            db.child("Users").child(uid).set(user_info)

            print(f"Successfully registered the user in the DB under UID: {uid}")
            return True

        except Exception as e:
            print(f"An error occurred while registering the user in the DB: {str(e)}")
            return False

    def get_user_data(self):
        user = self.verify_user()
        if user is None:
            return  # User verification failed, exit the function

        uid = user['localId']
        try:
            user_data = db.child("Users").child(uid).get()
            return user_data.val()  # Return the data of the user
        except Exception as e:
            print(f"An error occurred while getting the user data: {str(e)}")

    @staticmethod
    def get_user_data_void(user_uid):
        try:
            user_data = db.child("Users").child(user_uid).get()
            return user_data.val()  # Return the data of the user
        except Exception as e:
            print(f"An error occurred while getting the user data: {str(e)}")
            return None

    def change_user_name(self, new_name):
        user = self.verify_user()
        if user is None:
            return  # User verification failed, exit the function

        uid = user['localId']
        try:
            user_data = db.child("Users").child(uid).get().val()
            last_name_change = datetime.strptime(user_data['last_name_change'], "%Y-%m-%d %H:%M:%S.%f")

            # Check if more than 14 days have passed since last name change and new name is different
            if datetime.now() - last_name_change > timedelta(days=14) and user_data['name'] != new_name:
                user_data['name'] = new_name
                user_data['last_name_change'] = str(datetime.now())  # Reset the last name change time

                # Update the user data in Firebase
                db.child("Users").child(uid).set(user_data)
                return f"Successfully changed the user's name to: {new_name}"

            else:
                return "Cannot change user's name. Either less than 14 days have passed since the last name change, " \
                       "or the new name is the same as the current one."
        except Exception as e:
            print(f"An error occurred while changing the user's name: {str(e)}")

    def follow_post(self, post_id):
        # Retrieve the current follow list
        self.retrieve_follow_list()

        # Check if the list contains only a single "None" element
        if len(self.follow_list) == 1 and self.follow_list[0] == "None":
            self.follow_list[0] = post_id  # Replace "None" with post_id
        elif post_id not in self.follow_list:
            self.follow_list.append(post_id)
            print(f"post with {post_id} added to Follow list")

        # Update the entire follow list in Firebase
        db.child("Users").child(self.uid).update({"follow_list": self.follow_list})

    def unfollow_post(self, post_id):
        # Retrieve the current follow list
        self.retrieve_follow_list()

        if post_id in self.follow_list:
            self.follow_list.remove(post_id)
            # If the list is empty after removing, add "None"
            if len(self.follow_list) == 0:
                self.follow_list.append("None")

        # Update the entire follow list in Firebase
        db.child("Users").child(self.uid).update({"follow_list": self.follow_list})

    def retrieve_follow_list(self):
        follow_list = db.child("Users").child(self.uid).child("follow_list").get().val() or []
        self.follow_list = follow_list
        return self.follow_list
