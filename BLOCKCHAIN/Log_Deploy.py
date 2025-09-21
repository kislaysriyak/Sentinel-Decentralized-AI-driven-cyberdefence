from web3 import Web3 # to interact with the blockchain
from solcx import compile_standard # To setup the solidity compiler
from solcx import set_solc_version # Definig the solc version
import os # to read environment variables
from dotenv import load_dotenv # to load environment variables from .env file
set_solc_version("0.6.0") #setting the solc version to 0.6.0
load_dotenv() #load the .env file

recipt_queue=[]  #queue to store transaction recipt
#importing the contract file
with open("./logs.sol") as file:
    log_file=file.read()

# ===================================================================
# Setting Up Blockchain
# ===================================================================
compiled_sol=compile_standard(
    {


     "language":"Solidity",
        "sources":{"logs.sol":{"content": log_file}},
        "settings":{
         "outputSelection":{
                "*":{
                    "*":["abi","metadata","evm.bytecode","evm.sourceMap"]
                }
            }
        }
    }    
)
solc_version="0.6.0",
abi=compiled_sol["contracts"]["logs.sol"]["logs"]["abi"]
bytecode=compiled_sol["contracts"]["logs.sol"]["logs"]["evm"]["bytecode"]["object"]

provider=Web3.HTTPProvider("HTTP://127.0.0.1:8545")
w3=Web3(provider)
chain_id=1337
my_address="0x868FCc0ee2530fc980c8DAC1142a42D5D7155176" # Have to change this and PVT key to connect new Blockchain
private_key=os.getenv("PRIVATE_KEY")
logs=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce=w3.eth.get_transaction_count(my_address,"pending")

# ==========================================================================
# Creating Contract in BlockChain
# ==========================================================================

transaction=logs.constructor().build_transaction(
    {
        "chainId":chain_id,
        "nonce":nonce,
        "from":my_address,
        "gasPrice":w3.to_wei('20','gwei'),
        "gas":3000000
    }
)
signed_tx=w3.eth.account.sign_transaction(transaction,private_key=private_key)
tx_hash=w3.eth.send_raw_transaction(signed_tx.raw_transaction)
tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address=tx_recipt.contractAddress
logs=w3.eth.contract(address=contract_address,abi=abi)
current_nonce=w3.eth.get_transaction_count(my_address,'pending')

# ========================================================================
# Function for Detection Agent To store Attack type and Location of Attack
# =========================================================================


def store_log(attack_type, ip_address="", mac_address=""):
    
    global current_nonce,recipt_queue
    transaction=logs.functions.addlog(attack_type,ip_address,mac_address).build_transaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": current_nonce,
            "gasPrice":w3.to_wei('50','gwei'),
            "gas":3000000,
        }    
    )
    signed_txn=w3.eth.account.sign_transaction(transaction,private_key=private_key)
    txn_hash=w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    txn_recipt=w3.eth.wait_for_transaction_receipt(txn_hash)
    print("Log Stored")
    recipt_queue.append(txn_recipt)
    current_nonce+=1
    return txn_recipt

# ========================================================================
# Function for Analysis Agent To read New Logs from Blockchain
# =========================================================================

def read_new_logs():
    log_list=[]
    global recipt_queue
    while recipt_queue:
        recipt=recipt_queue.pop(0)
        log_entries=logs.events.Logadded().process_receipt(recipt)
        for entries in log_entries:
            log_list.append
            (
                (
                    entries.agrs.attackType,
                    entries.args.ipAddress,
                    entries.args.macAddress,
                    entries.args.sender
                )
            )

    return log_list
