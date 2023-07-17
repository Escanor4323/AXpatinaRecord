"""
Programed by: Joel Martinez
Py ver: Python 3.10.6
"""
import win32com.client as win32
from GUI import LoginWindow
import tkinter as tk
import time
from tkinter import ttk


def send_email_via_outlook(subject, body, recipient):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.Body = body

    # Check if recipient is a list and has more than one recipient
    if isinstance(recipient, list) and len(recipient) > 1:
        mail.To = "; ".join(recipient)  # join all recipients into a single string with ';' separator
    else:
        # If recipient is a list but only contains one email, select that email
        if isinstance(recipient, str):
            recipient = recipient
        mail.To = recipient

    mail.Send()


if __name__ == '__main__':
    # send_email_via_outlook(subject="Notification", body="This is a test message for email",
    # recipient="mjoel4318@gmail.com")
    # LoginWindow().mainloop()

    print("Initial")

