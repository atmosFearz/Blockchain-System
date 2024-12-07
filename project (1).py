import hashlib
import json
from time import time
import uuid
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(previous_hash='0', proof=100)

    def create_block(self, proof, previous_hash=None):
      
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else None
        }
        
        self.pending_transactions = []
        
        self.chain.append(block)
        return block

    def create_transaction(self, sender, recipient, amount):
      
        transaction = {
            'id': str(uuid.uuid4()),
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
       
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof

    def valid_proof(self, last_proof, proof):
    
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    @staticmethod
    def hash(block):
    
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
     
        return self.chain[-1]

    def is_chain_valid(self):
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
         
            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                return False
        
        return True

class BlockchainNode:
    def __init__(self):
        self.blockchain = Blockchain()
        self.node_id = str(uuid.uuid4())

    def mine_block(self):
        """
        Mine a new block in the blockchain
        """
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        
        
        proof = self.blockchain.proof_of_work(last_proof)
        
        
        self.blockchain.create_transaction(
            sender="0", 
            recipient=self.node_id,
            amount=1
        )
        
        
        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.create_block(proof, previous_hash)
        
        return block

    def add_transaction(self, sender, recipient, amount):
        return self.blockchain.create_transaction(sender, recipient, amount)

