import random
from datetime import datetime, timedelta
import time
from tqdm import tqdm
from prettytable import PrettyTable
from Sculpture import piece
from Record import Record
import authUserData as ud
from GUI import *
from User import User


def connection_initialize():

    print("Initialising server retrieval protocol...")

    for i in tqdm(range(100), desc="Loading..."):
        time.sleep(0.05)  # simulate time delay

    print("\nServer retrieval protocol initialised.\n")

    print("Fetching server metadata...")

    for i in tqdm(range(100), desc="Loading..."):
        time.sleep(0.02)  # simulate time delay

    print("\nServer metadata fetched.\n")

    print("Retrieving server databases...")

    for i in tqdm(range(100), desc="Loading..."):
        time.sleep(0.03)  # simulate time delay

    print("\nServer databases retrieved.\n")

    print("Commencing server retrieval...\n")

    for i in tqdm(range(100), desc="Retrieving..."):
        time.sleep(0.05)  # simulate time delay

    print("\nServer retrieval process complete. Server is now locally available.\n Users Available:")
    table = PrettyTable()

    # Add columns
    table.field_names = ["User ID", "First Name", "Last Name", "Email", "Last Login"]

    # Add rows with invented names
    table.add_row(["001", "Oliver", "Twist", "oliver.twist@example.com", "2023-07-01 09:00:00"])
    table.add_row(["002", "Sophie", "Turner", "sophie.turner@example.com", "2023-07-02 10:00:00"])
    table.add_row(["003", "Elijah", "Wood", "elijah.wood@example.com", "2023-07-03 11:00:00"])
    table.add_row(["004", "Amelia", "Pond", "amelia.pond@example.com", "2023-07-04 12:00:00"])
    print(table)


def test_function():
    token_id = "6D5Hjty0iAMqxN4KIXWVcjQ1OFr1"  # Replace with your token
    piece_types = ["Color", "Monochrome", "Sepia"]  # Add more types as needed

    for _ in range(5):
        # Create a random future date within next 30 days for the estimation_date
        random_future_days = timedelta(days=random.randint(1, 30))
        estimation_date = (datetime.now() + random_future_days).isoformat()

        # Create a random unit (i.e., a piece)
        piece_name = "Piece " + str(random.randint(1, 100))
        piece_size = str(random.randint(1, 100)) + "cm"
        piece_edition = "Edition " + str(random.randint(1, 10))
        piece_type = random.choice(piece_types)
        unit = piece(piece_name, piece_size, piece_edition, piece_type)

        # Create a random progress value between 1 and 100
        progress = random.randint(1, 100)

        # Create a reasonable note
        note = "This is a note for post with estimation_date: " + estimation_date

        # Create a new Record and upload it
        record = Record(estimation_date, unit, progress, token_id, note)
        record.upload_record()

        # Retrieve and print the newly created record
        print(Record.retrieve_record(record.post_id))

    # Retrieve and print all records
    all_records = Record.retrieve_records()
    for record in all_records:
        print(record)


if __name__ == '__main__':
    # GUI------------------todo login
    # login_window = LoginWindow()
    # login_window.mainloop()

    # GUI --------------------todo MainWindow


    # Create the MainWindow

    if input("trace server: (1/0) ").lower() == "1":
        connection_initialize()

    user = User(email="AXrecordNotification@gmail.com", password="(/}n"
                                                                 "}*M["
                                                                 "'SM!c%Cv0e7W")

    window = MainWindow(user=user)

    # Run the window
    window.mainloop()

    # test_function()
