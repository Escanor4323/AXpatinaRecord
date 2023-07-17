import firebase_admin
from firebase_admin import auth


def authenticate_email(email):
    try:
        user = auth.get_user_by_email(email)
        auth.set_custom_user_claims(user.uid, {"authenticated": True})
        print("Email authenticated successfully.")
    except Exception as e:
        print("Authentication error:", e)
