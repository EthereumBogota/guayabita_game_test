import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("contracts/contract_abi.json") as f:
    info_json = json.load(f)
ABI = info_json["output"]["abi"]

CONTRACT = "0x0B5cc2045DF06C1E5356d8F1380c626f6DCFEB40"
WALLET = os.environ["WALLET"]
PRIV_KEY = os.environ["PRIV_KEY"]

arbitrum_rpc_url = 'https://endpoints.omniatech.io/v1/arbitrum/sepolia/public'
w3 = Web3(Web3.HTTPProvider(arbitrum_rpc_url))

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

function_data = contract.functions.guardarSaludo("Hola desde la casa de Oscar").build_transaction({
    'from': account_address,
    'gas': 5000000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'nonce': w3.eth.get_transaction_count(WALLET),
    'chainId': 421614,
})

signed_transaction = w3.eth.account.sign_transaction(function_data, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print("Hash send transaction: ", transaction_hash.hex())

result2 = contract.functions.leerSaludo().call()

print("Resultado de la consulta:", result2)

