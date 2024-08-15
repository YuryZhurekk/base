from web3 import Web3
import json
import time
import random

web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/base'))


with open('claim.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)


contract_address = "0xa7891c87933BB99Db006b60D8Cb7cf68141B492f" 


contract = web3.eth.contract(address=contract_address, abi=contract_abi)

with open('wallets.txt', 'r') as file:
    private_keys = [line.strip() for line in file.readlines()]


_quantity = 1
_currency = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
_pricePerToken = 0
_allowlistProof = (
    ["0x0000000000000000000000000000000000000000000000000000000000000000"], 
    1, 
    0,  
    _currency 
)
_data = b''

for private_key in private_keys:
    account = web3.eth.account.from_key(private_key)
    _receiver = account.address
    nonce = web3.eth.get_transaction_count(_receiver)
    gas_price = web3.eth.gas_price

    transaction = contract.functions.claim(
        _receiver,
        _quantity,
        _currency,
        _pricePerToken,
        _allowlistProof,
        _data
    ).build_transaction({
        'chainId': 8453,
        'nonce': nonce,
        'gasPrice': gas_price,
    })

    gasLimit = web3.eth.estimate_gas(transaction)
    transaction['gas'] = int(gasLimit * random.uniform(1.1, 1.2))
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_link = f"https://basescan.org/tx/{txn_hash.hex()}"
    print(f"Транзакция отправлена для {_receiver}: {txn_link}")

    delay = random.uniform(10, 20) 
    print(f"Задержка {delay:.2f} секунд перед следующей транзакцией.")
    time.sleep(delay)
