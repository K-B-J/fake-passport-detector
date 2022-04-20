from solcx import compile_standard, install_solc
from web3 import Web3, exceptions
from dotenv import load_dotenv
import json
import os

load_dotenv()
install_solc("0.6.0")

contract_address = "0x286cc2B2D00827B0a29A655cf387403c79d17151"

with open("./main/passport.sol", "r") as file:
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

with open("./main/compiled-sol.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["passport.sol"]["PassportContract"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["passport.sol"]["PassportContract"]["abi"]

contract_id, contract_interface = compiled_sol.popitem()


# Web3 to connect to ganache
w3 = Web3(Web3.HTTPProvider(os.environ.get("HTTP_PROVIDER")))
chain_id = 4
my_address = "0x7074ee5A5F811Be196D3AFccD960cE15EF2E11Cb"
private_key = os.environ.get("PRIVATE_KEY")


# Making Contract
Passport = w3.eth.contract(abi=abi, bytecode=bytecode)

# getting latest transaction which is also nonce
nonce = w3.eth.getTransactionCount(my_address)

# Print statement to get the nonce number when the server is run
print("\nCurrent Nonce:", nonce)


def deployContract(Passport):
    # 1. Build transaction
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


if contract_address == "":
    txnReceipt = deployContract(Passport)
    passport = w3.eth.contract(address=txnReceipt.contractAddress, abi=abi)

    # Print statemtents to get the contract address when a new contract is deployed
    print("Contract Address:", txnReceipt.contractAddress)
    print("Contract Deployed Successfully\n")
else:
    passport = w3.eth.contract(address=contract_address, abi=abi)

    # Print statement for confirming that the contract was fetched successfully
    print("Contract Fetched Successfully\n")


def new_passport(passnum, personal_info, imagesInfo, passportInfo):
    global nonce
    try:
        store_transaction = passport.functions.storePassport(
            passnum, personal_info, imagesInfo, passportInfo
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
        w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Entered Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def get_passport_details(passnum):
    global nonce
    w3.eth.contract(abi=abi, bytecode=bytecode)
    try:
        data = passport.functions.getPassportDetails(passnum).call()
        isNonExistent = True
        for field in data:
            if field != "":
                isNonExistent = False
                break
        if isNonExistent:
            return {"success": False, "data": "Passport Hasn't Been Uploaded"}
        else:
            return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def update_passport_details(passnum, personalInfo, imagesInfo, passportInfo):
    global nonce
    try:
        store_transaction = passport.functions.updateDetails(
            passnum, personalInfo, imagesInfo, passportInfo
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
        w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Updated Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}
