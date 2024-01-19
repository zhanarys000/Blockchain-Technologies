import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

class DigitalSignatureManager:
    def __init__(self):
        # Generate a new key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign_file(self, file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        
        signature = base64.b64encode(self.private_key.sign(
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        )

        encrypted_folder = "encrypted"
        encrypted_file_name = f"encrypted_{os.path.basename(file_path)}.signature"
        encrypted_file_path = os.path.join(encrypted_folder, encrypted_file_name)
        with open(f'{encrypted_file_path}', "wb") as signature_file:
            signature_file.write(signature)
        

    def verify_signature(self, file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()

        with open(f"{file_path}.signature", "rb") as signature_file:
            signature = base64.b64decode(signature_file.read())

        print(f"{file_path}.signature")
        try:
            self.public_key.verify(
                signature,
                file_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Signature verification successful. The file is authentic.")
        except InvalidSignature:
            print("Signature verification failed. The file is not authentic.")
            return False
        except Exception as e:
            print(f"Signature verification failed. The file may be tampered with. Error: {e}")

