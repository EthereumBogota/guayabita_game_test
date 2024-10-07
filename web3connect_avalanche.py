import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("contracts/abi_avax.json") as f:
    info_json = json.load(f)
ABI = info_json["output"]["abi"]

CONTRACT = "0x218f6f72CA0c09313DC279641c9575F6e6C781CC"
WALLET = os.environ["WALLET"]
PRIV_KEY = os.environ["PRIV_KEY"]

avalanche_rpc_url = 'https://avalanche-fuji.blockpi.network/v1/rpc/public'
w3 = Web3(Web3.HTTPProvider(avalanche_rpc_url))

if w3.is_connected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
    print(w3.eth.block_number)
    print("-" * 50)
    balance = w3.eth.get_balance(WALLET)
    print(f"Balance: {w3.from_wei(balance, 'ether')} AVAX")
    print("-" * 50)

else:
    print("Connection Failed")

contract_address = CONTRACT
contract_abi = ABI

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

account_address = WALLET
private_key = PRIV_KEY

result = contract.functions.leerSaludo().call()

print(result)

function_data = contract.functions.guardarSaludo("Hola desde la casa de Oscar").build_transaction({
    'from': account_address,
    'gas': 200000,
    'maxFeePerGas': w3.to_wei('35', 'gwei'),  # Limite total del gas
    'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),  # Comisión preferente para minería
    'nonce': w3.eth.get_transaction_count(WALLET),
    'chainId': 43113,
})

signed_transaction = w3.eth.account.sign_transaction(function_data, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print("Hash send transaction: ", transaction_hash.hex())

result2 = contract.functions.leerSaludo().call()

print("Resultado de la consulta:", result2)

