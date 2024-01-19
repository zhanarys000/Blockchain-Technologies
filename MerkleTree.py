import hashlib
import json

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_merkle_tree()

    def build_merkle_tree(self):
        if not self.transactions:
            return None

        merkle_tree = [self.hash_transaction(tx) for tx in self.transactions]

        while len(merkle_tree) > 1:
            merkle_tree = self._build_next_level(merkle_tree)

        return merkle_tree[0]

    def hash_transaction(self, transaction):
        transaction_data = json.dumps(transaction, sort_keys=True)
        return hashlib.sha256(transaction_data.encode()).hexdigest()

    def _build_next_level(self, prev_level):
        next_level = []

        for i in range(0, len(prev_level), 2):
            left_child = prev_level[i]
            right_child = prev_level[i + 1] if i + 1 < len(prev_level) else left_child

            parent_hash = hashlib.sha256((left_child + right_child).encode()).hexdigest()
            next_level.append(parent_hash)

        return next_level

    def get_root(self):
        return self.root
