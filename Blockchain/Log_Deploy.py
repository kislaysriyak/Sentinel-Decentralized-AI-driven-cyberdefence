from web3 import Web3
from solcx import compile_standard
from solcx import set_solc_version
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
                    "*":["abi","metadata","bytecode","evm.sourceMap"]
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

provider=Web3.HTTPProvider("HTTP://127.0.0.1:7545")
w3=Web3(provider)
chain_id=1337
my_address=
private_key=os.getenv("PRIVATE_KEY")
logs=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce=w3.eth.get_transaction_count(my_address)


transaction=logs.constructor().build_transaction(
    {
        "chainId":chain_id,
        "nonce":nonce,
        "from":my_address,
    }
)

def store_log(message):
    transaction=logs.functions.addlog(message).build_transaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce+1,
        }    
    )

signed_txn=w3.eth.account.sign_transaction(transaction,private_key=private_key)
txn_hash=w3.eth.send_raw_transaction(signed_txn.raw_transaction)
txn_recipt=w3.eth.wait_for_transaction_receipt(txn_hash)
print("Log Stored")

store_log("Test log from AI Agent")
