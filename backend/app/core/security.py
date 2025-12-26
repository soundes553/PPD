from cryptography.fernet import Fernet
import json
import os

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not found in .env file!")

cipher = Fernet(ENCRYPTION_KEY.encode())


def encrypt_prediction(prediction_data: dict) -> str:
    """
    Encrypts a prediction dictionary and returns encrypted string
    """
    json_str = json.dumps(prediction_data)
    encrypted_bytes = cipher.encrypt(json_str.encode())
    return encrypted_bytes.decode()


def decrypt_prediction(encrypted_data: str) -> dict:
    """
    Decrypts an encrypted prediction string back to dictionary
    """
    decrypted_bytes = cipher.decrypt(encrypted_data.encode())
    json_str = decrypted_bytes.decode()
    prediction_data = json.loads(json_str)
    return prediction_data