import os
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

class FileEncryptor:
    def __init__(self, key=None):
        if key is None:
            self.key = self.generate_key()
        else:
            self.key = key

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    def save_key_to_file(self, filename="secret.key"):
        with open(f'encrypted/{filename}', "wb") as key_file:
            key_file.write(self.key)

    @classmethod
    def load_key_from_file(cls, filename="secret.key"):
        with open(f'{filename}', "rb") as key_file:
            return key_file.read()

    def encrypt_file(self, file_path):
        cipher = Fernet(self.key)
        with open(file_path, "rb") as file:
            file_data = file.read()
            encrypted_data = cipher.encrypt(file_data)

        encrypted_folder = "encrypted"
        encrypted_file_name = f"encrypted_{os.path.basename(file_path)}"

        os.makedirs(encrypted_folder, exist_ok=True)

        encrypted_file_path = os.path.join(encrypted_folder, encrypted_file_name)

        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        self.save_key_to_file(filename=f'{encrypted_file_name}.key')

    def _sanitize_file_name(self, file_path):
        return "".join(c if c.isalnum() or c in ('_', '.') else '_' for c in os.path.basename(file_path))

    def decrypt_file(self, encrypted_file_path):
        try:
            with open(encrypted_file_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()

            cipher = Fernet(self.load_key_from_file(filename=f'{encrypted_file_path}.key'))
            decrypted_data = cipher.decrypt(encrypted_data)

            decrypted_file_path = f"decrypted_{os.path.basename(encrypted_file_path)}"
            with open(f'decrypted/{decrypted_file_path}', "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)

            print("Decryption successful.")
        except InvalidToken:
            print("Error: Signature verification failed. The file may be tampered with.")
        except Exception as e:
            print(f"Error during decryption: {e}")
