from web3 import Web3
from solcx import compile_standard
from solcx import set_solc_version
import time
import json
import os
from dotenv import load_dotenv
set_solc_version("0.6.0") #setting the solc version to 0.6.0
load_dotenv() #load the .env file

with open("./logs.sol") as file:
    log_file=file.read()

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
'''with open("compiled_logs.json","w") as file:
    json.dump(compiled_sol,file)'''
abi=compiled_sol["contracts"]["logs.sol"]["logs"]["abi"]
bytecode=compiled_sol["contracts"]["logs.sol"]["logs"]["evm"]["bytecode"]["object"]

provider=Web3.HTTPProvider("HTTP://127.0.0.1:8545")
w3=Web3(provider)
chain_id=1337
my_address="0x868FCc0ee2530fc980c8DAC1142a42D5D7155176"
private_key=os.getenv("PRIVATE_KEY")
logs=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce=w3.eth.get_transaction_count(my_address,"pending")

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
time.sleep(1)
current_nonce=w3.eth.get_transaction_count(my_address,'pending')
def store_log(message):
    global current_nonce
    transaction=logs.functions.addlog(message).build_transaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce+1,
            "gasPrice":w3.to_wei('50','gwei'),
            "gas":3000000,
        }    
    )
store_log("Test log from AI Agent")
signed_txn=w3.eth.account.sign_transaction(transaction,private_key=private_key)
txn_hash=w3.eth.send_raw_transaction(signed_txn.raw_transaction)
txn_recipt=w3.eth.wait_for_transaction_receipt(txn_hash)
print("Log Stored")
current_nonce+=1
#create Log filter
log_filter=w3.eth.filter({
    "fromBlock":"latest",
    "address":my_address,
    "topics":[logs.events.Logadded().signature]
})

while True:
    new_events=log_filter.get_new_entries()
    if new_events:
        for events in new_events:
            print("New Log Added",events.args.log,"from",events.args.sender)
    time.sleep(1)      
