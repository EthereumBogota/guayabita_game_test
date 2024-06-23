import os
import json
from web3 import Web3

# with open("contract_abi.json") as archivo:
#     ABI = json.load(archivo)
with open("contracts/contract_abi.json") as f:
    info_json = json.load(f)
ABI = info_json["output"]["abi"]

CONTRACT = os.environ["CONTRACT"]
WALLET = os.environ["WALLET"]
PRIV_KEY = os.environ["PRIV_KEY"]

polygon_rpc_url = 'https://endpoints.omniatech.io/v1/matic/mumbai/public'
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

if w3.is_connected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")

contract_address = CONTRACT
contract_abi = ABI

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

account_address = WALLET
private_key = PRIV_KEY

result = contract.functions.leerSaludo().call()
print("Resultado de la consulta:", result)

