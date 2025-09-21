from solcx import compile_standard #compile solidity from JSON interface
import json
from dotenv import load_dotenv
load_dotenv() #load the .env file
from solcx import set_solc_version
set_solc_version("0.6.0") #setting the solc version to 0.6.0
from web3 import Web3   #to interact with the blockchain
import os

with open("./Start.sol","r") as file: #Inputing our solidity program in a file as read only
    start_file=file.read()
#print(start_file)

compiled_sol=compile_standard(
    {
        "language": "Solidity",#Tells the compiler what language you are compiling
        "sources":{"Start.sol":{"content": start_file}},
        "settings":{
            "outputSelection":{ #pecifies output per file and contract.
                "*":{ #First "*" → means apply to all source files.
                      #Second "*" → means apply to all contracts inside those files.
                    "*":["abi","metadata","evm.bytecode","evm.sourceMap"]
                }
            }#The list tells solc which outputs you want:
            #"abi" → Application Binary Interface (needed for interacting with the contract).
            #"metadata" → metadata about the contract (compiler version, etc.).
            #"evm.bytecode" → compiled contract bytecode (used when deploying).
            #"evm.sourceMap" → mapping from bytecode to source code lines (useful for debugging).'''
        },
    },   
)
solc_version="0.6.0", #specifies the solc version to use for compilation
#with open("compiled_code.json","w") as file: #writing the compiled code to a json file
#     json.dump(compiled_sol,file)

# get bytecode
bytecode=compiled_sol["contracts"]["Start.sol"]["Start"]["evm"]["bytecode"]["object"]
# above used to get the bytecode of the contract using the path in the compiled_sol dictionary whose structure is stored in compiled_code.json file
# get abi
abi=compiled_sol["contracts"]["Start.sol"]["Start"]["abi"]
# above used to get the abi of the contract using the path in the compiled_sol dictionary whose structure is stored in compiled_code.json file

#for connecting to ganache
provider=Web3.HTTPProvider("HTTP://127.0.0.1:8545") #connecting to the local ganache blockchain #(In Older versions of web3 use Web3.web3.HTTPProvider)
w3=Web3(provider)
chain_id=1337 #chain id or Network id of ganache
my_address="0x868FCc0ee2530fc980c8DAC1142a42D5D7155176" #your metamask account address
private_key=os.getenv("PRIVATE_KEY") #private key of your metamask account
#private_key="your private key"
print("Connected",w3.is_connected())# check the status of connection
#Create the contract in python
Start= w3.eth.contract(abi=abi,bytecode=bytecode)
nonce=w3.eth.get_transaction_count(my_address) #get the nounce of the account
#print(nonce)
#Build a transaction
transaction=Start.constructor().build_transaction({
    "chainId":chain_id,
    "from":my_address,
    "nonce":nonce,
    "gasPrice":w3.eth.gas_price
})
#print(transaction)
signed_txn=w3.eth.account.sign_transaction(transaction,private_key=private_key) #sign the transaction with private key
txn_hash=w3.eth.send_raw_transaction(signed_txn.raw_transaction) #send the signed transaction   
txn_recipt=w3.eth.wait_for_transaction_receipt(txn_hash) #wait for the transaction to be mined and get the transaction receipt
Start=w3.eth.contract(address=txn_recipt.contractAddress,abi=abi) #create the contract instance with the newly deployed address
print(Start.functions.retrieve().call()) #call the retrieve function of the contract 
#calls are used to read data from the blockchain without making a state change
#Transact are used to write data to the blockchain and make state changes

store_transaction=Start.functions.store(15).build_transaction({
    "chainId":chain_id,
    "from":my_address,
    "nonce":nonce+1,
    "gasPrice":w3.eth.gas_price
}
)
signed_store_txn=w3.eth.account.sign_transaction(store_transaction,private_key=private_key) #sign the transaction with private key
send_store_txn=w3.eth.send_raw_transaction(signed_store_txn.raw_transaction) #  send the signed transaction  
txn_recipt=w3.eth.wait_for_transaction_receipt(send_store_txn) #wait for the transaction to be mined and get the transaction receipt
Start.functions.retrieve().call() #call the retrieve function of the contract

print("Deploying Contract...")