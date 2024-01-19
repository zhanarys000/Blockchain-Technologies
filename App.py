import os
import tkinter as tk
from tkinter import filedialog
from DigitalSignature import DigitalSignatureManager
from File import FileEncryptor
from Block import Blockchain, Block, Transaction

class FileStorageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Storage System")

        self.file_encryptor = FileEncryptor()
        self.signature_manager = DigitalSignatureManager()
        self.blockchain = Blockchain()

        self.upload_button = tk.Button(self.master, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.download_button = tk.Button(self.master, text="Download File", command=self.download_file)
        self.download_button.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to upload")
        if file_path:
            self.file_encryptor.encrypt_file(file_path)
            self.signature_manager.sign_file(file_path)

            transaction = Transaction(file_path, "sender", "recipient")

            new_block = Block(len(self.blockchain.chain), transaction.timestamp, [transaction.to_dict()], self.blockchain.get_latest_block().hash)
            self.blockchain.add_block(new_block)

            tk.messagebox.showinfo("Upload Complete", "File uploaded successfully!")


    def download_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to download")
        print(file_path)
        if file_path:
            self.file_encryptor.decrypt_file(file_path)

            tk.messagebox.showinfo("Download Complete", "File downloaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileStorageApp(root)
    root.mainloop()
