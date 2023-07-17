import tkinter as tk

root = tk.Tk()
root.geometry("300x500")
root.title("Test Settings tab")

head_frame = tk.Frame(root, bg="#1E1E1E", highlightbackground="white", highlightthickness=1)


def toggle_settings():
    if not hasattr(toggle_settings, 'toggle_frame'):
        toggle_settings.toggle_frame = tk.Frame(root, bg="#1E1E1E")
        toggle_settings.toggle_frame.place(x=0, y=0,
                                           height=root.winfo_height(),
                                           width=200)

        back_button = tk.Button(toggle_settings.toggle_frame, image=backButton_Image, bg="#1E1E1E",
                                activeforeground="#1E1E1E",
                                activebackground="#1E1E1E",
                                bd=0,
                                command=toggle_settings.toggle_frame.destroy)
        back_button.place(x=150, y=10)
    else:
        toggle_settings.toggle_frame.destroy()
        delattr(toggle_settings, 'toggle_frame')


image1 = tk.PhotoImage(file="images/icons/SettingsWindow/image_4.png")
toogle_settings_button = tk.Button(head_frame,
                                   image=image1,
                                   bg="#1E1E1E", activeforeground="#1E1E1E", activebackground="#1E1E1E"
                                   , bd=0,
                                   command=toggle_settings)

toogle_settings_button.image = image1  # Keep a reference to the image

toogle_settings_button.pack(side=tk.LEFT)

head_frame.pack(side=tk.TOP, fill=tk.X)

head_frame.pack_propagate(False)
head_frame.configure(height=50)

backButton_Image = tk.PhotoImage(file="images/icons/SettingsWindow/button_2.png")  # Keep a reference to the image

root.mainloop()
