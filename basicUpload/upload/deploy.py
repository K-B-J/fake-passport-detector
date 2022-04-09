from solcx import compile_standard, install_solc
import json
from web3 import Web3, exceptions
import os

from dotenv import load_dotenv

load_dotenv()

with open("basicUpload/upload/passport.sol", "r") as file:
    passport_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"passport.sol": {"content": passport_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("basicUpload/upload/compiled-sol.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["passport.sol"]["PassportContract"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["passport.sol"]["PassportContract"]["abi"]

contract_id, contract_interface = compiled_sol.popitem()


# Web3 to connect to ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_PROVIDER")))
chain_id = 4
my_address = "0x3CA0790A8BC2A2BBa7173FDCe363a887BA7fDE3f"
private_key = os.getenv("PRIVATE_KEY")


# Making Contract
Passport = w3.eth.contract(abi=abi, bytecode=bytecode)

# getting latest transaction which is also nonce
nonce = w3.eth.getTransactionCount(my_address)
print("nonce:", nonce)


def deployContract(Passport):
    global nonce
    transaction = Passport.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    nonce += 1
    # 2. Signing the Transaction
    signedTxn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # 3. Sending Signed Transaction
    txnHash = w3.eth.send_raw_transaction(signedTxn.rawTransaction)

    # Waiting for confirmation/receipt
    txnReceipt = w3.eth.wait_for_transaction_receipt(txnHash)

    return txnReceipt


contract_address = "0x6C6A9Dc534708293B0BF888611f51Dd27D792F30"

if contract_address == "":
    txnReceipt = deployContract(Passport)
    print(txnReceipt.contractAddress)
    passport = w3.eth.contract(address=txnReceipt.contractAddress, abi=abi)
    print("Contract Deployed!")
else:
    passport = w3.eth.contract(address=contract_address, abi=abi)
    print("Contract Deployed!")


def new_passport(passport, passnum, name, dob):
    global nonce
    try:
        store_transaction = passport.functions.storePassport(
            passnum, name, dob
        ).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )

        nonce += 1
        signed_store_txn = w3.eth.account.sign_transaction(
            store_transaction, private_key=private_key
        )
        send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_store_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Entered Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def get_passport_details(passport, passnum):
    try:
        data = passport.functions.getPassportDetails(passnum).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def update_passport_details(passport, passnum, name):
    global nonce
    try:
        store_transaction = passport.functions.updateDetails(
            passnum, name
        ).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )

        nonce += 1
        signed_store_txn = w3.eth.account.sign_transaction(
            store_transaction, private_key=private_key
        )
        send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_store_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Updated Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


# while True:
#     ip = int(input())
#     if ip == 0:
#         print(new_passport(passport, "K103", "kaushal", "14-11-2000"))
#     elif ip == 1:
#         print(get_passport_details(passport, "K103"))
#     elif ip == 2:
#         print(update_passport_details(passport, "K103", "Kaushal"))
#     elif ip == 3:
#         break
#     else:
#         continue
