__all__ = (
    "keygen",
    "encrypt_secret",
    "decrypt_secret",
)

import os
from cryptography.fernet import Fernet

def keygen() -> str:
    """
    Generate a Fernet key
    """
    return Fernet.generate_key().decode()


def encrypt_secret(secret: str, key: str = None) -> str:
    """Encrypt a secret with a Fernet key string."""
    if key is None:
        key = os.environ["RAY_ENCRYPT_KEY"]
    f = Fernet(key)
    return f.encrypt(secret.encode()).decode()


def decrypt_secret(secret: str, key: str = None) -> str:
    """Decrypt a secret using a Fernet key string."""
    if key is None:
        key = os.environ["RAY_DECRYPT_KEY"]
    f = Fernet(key)
    return f.decrypt(secret).decode()