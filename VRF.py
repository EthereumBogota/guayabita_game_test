import os
import json
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("contracts/VRFv2Consumer_abi.json") as f:
    info_json = json.load(f)
ABI = info_json["output"]["abi"]

CONTRACT = os.environ["CONTRACT_VRF"]
WALLET = os.environ["WALLET"]
PRIV_KEY = os.environ["PRIV_KEY"]

sepolia_rpc_url = 'https://rpc.sepolia.org/'


def oracle_random_number():
    """
    this function call a random number from chainlink
    :return:
    """
    w3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))

    if w3.is_connected():
        print("-" * 50)
        print("Connection Successful")
        print("-" * 50)
    else:
        print("Connection Failed")

    contract_address = CONTRACT
    contract_abi = ABI
    queries = 20

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    account_address = WALLET
    private_key = PRIV_KEY

    function_data = contract.functions.requestRandomWords().build_transaction({
        'from': account_address,
        'gas': 5000000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': w3.eth.get_transaction_count(account_address),
        'chainId': 11155111,
    })

    signed_transaction = w3.eth.account.sign_transaction(function_data, private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    print("Hash send transaction: ", transaction_hash.hex())

    time.sleep(10)

    result = contract.functions.lastRequestId().call()
    print("lastRequestId:", result)

    for i in range(queries):
        request_status = contract.functions.s_requests(result).call()
        if request_status[0]:
            raw_number = contract.functions.getRequestStatus(result)
            print("Request OK")
            break

        else:
            print("Processing request")
            raw_number = None
            time.sleep(10)

    print("VRF random number: ")
    print(raw_number.arguments[0])

    return raw_number.arguments[0]
