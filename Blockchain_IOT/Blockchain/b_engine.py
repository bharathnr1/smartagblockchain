from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, crop_info, timestamp, previous_hash, nonce = 0 ):
        self.index = index
        self.crop_info = crop_info
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
        #json.dumps() takes an object and produces a string
        #self.__dict__ has all the object attributes
        #encode converts json formatted string to a UTF-8 string readable by hashlib
        #hashlib’s output is a byte hash - hexdigest converts from bytes to hex


class Blockchain:
    difficulty = 2

    def __init__(self):
        self.unconfirmed_crop_info = []
        self.chain = []

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        # print(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        print(self.chain)
        print("Entered add_block and appended this new block to the blockchain")
        return True

    def proof_of_work(self, block):
        block.nonce = 0
        print("Entered POW and calculated compute hash for the new block")
        compute_hash = block.compute_hash()
        while not compute_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            compute_hash = block.compute_hash()

        return compute_hash

    def add_new_crop_info(self, crop_info):
        print("Entered add_new_crop and appended crop details")
        self.unconfirmed_crop_info.append(crop_info)


    @classmethod
    def is_valid_proof(cls, block, block_hash):
        if block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash():
            return True

    #@classmethod
    #def check_chain_validity

    def mine(self):
        print("Entered mine function...")
        if not self.unconfirmed_crop_info:
            return False

        last_block = self.last_block

        new_block = Block(index = last_block.index + 1,
                          crop_info = self.unconfirmed_crop_info,
                          timestamp= time.time(),
                          previous_hash = last_block.hash)
        print("Created a Block...")
        proof = self.proof_of_work(new_block) #POW returns computed hash
        self.add_block(new_block, proof)

        self.unconfirmed_crop_info = []
        print("Reset unconfirmed crops to blank and returned the newly added block")
        # return new_block.index
        print(new_block)
        return new_block


def new_transaction():
    #tx_plant_info = request.get_json() #when we have the API info ready
    print("Entered the New transaction function and called add_new_crop func...")
    tx_plant_info =  ['Bharath',
                        'Tomato',
                        'Solanum lycopersicum',
                        '12.97194,77.59369',
                        '20',
                        '20' ]
    # Farmer who grew this crop:
    # Name of the crop:
    # Species / Scientific Name:
    # Geo-location of where the crop was grown:
    # Age of the Crop:
    # Height of the Plant:
    # Health of the Crop:
    blockchain.add_new_crop_info(tx_plant_info)

    return "Success", 201


def get_chain():
    chain_data = []
    print(len(blockchain.chain))
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    print( json.dumps({"length" : len(chain_data),
                        "chain" : chain_data }) )


def mine_unconfirmed_plant_info():
    result = blockchain.mine()
    if not result:
        return "No new transactions to mine"
    return "Block #{} is mined".format(result)



blockchain = Blockchain()
blockchain.create_genesis_block()


# get_chain()
#
# block1 = new_transaction()
# block2 = new_transaction()
# if block1:
#     r1 = blockchain.mine()
#     if r1:
#         print( "Added block1" )
#     else:
#         print("Block1 not added")

# if block2:
#     r2 = blockchain.mine()
#     if r2:
#         print( "Added block2" )
#     else:
#         print("Block2 not added")
# print(mine_unconfirmed_plant_info())

# get_chain()
