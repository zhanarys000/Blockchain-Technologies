import hashlib
import json
import time
from MerkleTree import MerkleTree

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.transactions = []
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.merkle_root = None 
        self.hash = self.calculate_hash()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.merkle_root = self.calculate_merkle_root()
        return self.calculate_hash()

    def calculate_merkle_root(self):
        if not self.transactions:
            return None
        merkle_tree = MerkleTree([tx.to_dict() for tx in self.transactions])
        return merkle_tree.get_root()

    def calculate_hash(self):
        hash_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'transactions': [tx.to_dict() for tx in self.transactions]
        }, sort_keys=True)
        return hashlib.sha256(hash_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]


    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

class Transaction:
    def __init__(self, file_name, sender, recipient):
        self.file_name = file_name
        self.sender = sender
        self.recipient = recipient
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'file_name': self.file_name,
            'sender': self.sender,
            'recipient': self.recipient,
            'timestamp': self.timestamp,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), default=lambda o: o.__dict__, sort_keys=True)

