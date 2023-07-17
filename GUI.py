import tkinter

import pyrebase
from tkinter import *
from tkinter import messagebox
from pathlib import Path
from User import User
from PIL import Image, ImageTk
from tkinter import filedialog
from Record import Record
from threading import Thread, Event
from tkinter import ttk
import time
from Sculpture import piece

# Set up your Firebase configuration
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
auth = firebase.auth()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("images/icons/LoginWindow_/")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def relative_location(self, objective_position: tuple):
    original_size = (1920, 1080)  # Original design size
    original_width, original_height = original_size
    objective_x, objective_y = objective_position

    relative_x = int((objective_x / original_width) * self.screen_width)
    relative_y = int((objective_y / original_height) * self.screen_height)

    return relative_x, relative_y


class LoginWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.canvas = Canvas(
            self,
            bg="#000000",
            height=600,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(401.0, 297.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(400.0, 217.0, image=self.image_image_2)

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(401.0, 383.0, image=self.entry_image_1)
        self.email_entry = Entry(bd=0, bg="#A4A4A4", fg="#000716", highlightthickness=0)
        self.email_entry.place(x=291.0, y=362.0, width=220.0, height=40.0)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(401.0, 462.0, image=self.entry_image_2)
        self.password_entry = Entry(bd=0, bg="#A4A4A4", fg="#000716", highlightthickness=0, show="• ")
        self.password_entry.place(x=293.0, y=439.0, width=216.0, height=44.0)

        self.canvas.create_text(
            287.0,
            340.0,
            anchor="nw",
            text="Email",
            fill="#A4A4A4",
            font=("JostRoman Regular", 16 * -1)
        )

        self.canvas.create_text(
            287.0,
            417.0,
            anchor="nw",
            text="Password",
            fill="#A4A4A4",
            font=("JostRoman Medium", 16 * -1)
        )

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(400.0, 216.0, image=self.image_image_3)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.login_button = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.login_button.configure(bg="#1E1E1E", fg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E")
        self.login_button.place(x=363.0, y=499.0, width=75.0, height=22.0)

        self.attempts = 0  # Initialize the number of attempts

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Create a User object
        user = User(email, password)

        if user.verify_user():
            print("User verification passed.")
            self.attempts = 0
            self.destroy()  # Destroy the login window
            MainWindow(user).mainloop()  # Pass user to MainWindow
        else:
            print("User verification failed.")
            self.attempts += 1
            if self.attempts >= 3:
                self.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password. 330")


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = Canvas(self, bg="#000000")
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview, bg="#000000")
        self.scrollable_window = Frame(canvas, bg="#000000")

        self.scrollable_window.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_window, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class MainWindow(Tk):
    def __init__(self, user, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.stop_event = Event()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width - 10}x{self.screen_height - 10}")
        self.configure(bg="#000000")
        self.resizable(False, False)
        self.user = user
        self.attributes('-fullscreen', False)

        self.title_bar = Frame(self, bg="#1E1E1E", relief="raised", bd=2)
        self.title_bar.pack(fill=BOTH)

        self.scale_x = self.screen_width / 1920
        self.scale_y = self.screen_height / 1080

        self.canvas = Canvas(
            self,
            bg="#000000",
            height=self.screen_height,
            width=self.screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = self.scale_image("images/icons/MainWindow/image_1.png")
        self.image_1 = self.canvas.create_image(*self.relative_location_MainWindow((173.0, 593.0)),
                                                image=self.image_image_1)

        self.image_image_2 = self.scale_image("images/icons/MainWindow/image_2.png")
        self.image_2 = self.canvas.create_image(*self.relative_location_MainWindow((1093.0, 589.0)),
                                                image=self.image_image_2)

        self.image_image_3 = self.scale_image("images/icons/MainWindow/image_3.png")
        self.image_3 = self.canvas.create_image(*self.relative_location_MainWindow((960.0, 55.0)),
                                                image=self.image_image_3)

        self.button_image_1 = self.scale_image("images/icons/MainWindow/button_1.png")
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_settings,
            relief="flat"
        )
        self.button_1.configure(bg="#1E1E1E", fg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E")
        self.button_1.place(x=self.relative_location_MainWindow((85.0, 187.0))[0],
                            y=self.relative_location_MainWindow((85.0, 187.0))[1],
                            width=int(152.0 * self.scale_x),
                            height=int(57.0 * self.scale_y))

        self.button_image_2 = self.scale_image("images/icons/MainWindow/button_2.png")
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.sign_out,
            relief="flat"
        )
        self.button_2.configure(bg="#1E1E1E", fg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E")
        self.button_2.place(x=self.relative_location_MainWindow((85.0, 971.0))[0],
                            y=self.relative_location_MainWindow((85.0, 971.0))[1],
                            width=int(97.0 * self.scale_x),
                            height=int(26.0 * self.scale_y))

        self.button_image_3 = self.scale_image("images/icons/MainWindow/button_3.png")
        self.toogle_followlist_button = Button(
            self,
            image=self.button_image_3,
            bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E",
            bd=0,
            command=self.toggle_follow_list
        )
        self.toogle_followlist_button.place(
            x=self.relative_location_MainWindow((65.0, 187.0))[0],
            y=self.relative_location_MainWindow((85.0, 243.0))[1],
            width=152.0,
            height=57.0
        )
        self.toogle_followlist_button.configure(bg="#1E1E1E", activebackground="#1E1E1E",
                                                activeforeground="#1E1E1E", fg="#1E1E1E")
        self.create_post_active = False

        self.button_image_createpost = self.scale_image("images/icons/MainWindow/button_4.png")
        self.toogle_createpost_button = Button(
            self,
            image=self.button_image_createpost,
            bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E",
            bd=0,
            command=self.toggle_create_post
        )
        self.toogle_createpost_button.place(
            x=self.relative_location_MainWindow((65.0, 295.0))[0] - 10,
            y=self.relative_location_MainWindow((85.0, 295.0))[1],
            width=150.0,
            height=57.0
        )
        self.toogle_createpost_button.configure(bg="#1E1E1E", activebackground="#1E1E1E",
                                                activeforeground="#1E1E1E", fg="#1E1E1E")

        self.canvas.create_text(
            *self.relative_location_MainWindow((1457.0, 31.0)),
            anchor="nw",
            text="Welcome Back!",
            fill="#717B8C",
            font=("Inter Medium", int(16 * -1 * self.scale_x))  # scale font size
        )

        self.username_label = self.canvas.create_text(
            *self.relative_location_MainWindow((1457.0, 58.0)),
            anchor="nw",
            text=self.user.get_user_data()['name'],
            fill="#4C535F",
            font=("Inter Medium", int(18 * -1 * self.scale_x))  # scale font size
        )

        self.image_image_4 = self.scale_image("images/icons/MainWindow/image_4.png")
        self.image_4 = self.canvas.create_image(
            self.relative_location_MainWindow((322.0, 48.0)),  # subtract 10 from the y-coordinate
            image=self.image_image_4
        )
        if user.get_user_data()['image'] == 'def':
            self.image_image_5 = self.scale_image("images/icons/MainWindow/image_5.png")
            self.image_5 = self.canvas.create_image(*self.relative_location_MainWindow((1409.0, 55.0)),
                                                    image=self.image_image_5)
        else:
            image_path = user.get_user_data()['image']
            if image_path:
                self.image_image_5 = ImageTk.PhotoImage(Image.open(image_path).resize((55, 55)))
                self.image_5 = self.canvas.create_image(*self.relative_location_MainWindow((1409.0, 55.0)),
                                                        image=self.image_image_5)

        # Toggle frame part Settings side toggle frame----------------------------------

        self.toggle_frame = None  # Initially no toggle frame
        self.backButton_Image = ImageTk.PhotoImage(
            file="images/icons/SettingsWindow/button_2.png")  # Keep a reference to the image

        self.image1 = ImageTk.PhotoImage(file="images/icons/SettingsWindow/image_4.png")
        self.toogle_settings_button = Button(
            self.title_bar,
            image=self.image1,
            bg="#000000", activeforeground="#000000", activebackground="#000000",
            bd=0,
            command=self.toggle_settings
        )

        self.image2 = ImageTk.PhotoImage(
            file="images/icons/MainWindow/button_3.png")  # Use your own image file here
        self.toggle_follow_list_button = Button(
            self.title_bar,  # Replace this with the parent widget where you want to place the button
            image=self.image2,
            bg="#000000", activeforeground="#000000", activebackground="#000000",
            bd=0,
            command=self.toggle_follow_list  # Call toggle_follow_list when button is clicked
        )

        self.scrollable_frame = ScrollableFrame(self.canvas)
        self.scrollable_frame.place(x=290, y=138, width=980, height=525)

        # Start a separate thread to periodically update the posts
        self.update_thread = Thread(target=self.update_posts)
        self.update_thread.start()

        self.scrollable_frame.place(x=290, y=138, width=980, height=525)

        self.toogle_settings_button.image = self.button_2  # Keep a reference to the image
        self.toogle_settings_button.pack(side=tkinter.LEFT)
        self.toggle_follow_list_button.image = self.button_image_3
        self.toggle_follow_list_button.pack(side=tkinter.LEFT)

    def follow_list_preview(self, parent, post):
        # Create a frame for the list preview
        list_frame = Frame(parent, bg='#1E1E1E', width=310, height=50)
        list_frame.pack(fill=X, padx=10, pady=5)
        list_frame.pack_propagate(False)
        if post is None or post == "None":
            canvas = Canvas(
                list_frame,
                bg="#1E1E1E",
                height=50,
                width=310,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )

            canvas.place(x=0, y=0)
            self.fl_image_image_1 = PhotoImage(
                file="images/icons/MainWindow/FollowListPreview/frame0/image_1.png")
            image_1 = canvas.create_image(
                155.0,
                20.0,
                image=self.fl_image_image_1
            )
            return list_frame
        # Create the canvas inside the frame
        canvas = Canvas(
            list_frame,
            bg="#1E1E1E",
            height=50,
            width=310,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Create the rectangle
        canvas.create_rectangle(
            135.0,
            5.0,
            261.0,
            46.0,
            fill="#D9D9D9",
            outline="")

        # Create the first button
        button_image_1 = PhotoImage(
            file="images/icons/MainWindow/FollowListPreview/button_1.png")
        button_1 = Button(
            canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=276.0,
            y=10.0,
            width=25.0,
            height=30.0
        )
        button_1.image = button_image_1  # Keep a reference to the image

        # Create the images
        image_image_1 = PhotoImage(
            file="images/icons/MainWindow/FollowListPreview/image_1.png")
        image_1 = canvas.create_image(
            40.0,
            13.0,
            image=image_image_1
        )
        canvas.image1 = image_image_1  # Keep a reference to the image

        image_image_2 = PhotoImage(
            file="images/icons/MainWindow/FollowListPreview/image_2.png")
        image_2 = canvas.create_image(
            40.0,
            33.0,
            image=image_image_2
        )
        canvas.image2 = image_image_2  # Keep a reference to the image

        image_image_3 = PhotoImage(
            file="images/icons/MainWindow/FollowListPreview/image_3.png")
        image_3 = canvas.create_image(
            171.0,
            10.0,
            image=image_image_3
        )
        canvas.image3 = image_image_3  # Keep a reference to the image

        # Return the frame
        return list_frame

    def destroy_toggle_frame_createPost(self):
        # Destroy the entries only for this widget
        self.entry_1.destroy()  # name
        self.entry_2.destroy()  # edition
        self.entry_3.destroy()  # size
        self.entry_4.destroy()  # Estimation date
        self.entry_5.destroy()  # type
        self.entry_6.destroy()  # progress
        self.entry_7.destroy()  # add notes
        self.button_1.destroy()
        self.button_uploadImg.destroy()
        self.toggle_frame.destroy()
        self.toggle_frame = None
        # reset the toggle frame property to None to only have a single one opened

    def gather_post_info(self):
        post_info = {
            "estimation_date": self.entry_4.get(),
            "piece_name": self.entry_1.get(),
            "piece_size": self.entry_3.get(),
            "piece_edition": self.entry_2.get(),
            "piece_type": self.entry_5.get(),
            "progress": self.entry_6.get(),
            "user_id_token": self.user.uid,
            "addNote": self.entry_7.get(),
            # todo
            "image_paths": "None"
        }
        return post_info

    @staticmethod
    def select_images():
        root = Tk()
        root.withdraw()  # we don't want a full GUI, so keep the root window from appearing

        # open the dialog to choose multiple files
        # filetypes argument only allows files of the type .jpg, .jpeg, .png
        file_paths = filedialog.askopenfilenames(filetypes=[('image files', '.jpg .jpeg .png')])

        if file_paths:  # if files were chosen
            return file_paths

        else:
            print("No files chosen.")
            return None

    def create_and_upload_post(self):
        # Gather info from entry fields
        post_info = self.gather_post_info()

        # Create a new Record instance with the gathered info
        record = Record(
            estimation_date=post_info["estimation_date"],
            unit=piece(name=post_info["piece_name"], size=post_info["piece_size"], edition=post_info["piece_edition"],
                       P_type=post_info["piece_type"]),
            progress=post_info["progress"],
            user_id_token=post_info["user_id_token"],
            addNote=post_info["addNote"],
            image_paths=self.selected_image_paths
        )

        # Upload the record
        record.upload_record()

    def toggle_create_post(self):
        if not self.toggle_frame:
            self.create_post_active = True

            self.toggle_frame = Canvas(
                self,
                bg="#FFFFFF",
                height=744,
                width=500,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )

            back_button = Button(
                self.toggle_frame,
                image=self.backButton_Image,
                borderwidth=0,
                highlightthickness=0,
                command=self.destroy_toggle_frame_createPost,
                relief="flat"
            )
            back_button.configure(bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E", fg="#1E1E1E")
            back_button.place(x=450, y=10, width=30.0, height=30.0)

            self.toggle_frame.place(x=0, y=0)
            self.bgCreatePost = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_1.png")
            self.image_1 = self.toggle_frame.create_image(
                250.0,
                372.0,
                image=self.bgCreatePost
            )

            self.image_name_of_Piece = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_2.png")
            self.image_2 = self.toggle_frame.create_image(
                111.0,
                127.0,
                image=self.image_name_of_Piece
            )

            self.entryImage_createPost1 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_1.png")
            self.entry_bg_1 = self.toggle_frame.create_image(
                323.7934875488281,
                126.47222137451172,
                image=self.entryImage_createPost1
            )
            self.entry_1 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_1.place(
                x=188.5869598388672,
                y=109.0,
                width=270.4130554199219,
                height=32.94444274902344
            )

            self.edition_create_postImg = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_3.png")
            self.image_3 = self.toggle_frame.create_image(
                83.0,
                181.0,
                image=self.edition_create_postImg
            )

            self.entryImage_createPost2 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_2.png")
            self.entry_bg_2 = self.toggle_frame.create_image(
                297.1800537109375,
                181.0,
                image=self.entryImage_createPost2
            )
            self.entry_2 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_2.place(
                x=135.36012268066406,
                y=164.0,
                width=323.6398620605469,
                height=32.0
            )

            self.create_post_sizeImg = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_4.png")
            self.image_4 = self.toggle_frame.create_image(
                75.0,
                235.0,
                image=self.create_post_sizeImg
            )

            self.entryImage_createPost3 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_3.png")
            self.entry_bg_3 = self.toggle_frame.create_image(
                297.1800537109375,
                235.0,
                image=self.entryImage_createPost3
            )
            self.entry_3 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_3.place(
                x=135.36012268066406,
                y=218.0,
                width=323.6398620605469,
                height=32.0
            )

            self.estimationD_createpostImg = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_5.png")
            self.image_5 = self.toggle_frame.create_image(
                118.0,
                289.0,
                image=self.estimationD_createpostImg
            )

            self.entryImage_createPost4 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_4.png")
            self.entry_bg_4 = self.toggle_frame.create_image(
                330.33966064453125,
                288.0,
                image=self.entryImage_createPost4
            )
            self.entry_4 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_4.place(
                x=201.67933654785156,
                y=271.0,
                width=257.3206481933594,
                height=32.0
            )

            self.type_create_postImg = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_6.png")
            self.image_6 = self.toggle_frame.create_image(
                80,
                343.0,
                image=self.type_create_postImg
            )

            self.entryImage_createPost5 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_5.png")
            self.entry_bg_5 = self.toggle_frame.create_image(
                297.1800537109375,
                343.0,
                image=self.entryImage_createPost5
            )
            self.entry_5 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_5.place(
                x=135.36012268066406,
                y=326.0,
                width=323.6398620605469,
                height=32.0
            )

            self.progress_createpost_Img = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_7.png")
            self.image_7 = self.toggle_frame.create_image(
                85,
                397.0,
                image=self.progress_createpost_Img
            )

            self.entryImage_createPost6 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_6.png")
            self.entry_bg_6 = self.toggle_frame.create_image(
                297.18006896972656,
                397.0,
                image=self.entryImage_createPost6
            )
            self.entry_6 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_6.place(
                x=135.36013793945312,
                y=380.0,
                width=323.6398620605469,
                height=32.0
            )

            self.extraNotes_createPost_Img = PhotoImage(
                file="images/icons/MainWindow/CreatePost/image_8.png")
            self.image_8 = self.toggle_frame.create_image(
                250.0,
                467.0,
                image=self.extraNotes_createPost_Img
            )

            self.entryImage_createPost7 = PhotoImage(
                file="images/icons/MainWindow/CreatePost/entry_7.png")
            self.entry_bg_7 = self.toggle_frame.create_image(
                253.5,
                559.2307739257812,
                image=self.entryImage_createPost7
            )
            self.entry_7 = Entry(
                bd=0,
                bg="#686666",
                fg="#000716",
                highlightthickness=0
            )
            self.entry_7.place(
                x=48.0,
                y=486.0,
                width=411.0,
                height=144.4615478515625
            )

            self.post_btn_cp = PhotoImage(
                file="images/icons/MainWindow/CreatePost/button_1.png")
            self.button_1 = Button(
                image=self.post_btn_cp,
                borderwidth=0,
                highlightthickness=0,
                command=self.confirm_upload_post,
                relief="flat"
            )
            self.button_1.place(
                x=360.0,
                y=673.0,
                width=126.0,
                height=34.0
            )
            self.button_1.configure(bg="#1E1E1E", activebackground="#1E1E1E",
                                    activeforeground="#1E1E1E", fg="#1E1E1E")

            self.post_uploadImageImg = PhotoImage(file="images/icons/MainWindow/CreatePost/button_2.png")
            self.selected_image_paths = None

            self.button_uploadImg = Button(image=self.post_uploadImageImg,
                                           borderwidth=0,
                                           highlightthickness=0,
                                           command=self.select_and_store_image_paths,
                                           relief="flat")
            self.button_uploadImg.place(
                x=48.0,
                y=669.0,
                width=195.0,
                height=34.0
            )

        else:
            self.destroy_toggle_frame_createPost()

    def select_and_store_image_paths(self):
        self.selected_image_paths = self.select_images()

    def update_posts(self):
        # Initialize old records as None
        old_records = None

        # Retrieve all records initially
        try:
            all_records = Record.retrieve_records()
            all_records.reverse()
        except TypeError:
            all_records = None

        # Show the clear notice if there are no posts initially
        if not all_records:
            self.clear_post_notice(self.scrollable_frame.scrollable_window)

        while True:
            # Retrieve all records
            try:
                new_records = Record.retrieve_records()
                new_records.reverse()
            except TypeError:
                new_records = None

            if old_records != new_records:
                # Clear the scrollable_frame
                for widget in self.scrollable_frame.scrollable_window.winfo_children():
                    widget.destroy()

                if new_records:
                    # Loop through all records
                    for record in new_records:
                        # Create a post for each record
                        self.Main_post(self.scrollable_frame.scrollable_window, record)
                else:
                    # No posts available, call clear_post_notice method
                    self.clear_post_notice(self.scrollable_frame.scrollable_window)

                # Update old records
                old_records = new_records

            # Wait for 1 second before updating again
            time.sleep(5)

    def clear_post_notice(self, parent):
        # Create a frame
        clear_frame = Frame(parent, bg='#000000', width=950, height=300)
        clear_frame.pack(fill=X, padx=10, pady=5)
        clear_frame.pack_propagate(False)

        # Create a canvas
        canvas = Canvas(
            clear_frame,
            bg="#000000",
            height=300,
            width=950,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Place images into the canvas
        image_image_1 = PhotoImage(file="images/icons/MainWindow/PostFrameClear/image_1.png")
        image_1 = canvas.create_image(
            474.0,
            148.0,
            image=image_image_1
        )
        canvas.image1 = image_image_1  # Keep a reference to the image

        image_image_2 = PhotoImage(file="images/icons/MainWindow/PostFrameClear/image_2.png")
        image_2 = canvas.create_image(
            474.0,
            160.0,
            image=image_image_2
        )
        canvas.image2 = image_image_2  # Keep a reference to the image

        return clear_frame

    def Main_post(self, parent, record):

        def truncate_text(text, max_length=35):
            return (text[:max_length - 3] + '...') if len(text) > max_length else text

        post_frame = Frame(parent, bg='#000000', width=950, height=300)
        post_frame.pack(fill=X, padx=10, pady=5)
        post_frame.pack_propagate(False)

        canvas = Canvas(
            post_frame,
            bg="#000000",
            height=300,
            width=950,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        canvas.create_rectangle(867.0, 188.0, 906.0, 208.0, fill="#B65050", outline="")
        canvas.create_rectangle(22.0, 21.0, 668.0, 275.0, fill="#000000", outline="")
        canvas.create_rectangle(691.0, 21.0, 929.0, 275.0, fill="#000000", outline="")
        post_id = record["post_id"]

        button_image_1 = PhotoImage(file="images/icons/MainWindow/Post/button_1.png")
        button_1 = Button(
            canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.confirm_delete_post(self.user, post_id),
            relief="flat"
        )
        button_1.configure(bg="#1E1E1E", activebackground="#1E1E1E", activeforeground="#1E1E1E")
        button_1.place(x=708.0, y=231.0, width=69.0, height=36.0)
        button_1.image = button_image_1  # Keep a reference to the image

        button_image_2 = PhotoImage(file="images/icons/MainWindow/Post/button_2.png")
        button_2 = Button(
            canvas,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.confirm_add_post(post_id),
            relief="flat"
        )
        button_2.place(x=782.0, y=231.0, width=58.0, height=36.0)
        button_2.configure(bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E")
        button_2.image = button_image_2  # Keep a reference to the image

        button_image_3 = PhotoImage(file="images/icons/MainWindow/Post/button_3.png")
        button_3 = Button(
            canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.toggle_postPreview(),
            relief="flat"
        )
        button_3.configure(bg="#1E1E1E", activebackground="#1E1E1E", activeforeground="#1E1E1E")
        button_3.place(x=845.0, y=231.0, width=68.0, height=36.0)
        button_3.image = button_image_3  # Keep a reference to the image

        image_image_1 = PhotoImage(file="images/icons/MainWindow/Post/image_1.png")
        image_1 = canvas.create_image(345.0, 148.0, image=image_image_1)
        canvas.image1 = image_image_1  # Keep a reference to the image

        image_image_2 = PhotoImage(file="images/icons/MainWindow/Post/image_2.png")
        image_2 = canvas.create_image(810.0, 148.0, image=image_image_2)
        canvas.image2 = image_image_2  # Keep a reference to the image

        # Add labels for record data
        Label(canvas, text=truncate_text(record["piece_name"]), bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=140, y=58)
        Label(canvas, text=truncate_text(record["piece_size"]), bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=95, y=103)
        Label(canvas, text=truncate_text(record["piece_edition"]), bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=115, y=149)
        Label(canvas, text=truncate_text(record["piece_type"]), bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=98, y=195)
        Label(canvas, text=truncate_text(str(record["progress"])), bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=485, y=57)
        Label(canvas, text=truncate_text(record["estimation_date"]),
              bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=460, y=130)
        Label(canvas, text=truncate_text(record["addNote"]), bg="#1E1E1E", fg="white",
              font=("Jordan", 12)).place(x=420, y=230)
        Label(canvas, text="Post by: " + truncate_text(self.user.get_user_data_void(record["user_id_token"])["name"]),
              bg="#1E1E1E", fg="white", font=("Jordan", 12)).place(x=70, y=230)

        return post_frame

    def confirm_upload_post(self):
        # Display a confirmation dialog
        if messagebox.askyesno("Confirm upload",
                               "This will upload the post. Do you want to continue?"):
            # Add the post to the follow list if user clicked 'Yes'
            self.create_and_upload_post()
            # Show a success message
            messagebox.showinfo("Post uploaded", "The post has been uploaded successfully!")

    def confirm_add_post(self, post_id):
        # Display a confirmation dialog
        if messagebox.askyesno("Confirm Add",
                               "This will add the post to your follow list. Do you want to continue?"):
            # Add the post to the follow list if user clicked 'Yes'
            self.user.follow_post(post_id)
            # Show a success message
            messagebox.showinfo("Follow List", "The post has been added to follow list successfully!")

    def confirm_delete_post(self, user, post_id):
        # Display a confirmation dialog
        if messagebox.askyesno("Confirm Delete",
                               "This will delete the post permanently and for all users. Do you still want to continue?"):
            Record.delete_record(post_id, user.uid)  # Only delete the post if user clicked 'Yes'

    def toggle_postPreview(self):
        if not self.toggle_frame:
            self.close_button = PhotoImage(file="images/icons/PreviewPost/button_1.png")
            self.Panel = PhotoImage(file="images/icons/PreviewPost/image_1.png")
            self.Panel2 = PhotoImage(file="images/icons/PreviewPost/image_2.png")
            self.text = PhotoImage(file="images/icons/PreviewPost/image_3.png")
            self.text_notes = PhotoImage(file="images/icons/PreviewPost/image_4.png")

            self.toggle_frame = Canvas(
                self,
                bg="#1E1E1E",
                height=500,
                width=800,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )
            self.toggle_frame.place(x=(self.winfo_width() - 800) / 2, y=(self.winfo_height() - 500) / 2)

            button_1 = Button(
                self.toggle_frame,
                image=self.close_button,
                borderwidth=0,
                highlightthickness=0,
                command=self.destroy_toggle_frame,  # change this to the required function
                relief="flat"
            )
            button_1.configure(bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E", fg="#1E1E1E")
            button_1.place(x=733.0, y=14.0, width=40.0, height=26.0)

            image_1 = self.toggle_frame.create_image(
                595.0,
                263.0,
                image=self.Panel
            )

            image_2 = self.toggle_frame.create_image(
                214.0,
                402.0,
                image=self.Panel2
            )

            image_3 = self.toggle_frame.create_image(
                126.0,
                176.0,
                image=self.text
            )

            image_4 = self.toggle_frame.create_image(
                89.0,
                369.0,
                image=self.text_notes
            )

            label1 = Label(self.toggle_frame, text="1", bg="#1E1E1E", fg="#FFFFFF")
            label1.place(x=20, y=20)

            label2 = Label(self.toggle_frame, text="2", bg="#1E1E1E", fg="#FFFFFF")
            label2.place(x=20, y=50)

            label3 = Label(self.toggle_frame, text="3", bg="#1E1E1E", fg="#FFFFFF")
            label3.place(x=20, y=80)

            label4 = Label(self.toggle_frame, text="4", bg="#1E1E1E", fg="#FFFFFF")
            label4.place(x=20, y=110)

            label5 = Label(self.toggle_frame, text="5", bg="#1E1E1E", fg="#FFFFFF")
            label5.place(x=20, y=140)

            label6 = Label(self.toggle_frame, text="6", bg="#1E1E1E", fg="#FFFFFF")
            label6.place(x=20, y=170)

        else:
            self.destroy_toggle_frame()

    def toggle_follow_list(self):
        if not self.toggle_frame:
            self.backButton_Image = PhotoImage(file="images/icons/SettingsWindow/button_2.png")

            self.toggle_frame = Canvas(
                self,
                bg="#1E1E1E",
                height=self.winfo_height(),
                width=500,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )
            self.toggle_frame.place(x=0, y=0)

            back_button = Button(
                self.toggle_frame,
                image=self.backButton_Image,
                borderwidth=0,
                highlightthickness=0,
                command=self.destroy_toggle_frame,
                relief="flat"
            )
            back_button.configure(bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E", fg="#1E1E1E")
            back_button.place(x=450, y=10, width=30.0, height=30.0)

            self.image_background1 = PhotoImage(file="images/icons/FollowListWindow/image_1.png")
            image_1 = self.toggle_frame.create_image(
                217.0,
                372.0,
                image=self.image_background1
            )

            self.image_background2 = PhotoImage(file="images/icons/FollowListWindow/image_2.png")
            image_2 = self.toggle_frame.create_image(
                217.0,
                394.0,
                image=self.image_background2
            )

            # Create a frame inside the canvas for the scrollbar
            scroll_frame = Frame(self.toggle_frame, width=500, height=300)
            scroll_frame.place(x=40, y=90)

            # Create a canvas inside the frame
            scroll_canvas = Canvas(scroll_frame, bg="#1E1E1E")
            scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)

            # Add a scrollbar to the frame, and link it to the scroll_canvas
            scrollbar = ttk.Scrollbar(scroll_frame, orient=VERTICAL, command=scroll_canvas.yview)
            scrollbar.pack(side=RIGHT, fill=Y)

            # Make sure the canvas knows how to react to the scrollbar
            scroll_canvas.configure(yscrollcommand=scrollbar.set)

            # This part makes the view responsive to size changes
            scroll_canvas.bind('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))

            # Create another frame inside the canvas for placing widgets
            content_frame = Frame(scroll_canvas)
            scroll_canvas.create_window((0, 0), window=content_frame, anchor='nw')

            self.update_thread_followList = Thread(target=self.update_scrollbar,
                                                   args=(scroll_canvas,))
            self.update_thread_followList.start()


        else:
            self.destroy_toggle_frame()

    def update_scrollbar(self, scroll_canvas):
        old_follow_list = None

        while True:
            # Check if scroll_canvas still exists
            if scroll_canvas.winfo_exists():
                try:
                    new_follow_list = self.user.retrieve_follow_list()
                except TypeError:
                    new_follow_list = None

                if old_follow_list is None and not new_follow_list:
                    self.follow_list_preview(scroll_canvas, None)

                elif old_follow_list != new_follow_list:
                    # Clear the scrollable_frame
                    for widget in scroll_canvas.winfo_children():
                        widget.destroy()

                    if new_follow_list:
                        # Loop through the follow list
                        for follow_item in new_follow_list:
                            # Create a follow list preview for each item
                            self.follow_list_preview(scroll_canvas, follow_item)

                    # Update old follow list
                    old_follow_list = new_follow_list

            else:
                # If scroll_canvas doesn't exist, break the loop
                break

            # Wait for 2 seconds before updating again
            time.sleep(2)

    def toggle_settings(self):
        if not self.toggle_frame:
            self.backButton_Image = PhotoImage(file="images/icons/SettingsWindow/button_2.png")
            self.logoutButton_Image = PhotoImage(file="images/icons/MainWindow/button_2.png")
            self.entry_image_1 = PhotoImage(file="images/icons/SettingsWindow/entry_1.png")
            self.submitButton_Image = PhotoImage(file="images/icons/SettingsWindow/button_4.png")
            self.uploadButton_Image = PhotoImage(file="images/icons/SettingsWindow/button_3.png")

            self.toggle_frame = Frame(self, bg="#1E1E1E")
            self.toggle_frame.place(x=0, y=0, height=self.winfo_height(), width=500)

            # Back Button
            back_button = Button(self.toggle_frame, image=self.backButton_Image, bg="#1E1E1E",
                                 activeforeground="#1E1E1E", activebackground="#1E1E1E", bd=0,
                                 command=self.destroy_toggle_frame)
            back_button.place(x=450, y=10)

            # Logout Button
            logout_button = Button(self.toggle_frame, image=self.logoutButton_Image, bg="#1E1E1E",
                                   activeforeground="#1E1E1E", activebackground="#1E1E1E", bd=0,
                                   command=self.sign_out)
            logout_button.place(x=self.relative_location_MainWindow((400, self.winfo_height() - 100))[0] + 100,
                                y=self.relative_location_MainWindow((400, self.winfo_height()))[1] + 150,
                                width=int(152.0 * self.scale_x), height=int(57.0 * self.scale_y))

            # Text
            Label(self.toggle_frame, text="Change User name:", bg="#1E1E1E", fg="#FFFFFF",
                  font=("JostRoman Regular", 12)).place(x=53, y=245)

            # Entry field image
            Label(self.toggle_frame, image=self.entry_image_1, bg="#1E1E1E").place(x=213, y=239)

            # Entry field
            self.entry_1 = Entry(self.toggle_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
            self.entry_1.place(x=226.0, y=245.0, width=162.0, height=30.0)

            submit_button = Button(self.toggle_frame, image=self.submitButton_Image, bg="#1E1E1E",
                                   activeforeground="#1E1E1E", activebackground="#1E1E1E", bd=0,
                                   command=self.submit_command)
            submit_button.place(x=250, y=290)  # adjust these values as needed

            self.user_image_label = Label(self.toggle_frame, image=self.image_image_5, bg="#1E1E1E")

            self.user_image_label.place(x=50, y=50)

            upload_button = Button(self.toggle_frame, image=self.uploadButton_Image, bg="#1E1E1E",
                                   activeforeground="#1E1E1E", activebackground="#1E1E1E", bd=0,
                                   command=self.upload_image)
            upload_button.place(x=50, y=110)

            user_name_label = Label(self.toggle_frame, text=f"User's Name: {self.user.name}",
                                    bg="#1E1E1E", fg="#FFFFFF", font=("JostRoman Regular", 12))
            user_name_label.place(x=200, y=50)  # adjust these values as needed

            user_stand_label = Label(self.toggle_frame, text=f"User's Stand: {self.user.process_stand}",
                                     bg="#1E1E1E", fg="#FFFFFF", font=("JostRoman Regular", 12))
            user_stand_label.place(x=200, y=90)  # adjust these values as needed

        else:
            self.destroy_toggle_frame()

    def submit_command(self):
        # Call change_user_name and get the result
        result = self.user.change_user_name(self.entry_1.get())
        # Show a pop-up window with the result
        messagebox.showinfo("Name Change Result", result)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            # Upload the image to Firebase
            upload_result = self.user.upload_image_DB(file_path)
            if upload_result is not None:
                messagebox.showinfo("Image Upload Result", upload_result)

            # Reload the image from Firebase to ensure it's the same as the one just uploaded
            download_path = file_path + "_downloaded"  # or another path where you want to save the downloaded image
            download_result = self.user.download_image_DB(download_path)
            if download_result is not None:
                messagebox.showinfo("Image Download Result", download_result)

            # Display the downloaded image in the UI
            new_image = ImageTk.PhotoImage(Image.open(download_path).resize((55, 55)))
            self.image_image_5 = new_image
            self.user_image_label.config(image=new_image)
            self.user_image_label.image = new_image
            self.canvas.itemconfigure(self.image_5, image=new_image)

    def update_username(self):
        new_name = self.entry_1.get()

        # Call change_user_name and get the result
        result = self.user.change_user_name(new_name)

        # Show a pop-up window with the result
        messagebox.showinfo("Name Change Result", result)

        if "Successfully changed the user's name" in result:
            # Only update the name in the UI if the name was successfully changed in Firebase
            self.canvas.itemconfigure(self.username_label, text=self.user.get_user_data()['name'])

    def destroy_toggle_frame(self):
        if self.toggle_frame and self.create_post_active:
            self.destroy_toggle_frame_createPost()
        else:
            self.toggle_frame.destroy()
            self.toggle_frame = None

    def relative_location_MainWindow(self, objective_position: tuple):
        original_size = (1920, 1080)  # Original design size
        original_width, original_height = original_size
        objective_x, objective_y = objective_position

        relative_x = int((objective_x / original_width) * self.screen_width)
        relative_y = int((objective_y / original_height) * self.screen_height)

        return relative_x, relative_y

    def scale_image(self, image_path):
        # Open an image file
        with Image.open(image_path) as img:
            # Resize it
            img = img.resize((int(img.width * self.scale_x), int(img.height * self.scale_y)), Image.ANTIALIAS)
            # Return a PhotoImage object
            return ImageTk.PhotoImage(img)

    def sign_out(self):
        self.stop_event.set()  # Stops the thread
        self.destroy()
        LoginWindow().mainloop()
