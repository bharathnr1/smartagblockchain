from django.shortcuts import render, redirect
from hashlib import sha256
import json
import time, datetime
from .forms import add_crop_details
from .models import Crop_info
# Create your views here.


def home(request):
    return render(request, "home.html")


def initiate(request):
    times = []
    genesis_block = ''
    if(request.method =="POST"):
        if not len(blockchain.chain):
            blockchain.create_genesis_block()
            print("Initiated the blockchain")

        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)

        genesis_block = chain_data
        # genesis_block = json.dumps({"length" : len(chain_data),
        #                      "chain" : chain_data })
        # print( json.dumps({"length" : len(chain_data),
        #                     "chain" : chain_data }),)
    return render(request, "initiate.html", {'genesis_block': genesis_block})

def block_add(request):
    form = add_crop_details()
    if(request.method == "POST"):
        # form = add_crop_details(request.POST)
        tx_crop_info = add_crop_details(data=request.POST)
        if tx_crop_info.is_valid():
            x = tx_crop_info.save()
        print("Inside block_add")
        y = []
        y.append(str(x.farmer))
        y.append(str(x.crop_name))
        y.append(str(x.crop_species))
        # y.append(str(x.geolocation_lat))
        # y.append(str(x.geolocation_lon))
        y.append(str(x.crop_age))
        y.append(str(x.crop_height))
        print(y)
        blockchain.add_new_crop_info(y)
        print("Mining")
        blockchain.mine()
        return redirect('view_blockchain')
    return render(request, 'block_add.html',{'form': form})


def view_blockchain(request):
    blocks = "No blocks created yet! Initiate the blockchain and start adding blocks..."
    if(request.method =="GET"):
        if not len(blockchain.chain):
            blocks = "No blocks created yet! Initiate the blockchain and start adding blocks...Inside method"
        stages = ['Null','Seed', 'Sapling','Plant','Flower Stage','Fruit Development','Fruit Ripening']
        chain_data = []
        print(stages)
        print((blockchain.chain))
        for block in blockchain.chain:
            chain_data.append(block.__dict__)

        # geolocation = append('https://www.google.com/maps/@',)
        context = zip(chain_data, stages)
        # blocks = json.dumps({"length" : len(chain_data),
        #                     "chain" : chain_data })
        # parsed = json.loads(blocks)
        # #parsed is in python dictionary - we can change the way it looks from here
        # chain = parsed['chain']

    return render(request, 'view_blockchain.html', {'context' : context })


def particles(request):
    sensor_data = ['0','0','0','0','0','0']
    context = ""
    clicked = ""

    if(request.POST.get('seedbtn')):
        print("seedbtn clicked")
        sensor_data = ['0-12 Days', '24', '33', '14', '1', '7' ]
        context =  sensor_data
        clicked = 'seedclick'
        print(context)
        return render(request, "particles.html", {'context': context, 'clicked': clicked, })

    elif(request.POST.get('saplingsbtn')):
        print("saplingsbtn clicked")
        sensor_data = ['12-24 Days', '24', '33', '14', '2', '7' ]
        context =  sensor_data
        clicked = 'saplingsclick'
        print(context)
        return render(request, "particles.html", {'context': context, 'clicked': clicked })

    elif(request.POST.get('plantbtn')):
        print("plantbtn clicked")
        sensor_data = ['24-36 Days', '22', '33', '15', '4', '7' ]
        context =  sensor_data
        clicked = 'plantclick'
        print(context)
        return render(request, "particles.html", {'context': context, 'clicked': clicked })

    elif(request.POST.get('flowerbtn')):
        print("flowerbtn clicked")
        sensor_data = ['36-48 Days', '25', '33', '16', '4', '7' ]
        context =  sensor_data
        clicked = 'flowerclick'
        print(context)
        return render(request, "particles.html", {'context': context, 'clicked': clicked })

    elif(request.POST.get('fruitbtn')):
        print("fruitbtn clicked")
        sensor_data = ['48-60 Days', '22', '34', '18', '5', '7' ]
        context =  sensor_data
        clicked = 'fruitclick'
        print(context)
        return render(request, "particles.html", {'context': context, 'clicked': clicked })

    elif(request.POST.get('harvestbtn')):
        print("harvestbtn clicked")
        sensor_data = ['60-100 Days', '22', '34', '18', '6', '7' ]
        context =  sensor_data
        clicked = 'harvestclick'
        print(context)
        return render(request, "particles.html", {'context': context, 'clicked': clicked })

    else:
        print("seedbtn not clicked")

    return render(request, "particles.html")


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
        #put x eqaul to the outpitand add x to genesis_block and see datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        x = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        genesis_block = Block(0, [], x, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        # print(genesis_block)

    @property
    def last_block(self):
        print("Last block1")
        print(self.chain)
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

        print(self.last_block)
        print(type(self.last_block))
        last_block = self.last_block

        new_block = Block(index = last_block.index + 1,
                          crop_info = self.unconfirmed_crop_info,
                          timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                          previous_hash = last_block.hash)
        print("Created a Block...")
        proof = self.proof_of_work(new_block) #POW returns computed hash
        self.add_block(new_block, proof)

        self.unconfirmed_crop_info = []
        print("Reset unconfirmed crops to blank and returned the newly added block")
        # return new_block.index
        print(new_block)
        return new_block

blockchain = Blockchain()

def new_transaction():
    #tx_plant_info = request.get_json() #when we have the API info ready
    # tx_plant_info = #form
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
