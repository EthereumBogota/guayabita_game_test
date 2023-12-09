import os
import json
from web3 import Web3


with open("contracts/VRFv2Consumer_abi.json") as f:
    info_json = json.load(f)
ABI = info_json["output"]["abi"]

CONTRACT = os.environ["CONTRACT_VRF"]
WALLET = os.environ["WALLET"]
PRIV_KEY = os.environ["PRIV_KEY"]

sepolia_rpc_url = 'https://rpc.sepolia.org/'
w3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))

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

result = contract.functions.lastRequestId().call()
print("lastRequestId:", result)

# # Interactuar con la función guardarSaludo
# greeting_message = "Saludos desde la casa con Jhonsito"
# function_data = contract.functions.guardarSaludo(greeting_message).build_transaction({
#     'from': account_address,
#     'gas': 3000000,
#     'gasPrice': w3.to_wei('10', 'gwei'),
#     'nonce': w3.eth.get_transaction_count(account_address),
#     'chainId': 80001,
# })
#
# signed_transaction = w3.eth.account.sign_transaction(function_data, private_key)
# transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
#
# print("Hash de la transacción enviada:", transaction_hash.hex())

# https://mumbai.polygonscan.com/tx/0x663fcce44e2507b9a0fb49b194149670b10fec18442d3a5b2234a682b2784a54
