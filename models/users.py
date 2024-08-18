from firebase_admin.auth import UserRecord


class User:
    def __init__(self, user_record: UserRecord):
        self.user_record = user_record

    def get_dict(self):
        return {
            "uid": self.user_record.uid,
            "displayName": self.user_record.display_name,
            "email": self.user_record.email,
            "emailVerified": self.user_record.email_verified,
            "photo": self.user_record.photo_url,
            "mobile": self.user_record.phone_number,

        }