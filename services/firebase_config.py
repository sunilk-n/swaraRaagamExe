import os


def get_firebase_config():
    return {
      "type": os.getenv("FB_TYPE"),
      "project_id": os.getenv("FB_PROJECT_ID"),
      "private_key_id": os.getenv("FB_PRIVATE_KEY_ID"),
      "private_key": os.getenv("FB_PRIVATE_KEY").replace(r'\n', '\n'),
      "client_email": os.getenv("FB_CLIENT_EMAIL"),
      "client_id": os.getenv("FB_CLIENT_ID"),
      "auth_uri": os.getenv("FB_AUTH_URI"),
      "token_uri": os.getenv("FB_TOKEN_URI"),
      "auth_provider_x509_cert_url": os.getenv("FB_AUTH_PROVIDER"),
      "client_x509_cert_url": os.getenv("FB_CLIENT"),
      "universe_domain": os.getenv("FB_UNIVERSAL_DOMAIN")
    }
