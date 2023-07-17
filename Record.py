import pyrebase
import uuid
import os

config = {
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

firebase = pyrebase.initialize_app(config)
database = firebase.database()


def generate_post_id():
    id_str = str(uuid.uuid4())[:8]  # Generates a random UUID and takes first 8 characters
    return id_str


class Record:
    def __init__(self, estimation_date=None, unit=None, progress=1, user_id_token=None, addNote="None",
                 image_paths=None):
        self.estimation_date = estimation_date
        self.piece_name = unit.name if unit else None
        self.piece_size = unit.size if unit else None
        self.piece_edition = unit.ed if unit else None
        self.piece_type = unit.ptype if unit else None
        self.progress = progress
        self.user_id_token = user_id_token
        self.addNote = addNote
        self.post_id = generate_post_id()
        self.image_paths = image_paths if image_paths else []
        self.storage = firebase.storage()

    # this will work with a function in the GUI function to create a post
    def upload_images_to_firebase(self):
        image_urls = []
        for image_path in self.image_paths:
            destination = "post_src/" + self.post_id + "/" + os.path.basename(image_path)
            self.storage.child(destination).put(image_path)
            image_url = self.storage.child(destination).get_url(None)
            image_urls.append(image_url)
        return image_urls  # Returns a list of image URLs

    def upload_record(self):
        record = {
            "post_id": self.post_id,
            "estimation_date": self.estimation_date,
            "piece_name": self.piece_name,
            "piece_size": self.piece_size,
            "piece_edition": self.piece_edition,
            "piece_type": self.piece_type,
            "progress": self.progress,
            "user_id_token": self.user_id_token,
            "addNote": self.addNote,
            "image_paths": self.upload_images_to_firebase()
        }
        database.child("posts").child(self.post_id).set(record)

    def edit_record(self, key, value):
        database.child("posts").child(self.post_id).update({key: value})

    @staticmethod
    def retrieve_record(post_id):
        return database.child("posts").child(post_id).get().val()

    @staticmethod
    def retrieve_records():
        all_records = database.child("posts").get().val()
        record_list = []
        for post_id in all_records:
            record_list.append(Record.retrieve_record(post_id))
        return record_list

    @staticmethod
    def get_record(post_id):
        try:
            record = database.child("posts").child(post_id).get().val()
            if record is None:
                raise ValueError(f"Record with post ID {post_id} not found.")
            else:
                return record
        except ValueError as value_post_error:
            print(value_post_error)

    @staticmethod
    def delete_record(post_id, uid):
        storage = firebase.storage()
        try:
            # Trying to delete with image if possible
            storage.delete("post_src/" + post_id, token=None)
            database.child("posts").child(post_id).remove()
            database.child("Users").child(uid).child("follow_list").child(post_id).remove()
        except:
            # Else we just delete the data without an image directory available
            database.child("posts").child(post_id).remove()
            database.child("Users").child(uid).child("follow_list").child(post_id).remove()

