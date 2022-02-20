import base64
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee
from terra_sdk.util.contract import get_code_id, get_contract_address
import json

def execute_contract(sender: str, contract_address: str, execute_msg, client):
    execute = MsgExecuteContract(
        sender = sender.key.acc_address,
        contract = contract_address,
        execute_msg = execute_msg
    )

    execute_tx = sender.create_and_sign_tx(CreateTxOptions(
        msgs=[execute],
        memo="execute contract",
        fee=Fee(4000000, "10000000uluna")
    ))
    execute_tx_result = client.tx.broadcast(execute_tx)
    return execute_tx_result

def mint(signer, to, amount, client):
    """
    signer: the actual wallet of the contract caller
    to: actual wallet of receiver of tokens
    """
    addresses = None
    with open("addresses.json", "r") as fp:
        addresses = json.load(fp)

    cw20_contract_address = addresses["cw20"]["contract_address"]
    return execute_contract(signer, cw20_contract_address, {"mint": {"txSigner":signer.key.acc_address, "recipient":to.key.acc_address, "amount":amount}}, client)

def transfer(signer, to, amount):
    addresses = None
    with open("addresses.json", "r") as fp:
        addresses = json.load(fp)

    cw20_contract_address = addresses["cw20"]["contract_address"]
    return execute_contract(signer, cw20_contract_address, {"transfer":{"txSigner":signer.key.acc_address, "recipient":to.key.acc_address, "amount":amount}})


def balance(sender_address: str, client):
    addresses = None
    with open("addresses.json", "r") as fp:
        addresses = json.load(fp)

    cw20_contract_address = addresses["cw20"]["contract_address"]
    bal = client.wasm.contract_query(
        cw20_contract_address,
        {"balance": {"address": sender_address}}
    )
    return bal["balance"]