from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
print(f"Your encryption key: {key.decode()}")
print("\nAdd this to your .env file:")
print(f"ENCRYPTION_KEY={key.decode()}")